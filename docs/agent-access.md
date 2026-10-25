# Agent access

The assistant should receive the smallest authorized evidence bundle that supports the question, together with what remains unknown. A retrieval result should preserve classification, validity and provenance rather than returning anonymous chunks.

## The implemented interface

`demo/brain.py` is a local CLI. It reads a bundled JSON fixture and Markdown sources, then emits JSON. The default audience is `general`; `--audience marketing` simulates a second role. This flag is not authentication or an enforceable security boundary: anyone with this public repository can read every synthetic file.

The tests verify that filtering excludes an inaccessible topic from the returned answer, even when it matches the query. They do not establish production authorization.

```sh
python3 demo/brain.py "Q4 marketing strategy" --domain marketing
python3 demo/brain.py "Q4 marketing strategy" --as-of 2027-01-01
python3 demo/brain.py "What is the hotel's payroll policy?"
```

The last two commands abstain. An unknown domain produces the same generic abstention as an unknown topic. On answerable input, sources include repository-relative paths, inclusive line ranges and hashes. Evidence hashes must still match before an answer is returned.

## A possible MCP boundary

MCP could carry structured tools such as `search_knowledge`, `read_evidence` and `propose_knowledge_change`. These names are illustrative contracts, not implemented tools in this repository. MCP supplies an interoperability boundary; it does not decide which company statements are authoritative or who may change them.

A service implementing such tools would authenticate the caller, authorize every retrieval and source read, bound result size, and separate read scopes from proposal or execution scopes. Changes would remain proposals until the application accepts the exact revision. Documents and tool outputs remain untrusted data, including instructions embedded in retrieved text.

A business action, such as launching a campaign, needs a separate tool and explicit authorization policy. Correct retrieval alone does not authorize that action. No action tools or MCP server are included here.
