---
name: write-readme
description: Probe a repository's facts and audit its README section by section, with evidence for every verdict.
disable-model-invocation: true
metadata:
  version: 0.1.0
  tags: [readme, documentation, audit]
  scope: global
---

# write-readme

先探查仓库事实，再按固定骨架逐节审计 README，产出逐行带证据的 gap 报告。

## 何时使用

- 仓库没有 `README.md`，或 README 已经落后于代码和脚本。
- 安装、运行命令与 `scripts/`、CI 对不上，想知道差在哪。
- 给 monorepo 的某个子包补 README：给一个路径就审计那个目录，缺省审计仓库根目录。
- 对外发布前，先要一张按小节排好的缺口清单。

## 探查

在目标目录里逐项取证，只记能指回文件或命令输出的内容。

| 探查项 | 读出的事实 |
|---|---|
| 顶层目录树 | 模块划分与语言，开篇句与 Architecture 的素材 |
| 已有 `README` / `CONTRIBUTING` / `LICENSE` / `docs/` | 哪些小节能指向现成文件，链接目标是否真实存在 |
| 清单文件：`package.json`、`pyproject.toml`、`Cargo.toml`、`go.mod`、`pom.xml`、`*.csproj`、`Gemfile`、`composer.json` | 包名、运行时版本、依赖、可执行的入口 |
| `scripts` 段与 `Makefile` / `justfile` | 安装、构建、测试、运行的真实命令 |
| `.github/workflows/` | CI 实际跑的命令与平台矩阵，用来核对命令真能跑 |
| `git remote` | 仓库 URL 与宿主，徽章、clone 地址、issue 入口的来源 |

顶层目录树指目标目录的一级成员；子包路径下同法取证。

清单查不到的事实——对外联系人、维护状态意图、是否对外发布——列成问题问人；问到之前保持空着。

完成判据：清单六项各自留下证据。

## 审计

按下面的固定骨架逐节对照证据，报告的排序与骨架一致。报告直接回在对话里，不写磁盘。

```text
# <项目名>
（1–3 句：做什么 + 为什么有用）
[徽章] [截图/演示]                                   条件
## Status                                           必写：一行维护状态
## Getting started                                  必写：前置要求 + 安装 + 构建 + 运行
## Usage                                            必写：示例 + 预期输出
[## Configuration]                                  条件：有配置项
[## Architecture]                                   条件：多模块
[## Documentation]                                  条件：有独立文档
## Getting help                                     必写：求助入口 + 维护者联系方式
## Contributing                                     必写：指向 CONTRIBUTING.md 与 PR 流程
## License                                          必写：许可证名 + 指向 LICENSE
[## Acknowledgements / Related projects / Citation]  条件
```

每个小节给一个现状：

- **有**：小节在，内容与证据一致。
- **缺**：整节不在。
- **不准确**：小节在，但与证据矛盾、过期，或只剩占位符。

条件小节因项目里没有对应对象而不出现时，写「不适用」，并写出缺的条件。

证据落到文件路径加行号，或一条命令加输出；查不到就写「无」。

完成判据：六个必写节各有一行现状和一条证据；每个条件节要么给出结论，要么写明不适用的理由。

## 参考资料

- `references/audit-report.md`：报告的四列、动作词与一份按本骨架填好的范例；写报告前读。
