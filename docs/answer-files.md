# Answer files and site decisions

`files/RHEL9_Answerfile.xml` provides technical exceptions for evaluator
limitations. DEFAULT runs live validation and fails closed when its prerequisites
are missing. Review the code against your evaluator version and benchmark before
opting in. For example, custom checks recognize enforcing PAM `requisite` rules,
systemd AIDE scheduling, protected user keys and existing audit rule renderings.

`examples/RHEL9_Site_Answerfile.xml` contains procedural templates under the
SITE_POLICY key. Their statuses remain Not Reviewed. They deliberately provide
no approval, production boundary, encrypted-storage attestation, forwarding
assertion, patch-currency assertion or authoritative NTP source determination.
Copy and edit these entries into your private site answer file only after the
responsible reviewer records supporting evidence and chooses an appropriate
status. Renaming a key or selecting a template does not establish compliance.

The firewall and account validators consume root-owned records created from
explicitly configured role variables. Populate those variables from approvals
in the actual inventory. The role's empty defaults do not approve observed state.

Keep the reviewed site answer file outside the public repository. If another
playbook manages your installed evaluator, synchronize that deployment source as
well as the file on the managed host. Public DEFAULT no longer includes the lab's
manual NF/NA determinations; importing those old results into another system
would be incorrect.
