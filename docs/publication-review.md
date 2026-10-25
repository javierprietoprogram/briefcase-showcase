# Publication review

Review date: 2026-10-25. Scope: the public showcase, its bundled fixture and its complete Git history, including the presentation polish.

The documentation and Python demonstration were authored specifically for this repository. The example uses an invented organization, fictional people and fabricated business events. It contains no exported company documents, live connector outputs or production implementation.

The pre-publication review checks every publishable file and the Git commit metadata and blobs for credential patterns, email addresses, non-public URLs, local filesystem paths and confidential names. Evidence fingerprints in the fixture are expected SHA-256 values of the bundled synthetic sources, not credentials. Git uses a generic no-reply author address, rather than a private author email.

Manual review checks the origin of every example, every external link and each claim about implementation. External links are limited to the public Briefcase website and this public repository’s GitHub Actions test status. MIT license text is standard license boilerplate. No external dependencies, telemetry, credentials or network requests are required by the demo.

Fourteen behavioral tests cover the accepted answer, source mutation and absence, approval evidence, conflicting decisions, proposal status, visibility and domain filtering, validity boundaries, topic ambiguity, unsupported questions and invalid source paths or locators. These are checks of the small synthetic implementation, not a security certification or production benchmark.

Deliberately excluded: company knowledge records, project identities, customer information, messages, internal operating instructions, deployment details, vendor identifiers, unpublished plans and proprietary code. Only high-level architectural ideas and public company positioning are described.

For subsequent changes, repeat the file and history checks before publishing. An ignore rule alone cannot remove sensitive data already committed.

The presentation pass adds a read-only GitHub Actions test job on push and pull request, using commit-pinned official actions and Python 3.10. It also adds a test-status badge and a Mermaid view of the synthetic answer flow. The demo, fixture and conceptual architecture are unchanged. The private knowledge repository was not accessed during this pass.
