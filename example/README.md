# Synthetic company walkthrough

Northstar Hotels, its staff and all business information here are invented for this repository. Any resemblance to an existing organization or person is coincidental. No real company data was used to construct the fixtures.

| Artifact | What it says | How it should be treated |
| --- | --- | --- |
| `sources/project-draft.md` | Discount advertising is proposed | Context, not an accepted plan |
| `sources/meeting.md` | Participants favor direct-booking content | Evidence of discussion |
| `sources/decision.md` | The direct-booking choice is approved | Authority for the current answer |
| `sources/previous-decision.md` | Earlier exploratory advertising choice | Superseded history |
| `knowledge.json` | Links evidence, classifications, scope and validity | Reviewed synthetic model used by the CLI |

All paths above are relative to `synthetic-company/`.

The fictional participants are Morgan Vale (marketing owner) and Casey Linden (operations reviewer). The current decision runs from 2026-10-15 through 2026-12-31. Its review is simulated in the decision note; it is not a real approval event.

The demonstration distinguishes the draft from the accepted outcome rather than merging them into a contradictory summary. It retrieves the current decision and returns its three supporting sources. It preserves the earlier decision without treating it as current.

To see evidence-integrity failure, change a source file locally and run the CLI again. It returns `review_required`. The fixture hash must only change after reviewing that source; regenerating a hash by itself is not review. The automated tests perform this mutation in temporary directories.

The code uses a fixed, explicit topic vocabulary and templated answer. It does not claim natural-language understanding, real entity resolution, semantic search or complete coverage of company questions.
