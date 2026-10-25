"""Deterministic retrieval over a synthetic knowledge fixture. No network or LLM."""
import argparse
from datetime import date
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = Path('example/synthetic-company/knowledge.json')
DEFAULT_DATE = '2026-10-20'


def abstain():
    return {'status': 'abstained', 'reason': 'No supported, permitted, current decision.'}


def review(reason):
    return {'status': 'review_required', 'reason': reason}


def evidence(root, source):
    relative = Path(source['path'])
    path = (root / relative).resolve()
    if relative.is_absolute() or not path.is_relative_to(root.resolve()):
        raise ValueError('Evidence must stay inside the fixture repository.')
    if any((root / Path(*relative.parts[:i])).is_symlink()
           for i in range(1, len(relative.parts) + 1)):
        raise ValueError('Evidence symlinks are not supported.')
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != source['sha256']:
        raise ValueError('Evidence changed after review.')
    first, last = source['lines']
    if not 1 <= first <= last <= len(data.decode('utf-8').splitlines()):
        raise ValueError('Invalid evidence locator.')
    return {'id': source['id'], 'path': relative.as_posix(),
            'lines': [first, last], 'sha256': source['sha256']}


def answer(question, *, root=ROOT, audience='general', domain=None, as_of=DEFAULT_DATE):
    """Fixture metadata is trusted; audience is a simulation, not authentication."""
    root = Path(root)
    when = date.fromisoformat(as_of)
    model = json.loads((root / FIXTURE).read_text())
    if model.get('synthetic') is not True or model.get('schema_version') != 1:
        return review('Unsupported synthetic fixture.')
    query = ' '.join(re.findall(r'\w+', question.lower()))

    def mentions(term):
        return re.search(r'(?<!\w)' + re.escape(term) + r'(?!\w)', query) is not None

    topics = [t for t in model['topics']
              if audience in t['audiences'] and (domain is None or t['domain'] == domain)
              and all(any(mentions(term) for term in group) for group in t['query_terms'])]
    if not topics:
        return abstain()
    if len(topics) != 1:
        return review('Multiple permitted topics match; clarify the scope.')
    records = [r for r in model['records'] if r['topic_id'] == topics[0]['id']]
    candidates = [r for r in records if r['kind'] == 'decision' and r['status'] == 'approved'
                  and date.fromisoformat(r['valid_from']) <= when
                  <= date.fromisoformat(r['valid_until'])]
    if not candidates:
        return abstain()
    if len(candidates) != 1:
        return review('Conflicting approved decisions require review.')
    chosen = candidates[0]
    approval = chosen.get('approval') or {}
    if not approval.get('reviewer') or approval.get('source_id') not in chosen['source_ids']:
        return review('Decision has no linked approval evidence.')
    sources = {s['id']: s for s in model['sources']}
    if len(sources) != len(model['sources']) or len(set(chosen['source_ids'])) != len(chosen['source_ids']):
        return review('Duplicate evidence identifiers require review.')
    try:
        citations = [evidence(root, sources[s]) for s in chosen['source_ids']]
    except (KeyError, ValueError, OSError, UnicodeError):
        return review('Supporting evidence is missing, changed or invalid.')
    return {'status': 'answered', 'as_of': when.isoformat(),
            'answer': {'decision': chosen['summary'], 'owner': chosen['owner'], 'scope': chosen['scope']},
            'decision_id': chosen['id'], 'sources': citations,
            'qualifications': ['The project draft is a proposal, not the approved decision.']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('question', nargs='?', default="What was decided about the hotel's Q4 marketing strategy?")
    parser.add_argument('--audience', choices=['general', 'marketing'], default='general',
                        help='Synthetic visibility simulation; not authentication.')
    parser.add_argument('--domain')
    parser.add_argument('--as-of', default=DEFAULT_DATE, type=date.fromisoformat,
                        help='Validity date YYYY-MM-DD; fixed demo default.')
    args = parser.parse_args()
    result = answer(args.question, audience=args.audience, domain=args.domain, as_of=str(args.as_of))
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
