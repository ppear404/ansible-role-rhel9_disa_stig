# Third-party references

The role targets the **DISA RHEL 9 STIG V2R10**. Benchmark control identifiers
identify external requirements; this project is not an official DISA or Red Hat
product and does not implement the full benchmark. Obtain benchmark documents
from the [DISA Cyber Exchange](https://www.cyber.mil/stigs/downloads/).

**Evaluate-STIG** is an independent assessment tool. Obtain its distribution and
review its license and integrity information separately. Its source, archives,
checklists, documentation and logos are not part of this repository.

`files/sssd_dod_roots.pem` contains public DoD root CA certificates, not private
keys. The role pins the bundle's SHA-256 digest. Review certificate subjects,
validity, trust scope and current authoritative distribution before deployment.
The project license covers the role code; it does not confer rights in external
products, marks or independently issued certificates.

PowerShell installation uses Microsoft's signed RHEL repository. See the
[Microsoft installation instructions](https://learn.microsoft.com/powershell/scripting/install/install-rhel).
