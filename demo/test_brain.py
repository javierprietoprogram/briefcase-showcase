"""Authority, evidence integrity and disclosure checks on disposable fixtures."""
import copy
import json
from pathlib import Path
import shutil
import tempfile
import unittest

from brain import answer, ROOT, FIXTURE

QUESTION = "What was decided about the hotel's Q4 marketing strategy?"


class RetrievalTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=ROOT, prefix='.test-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        shutil.copytree(ROOT / 'example', self.root / 'example')
        self.model = json.loads((self.root / FIXTURE).read_text())

    def save(self):
        (self.root / FIXTURE).write_text(json.dumps(self.model))

    def ask(self, question=QUESTION, **options):
        return answer(question, root=self.root, **options)

    def test_approved_choice_has_three_sources(self):
        result = self.ask()
        self.assertEqual(result['decision_id'], 'NS-DEC-02')
        self.assertEqual({s['id'] for s in result['sources']}, {'draft', 'meeting', 'decision'})
        self.assertIn('do not launch', result['answer']['decision'])

    def test_changed_evidence_requires_review(self):
        path = self.root / self.model['sources'][0]['path']
        path.write_text(path.read_text() + '\nChanged after review.\n')
        self.assertEqual(self.ask()['status'], 'review_required')

    def test_missing_evidence_requires_review(self):
        self.model['sources'] = self.model['sources'][1:]
        self.save()
        self.assertEqual(self.ask()['status'], 'review_required')

    def test_conflicting_approved_decisions_are_not_ranked_away(self):
        conflicting = copy.deepcopy(self.model['records'][-1])
        conflicting.update(id='NS-DEC-CONFLICT', summary='Launch discount ads now.')
        self.model['records'].append(conflicting)
        self.save()
        self.assertEqual(self.ask()['status'], 'review_required')

    def test_proposals_do_not_become_decisions(self):
        self.model['records'][-1]['status'] = 'pending'
        self.save()
        self.assertEqual(self.ask()['status'], 'abstained')

    def test_approval_must_link_to_evidence(self):
        self.model['records'][-1]['approval']['source_id'] = 'unknown'
        self.save()
        self.assertEqual(self.ask()['status'], 'review_required')

    def test_visibility_filter_does_not_disclose_topic_or_sources(self):
        self.model['topics'][0]['audiences'] = ['marketing']
        self.save()
        self.assertEqual(self.ask(), self.ask('unrelated question'))
        self.assertEqual(self.ask(audience='marketing')['status'], 'answered')

    def test_domain_filter_does_not_disclose_topic(self):
        self.assertEqual(self.ask(domain='payroll'), self.ask('unrelated question'))

    def test_validity_interval_is_bounded_and_inclusive(self):
        for day in ['2026-10-14', '2027-01-01']:
            self.assertEqual(self.ask(as_of=day)['status'], 'abstained')
        for day in ['2026-10-15', '2026-12-31']:
            self.assertEqual(self.ask(as_of=day)['status'], 'answered')

    def test_similar_word_is_not_topic_match(self):
        self.assertEqual(self.ask('Q40 marketing')['status'], 'abstained')

    def test_ambiguous_topic_requires_clarification(self):
        duplicate = copy.deepcopy(self.model['topics'][0])
        duplicate['id'] = 'OTHER-TOPIC'
        self.model['topics'].append(duplicate)
        self.save()
        self.assertEqual(self.ask()['status'], 'review_required')

    def test_path_escape_is_rejected(self):
        self.model['sources'][0]['path'] = '../outside.md'
        self.save()
        self.assertEqual(self.ask()['status'], 'review_required')

    def test_invalid_locator_is_rejected(self):
        self.model['sources'][0]['lines'] = [1, 10000]
        self.save()
        self.assertEqual(self.ask()['status'], 'review_required')

    def test_unknown_question_abstains(self):
        self.assertEqual(self.ask('What is the hotel payroll policy?')['status'], 'abstained')


if __name__ == '__main__':
    unittest.main()
