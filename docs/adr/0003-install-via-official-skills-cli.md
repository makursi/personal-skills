# 安装交给官方 skills CLI

**Status:** accepted（取代 [ADR 0002](./0002-link-install-instead-of-copy.md)）

分发与安装改为使用官方 `skills` CLI（npm 包 `skills`，出自 vercel-labs/skills，写作时 1.9.0，要求 Node >= 22.20）。安装命令是 `npx skills add makursi/personal-skills -g`，产物是复制进消费目录 `~/.agents/skills` 的 skill 目录，由 CLI 记进自己的 lock 文件；仓库自带的 junction 安装器已删除。

反悔的触发是分发面。ADR 0002 成立的前提是“只有这一台机器、只有本人使用”，这个前提已经不成立：仓库公开后，这台机器之外的人也要能把仓库装到自己机器上，而 junction 和目录符号链接都是本机路径的别名，换一台机器就失效。跨机器安装只能落在复制上，复制则交给平台认可的安装器，比自建脚本可靠。

## Considered Options

- **只保留 junction 安装器**：否决理由：跨机器安装无从谈起，仓库公开后的第一条使用路径就是 CLI；两套安装器并存还会产出两种不一致的安装结果。
- **自建安装器发布到 npm**：否决理由：重复实现 `skills` 已有的 add/update/list，还要自己追各 Agent 的消费目录约定；平台认可的路径已经存在，自建只会更早腐坏。

## Consequences

- 安装从链接变成复制：消费目录里的副本不再随仓库即时生效，更新要显式跑 `skills update`。
- `skills update` 删除并重建消费目录，消费者在副本上的手改会被丢弃。这正是 ADR 0002 拒绝复制时引用的风险，现在从“本仓库内部的一致性”转移到“消费者的改动”。
- 安装器只剩一个，仓库不再维护安装脚本；消费目录路径与 lock 文件交给 CLI。
- `skills/` 仍是唯一真源，装出去的是副本；改 skill 只能改仓库，不能改消费目录。
- ADR 0002 整体失效，由本文件取代。
