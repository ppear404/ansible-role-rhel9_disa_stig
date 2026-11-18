# Contributing

Keep changes scoped to a control and identify the benchmark revision, Vuln ID,
Rule ID, applicability, and pass criteria. Use the Develop → Test → Deploy →
Validate workflow in AGENTS.MD. Obtain benchmark/evaluator references separately;
do not commit downloaded distributions or copied benchmark documents.

Run the validation commands in README.md. Use a dedicated RHEL 9 test system for
live checks, review check-mode output, deploy only to the explicit inventory limit,
and verify effective state and idempotence. CI performs static checks only.

Technical answer-file exceptions must fail closed and collect fresh evidence.
Manual policy decisions belong in a separately reviewed site answer file. Never
include production approvals, credentials, internal inventory, raw checklists,
or unredacted command output in a pull request or issue.
