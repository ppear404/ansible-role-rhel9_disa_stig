# Publishing a public snapshot

Publish only the reviewed role source and examples. Exclude local inventory,
credentials, raw assessments, downloaded evaluator/benchmark distributions and
editor caches. The content guard checks the public working tree; it does not
remove files from earlier Git commits or prove that history is free of secrets.

The original development history contained live inventory and assessment data.
Use a fresh repository initialized from the cleaned source snapshot, or review
and sanitize the entire history before pushing existing refs to a public remote.
Keep the original history and evidence in private storage. A public source archive
must exclude `.git` and all ignored local artifacts.

Before creating the initial public commit, choose the intended public Git author
identity, run the README validation commands and review the staged file list.
The GitHub workflow performs static validation only; enable repository security
reporting and branch protection according to your maintenance process.
