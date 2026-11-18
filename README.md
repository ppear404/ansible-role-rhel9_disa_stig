# RHEL 9 DISA STIG Ansible role

An Ansible role implementing a **subset of DISA RHEL 9 STIG V2R10** controls on
RHEL 9 x86_64. It includes filesystem protections, boot settings, targeted audit
rules, password-quality enforcement, integrity scanning, USB policy, firewall
validation, time configuration and authentication trust settings.

This is a remediation aid, not a complete hardening baseline or a compliance
certification. Existing system configuration, site approvals and independently
verified assessment evidence remain necessary. See the [control map](tests/control-map.md)
and [answer-file guidance](docs/answer-files.md).

## Requirements

- RHEL 9 x86_64, working package repositories, SSH access and sudo/become rights.
- Ansible core 2.16 or later and the `ansible.posix` collection.
- Existing filesystems for configured mount points; the role does not partition disks.
- An existing valid custom authselect profile for PAM password-quality tasks.
- A nonempty, approved AIDE baseline at `/var/lib/aide/aide.db.gz`.
- FIPS installation/boot provisioning completed separately. The role enforces the
  `FIPS` crypto policy but does not provision FIPS boot mode or disk encryption.

Kernel and immutable audit changes can reboot the host. USB deny-all blocks USB
peripherals. Use a dedicated test host and retain recovery access when reviewing
these controls.

## Quick start

Keep the checkout directory named `rhel9_disa_stig`, or install it under that
name in your Ansible roles path.

```sh
ansible-galaxy collection install -r requirements.yml
cp inventory/hosts.ini.example inventory/hosts.ini
mkdir -p inventory/group_vars
cp inventory/group_vars.example.yml inventory/group_vars/rhel9.yml
```

Edit both private inventory files before running. The example address is reserved
for documentation. Local inventory is ignored by Git; use an SSH agent or SSH
configuration and Ansible Vault for credentials and password hashes.

```sh
ansible-playbook tests/test.yml --limit rhel9-dev --list-hosts
ansible-playbook tests/test.yml --limit rhel9-dev --check --diff
ansible-playbook tests/test.yml --limit rhel9-dev
# Repeat the same play to check idempotence.
```

For an existing Ansible project:

```yaml
- name: Apply selected RHEL 9 STIG remediation
  hosts: rhel9
  become: true
  roles:
    - role: rhel9_disa_stig
```

Inventory groups and host names are up to your project. Always use an explicit
`--limit` and confirm the selected hosts before deploying. Use `--tags V-258194`
to select an individual control; include its dependencies when applicable.

## Site variables

The role reads **`rhel9_stig_*`** variables. RHEL 10 variable names are not aliases.
Store the reviewed settings in the actual inventory used by your normal
playbook, so test-only extra vars do not hide missing deployment configuration.

| Variable | Default | Purpose |
| --- | --- | --- |
| `mount_options` | See [defaults](defaults/main.yml) | Required options for existing filesystem paths |
| `grub_superuser` | `grubdev` | Dedicated GRUB-only account name |
| `grub_password_hash` | Undefined | Unique PBKDF2 hash from `grub2-mkpasswd-pbkdf2`; store in Vault |
| `rhel9_stig_root_mail_recipients` | `[]` | Approved root-mail recipients; V-258174 |
| `rhel9_stig_time_servers` | `[]` | Approved authoritative DoW time sources; V-257945 |
| `rhel9_stig_authorized_local_accounts` | `[]` | Approved privileged local interactive accounts; V-258058 |
| `rhel9_stig_firewall_approval` | `{}` | Approved zone, interfaces, services and review reference; V-257937/V-257940 |
| `rhel9_stig_usb_deny_all` | `false` | Enable USB deny-all after reviewing peripherals; V-258038 |

Empty site inputs skip their conditional controls and are reported at the end of
the role. Skipping a task does not satisfy its control. No lab inventory,
recipient, public time pool, boot password or approval is supplied by default.

The firewall control applies a DROP target to the reviewed zone and validates
runtime/permanent settings and listeners. It preserves the configured service
exceptions and disables unapproved RPC exposure. The validator fails on drift;
it does not approve newly observed services. The role rejects unapproved local
interactive accounts without automatically deleting them.

The AIDE timer reports to root through Postfix. Configure the approved root alias
and verify actual delivery separately. Baselines are never automatically
re-created or approved. The SSSD trust task uses the digest-pinned public CA
bundle; review trust applicability and certificate validity before deployment.

## Assessment tools

Evaluate-STIG and official benchmark documents are **not bundled**. Obtain a
reviewed distribution separately; see [third-party notices](THIRD_PARTY_NOTICES.md).
The test playbooks use [tests/evaluator-vars.yml](tests/evaluator-vars.yml) and
allow overrides through your own private vars file.

```sh
ansible-playbook tests/install-powershell.yml --limit rhel9-dev
ansible-playbook tests/prepare-evaluator.yml --limit rhel9-dev \
  -e evaluator_archive=/absolute/path/to/evaluate-stig-1.2610.1.tar.gz
ansible-playbook tests/evaluate.yml --limit rhel9-dev -e phase=baseline
ansible-playbook tests/full-assessment.yml --limit rhel9-dev
```

Preparation installs a separately supplied archive beneath `/opt/eval_stig`.
Set `evaluator_root` and `evaluator_install_dir` when using another version or
layout. PowerShell comes from Microsoft's signed repository; active fapolicyd
package trust is refreshed after installation.

Scans default to native evaluation using a new empty answer directory, preventing
an existing installed answer file from silently changing native results. To opt
in to the reviewed technical answer file:

```sh
ansible-playbook tests/evaluate.yml --limit rhel9-dev \
  -e use_answer_file=true -e phase=answers
ansible-playbook tests/full-assessment.yml --limit rhel9-dev \
  -e evaluator_use_answer_file=true
python3 tests/summarize_evaluation.py tests/evidence/baseline.txt
```

Raw output and fetched checklists go to ignored `tests/evidence/` by default;
override `evaluator_artifacts_dir` to use private storage elsewhere. Treat these
files as sensitive. The public DEFAULT answer key contains technical validators;
manual site templates remain Not Reviewed until separately reviewed and adapted.
Public defaults do not reproduce a particular lab's finding counts.

## Development validation

```sh
python3 -m pip install -r requirements-dev.txt
ansible-galaxy collection install -r requirements.yml
ansible-playbook -i tests/inventory tests/test.yml --syntax-check
ansible-lint --offline tasks handlers defaults vars meta tests/*.yml inventory/group_vars.example.yml
python3 -m py_compile files/firewall_validate.py tests/summarize_evaluation.py
python3 tests/check_public_content.py
```

`tests/inventory` is for static checks only; it targets localhost and must never
be used to deploy the remediation role. GitHub Actions performs syntax, lint,
Python compilation and public-content checks without contacting RHEL systems.
Live validation requires a dedicated RHEL 9 host: capture baseline evidence,
review check mode, deploy, verify effective state, repeat for idempotence and
rerun the matching evaluator checks. Follow [CONTRIBUTING.md](CONTRIBUTING.md)
and [AGENTS.MD](AGENTS.MD).

## Publication

See [publishing guidance](docs/publishing.md) for source-only publication and
handling the private development history. Live inventory, raw assessments and
downloaded evaluator packages belong outside the public repository.

## License

Role code is licensed under [MIT No Attribution (MIT-0)](LICENSE).
See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for external tools and
public certificates, and [SECURITY.md](SECURITY.md) for reporting guidance.
