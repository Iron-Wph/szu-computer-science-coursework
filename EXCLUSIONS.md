# Initial publication exclusions

The source archive was inspected on 2026-08-25 before this public repository was
created. The source contained 117,219 files totaling approximately 32.69 GiB.
The publication snapshot retained 5,259 files totaling approximately 3.21 GiB.

| Category | Files excluded | Approx. size |
| --- | ---: | ---: |
| Dependency folders, build output, and IDE caches | 92,815 | 14.097 GiB |
| Archives | 131 | 4.821 GiB |
| Generated datasets and data assets | 13,699 | 2.941 GiB |
| Model files, databases, and scientific datasets | 78 | 2.520 GiB |
| Videos | 27 | 2.074 GiB |
| Third-party course material | 3,431 | 1.926 GiB |
| Generated temporary files and binaries | 616 | 0.513 GiB |
| Files at or above 49 MiB | 4 | 0.451 GiB |
| Installers and executables | 358 | 0.062 GiB |
| Private personal material | 65 | 0.036 GiB |
| Nested Git metadata | 722 | 0.033 GiB |
| Credentials and local secret files | 14 | 0.005 GiB |

The categories are mutually exclusive according to the first matching filter
rule, so their counts can be added without double-counting. Excluded files remain
only in the local source archive and are not release assets.

Two hard-coded API keys found in copied source were replaced with environment
variable lookups before any Git commit. Mock-account passwords were replaced by
an explicit `<demo-password>` placeholder. The original credentials should be
rotated by their owner even though they were never committed here.
