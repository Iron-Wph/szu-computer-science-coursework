# szu-computer-science-coursework

深圳大学（SZU）计算机科学本科课程作业、实验报告与课程项目归档。

An undergraduate Computer Science coursework archive from Shenzhen University
(SZU), covering programming, algorithms, systems, artificial intelligence,
computer vision, natural language processing, databases, networks, and graphics.

## 课程导航 / Course index

- [大一课程](./大一课程/)：高等数学、线性代数、大学物理、计算机导论、
  计算机系统、数字电路等。
- [大二](./大二/)：数据结构、离散数学、概率论、Java、机器学习、算法设计、
  计算机网络与计算机系统等。
- [大三](./大三/)：Web 编程、数据库、计算机图形学、编译原理、操作系统与
  大模型技术及应用等。
- [大四](./大四/)：计算机视觉、自然语言处理、智能网络与计算等。
- [义往情深](./义往情深/)：课程分享与朋辈学习材料。

目录沿用原课程归档结构，以便课程、实验和报告之间保持对应关系。部分课程
可能只有报告或源代码；被排除的大型数据和依赖应按照项目内说明重新获取。

## Publication scope

This repository is a curated publication snapshot rather than a byte-for-byte
backup. The following are intentionally not published:

- archives, videos, installers, executables, and compiled artifacts;
- virtual environments, dependency folders, IDE caches, and build output;
- API keys, local environment files, private application material, and uploads;
- large datasets, model weights, databases, and generated benchmark data;
- textbooks, answer sets, instructor slides, templates, and other material that
  is not clearly licensed for redistribution;
- individual files at or above 49 MiB.

The initial publication audit retained 5,259 files (about 3.21 GiB) from a local
archive of 117,219 files. See [EXCLUSIONS.md](./EXCLUSIONS.md) for the audit
summary and run [`scripts/verify-publication.ps1`](./scripts/verify-publication.ps1)
before future updates.

## Credentials and local setup

No live credentials are included. Projects that call external model providers
read their credentials from environment variables. Copy [`.env.example`](./.env.example)
to an untracked local environment file and provide only the variables needed by
the project you are running.

## Related standalone projects

- [Curry](https://github.com/Iron-Wph/Curry)
- [RAG](https://github.com/Iron-Wph/RAG)

Their nested Git metadata was not copied into this archive, so this repository
remains a normal monorepo rather than a collection of accidental submodules.

## License and responsible use

Original software authored for this archive is licensed under the
[MIT License](./LICENSE). Original reports, presentations, and images are made
available under [CC BY 4.0](./LICENSE-CONTENT.md), unless a file or directory says
otherwise. Third-party components retain their own licenses and are not
relicensed here.

This is a personal learning archive, not an official Shenzhen University
repository. Use it for reference and reproducible learning, not for submitting
copied coursework. See [DISCLAIMER.md](./DISCLAIMER.md).

---

Keywords: Shenzhen University, SZU, computer science coursework, algorithms,
machine learning, computer vision, NLP, LLM, operating systems, databases,
computer networks, computer graphics.
