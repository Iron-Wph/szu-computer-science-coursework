# Initial publication exclusions

The source archive was inspected on 2026-08-25 before this public repository was
created. The source contained 117,219 files totaling approximately 32.69 GiB.
The automated copy and first cleanup retained 4,942 coursework files totaling
approximately 2.78 GiB. A second content, privacy, license, and file-signature
audit removed another 1,424 files. The final snapshot contains 3,518 coursework
files totaling approximately 2.23 GiB; repository metadata adds nine small
tracked files, for 3,527 tracked files overall.

| Category | Files excluded | Approx. size |
| --- | ---: | ---: |
| Dependency folders, build output, and IDE caches | 92,815 | 14.097 GiB |
| Archives | 131 | 4.821 GiB |
| Generated datasets and data assets | 13,699 | 2.941 GiB |
| Model files, databases, and scientific datasets | 78 | 2.520 GiB |
| Videos | 27 | 2.074 GiB |
| Third-party course material | 3,561 | 2.133 GiB |
| Unverified document ownership | 179 | 0.325 GiB |
| Generated temporary files and binaries | 625 | 0.513 GiB |
| Files at or above 49 MiB | 3 | 0.352 GiB |
| Installers and executables | 358 | 0.062 GiB |
| Private personal material | 65 | 0.036 GiB |
| Nested Git metadata | 722 | 0.033 GiB |
| Credentials and local secret files | 14 | 0.005 GiB |
| Subsequent content, privacy, license, and signature audit | 1,424 | 0.553 GiB |
| **Total excluded** | **113,701** | **about 30.46 GiB** |

The automated categories are mutually exclusive according to the first matching
filter rule. The subsequent-audit row covers files removed from that initial
snapshot, so the final total can be added without double-counting. Excluded files
remain only in the local source archive and are not release assets.

Two hard-coded API keys found in copied source were replaced with environment
variable lookups before any Git commit. Mock-account passwords were replaced by
an explicit `<demo-password>` placeholder, and five local account fixtures with
names, identifiers, email addresses, or password fields were excluded. The final
audit also detects compiled executables by file signature, including binaries
without a filename extension. The original credentials should be rotated by
their owner even though they were never committed here.
