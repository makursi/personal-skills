---
name: write-readme
description: Write or fix a repository's README so it follows a fixed English skeleton and passes a mechanical checker.
disable-model-invocation: true
metadata:
  version: 0.1.0
  tags: [readme, documentation, audit]
---

# write-readme

先探查仓库事实，再按固定骨架逐节审计 README，用户确认草稿后落笔，最后跑机械校验脚本；退出码 0 才算交付。

## 何时使用

- 仓库没有 `README.md`，或 README 已经落后于代码和脚本。
- 安装、运行命令与 `scripts/`、CI 对不上，想知道差在哪。
- 给 monorepo 的某个子包补 README：给一个路径就处理那个目录，缺省处理仓库根目录。
- 对外发布前，先要一张按小节排好的缺口清单，再据此改写。

## 探查

在被审计目录里逐项取证，只记能指回文件或命令输出的内容。

| 探查项 | 读出的事实 |
|---|---|
| 顶层目录树 | 模块划分与语言，开篇句与 Architecture 的素材 |
| 已有 `README` / `CONTRIBUTING` / `LICENSE` / `docs/` | 哪些小节能指向现成文件，链接目标是否真实存在 |
| 清单文件：`package.json`、`pyproject.toml`、`Cargo.toml`、`go.mod`、`pom.xml`、`*.csproj`、`Gemfile`、`composer.json` | 包名、运行时版本、依赖、可执行的入口 |
| `scripts` 段与 `Makefile` / `justfile` | 安装、构建、测试、运行的真实命令 |
| `.github/workflows/` | CI 实际跑的命令与平台矩阵，用来核对命令真能跑 |
| `git remote` | 仓库 URL 与宿主，徽章、clone 地址、issue 入口的来源 |

顶层目录树指被审计目录的一级成员；子包路径下同法取证。

清单查不到的事实——对外联系人、维护状态意图、是否对外发布——列成问题问人；问到之前保持空着。

完成判据：清单六项各自留下证据。

## 审计

按 `assets/README-template.md` 的骨架顺序逐节对照证据，报告的排序与骨架一致。报告直接回在对话里，不写磁盘。

每个小节给一个现状：

- **有**：小节在，内容与证据一致。
- **缺**：整节不在。
- **不准确**：小节在，但与证据矛盾、过期，或只剩占位符。

条件小节因项目里没有对应对象而不出现时，写「不适用」，并写出缺的条件。

证据落到文件路径加行号，或一条命令加输出；查不到就写「无」。

完成判据：六个必写节各有一行现状和一条证据；每个条件节要么给出结论，要么写明不适用的理由。

## 落笔

按 `assets/README-template.md` 的骨架写英文草稿，每节怎么写由 `references/readme-spec.md` 定；事实只取探查留下的证据。

已有 README：判为「保留」的小节原样沿用；「改写」「新增」「删除」各自对上审计里的一条，逐条落实。没有 README：按骨架写整份草稿。

草稿先贴进对话，标明哪些小节新写、哪些沿用，以及待确认问题怎么处理，等用户确认。用户确认之后才写磁盘，一次写入被审计目录的 `README.md`。

标题层级即导航：正文里不写目录，链接与图片路径按 `references/github-mechanics.md` 的规则落笔。

完成判据：用户确认过草稿，磁盘上的 `README.md` 与确认稿逐节一致、与骨架的 H2 顺序一致。

## 校验

机械项交给脚本：

```bash
python ~/.agents/skills/write-readme/scripts/check-readme.py <target>
```

`<target>` 是被审计目录或它的 `README.md`，缺省 `.`。本 skill 装在消费目录 `~/.agents/skills/write-readme`，脚本固定在那里；在本仓库里改 skill 时，同一文件是 `skills/write-readme/scripts/check-readme.py`。脚本判什么、退出码各代表什么，以它文件头的说明为准。

脚本只判机械项。写完的 README 再过一遍语义自检，每条都对着最终稿确认：

- 模板里的 `<...>` 槽位、注释和「暂无」这类占位都已换成真实内容。
- `Status` 一行写明维护中、实验性还是已弃用，与探查到的证据一致。
- 每条命令都能照抄运行，与清单文件、`Makefile` / `justfile`、CI 里的一致。
- 全文是英文；命令、包名、路径、环境变量保持仓库里的原样。
- 每个必写小节的标题下都有真实内容，不是空行，也不是一句指向别处的说明。

完成判据：脚本退出码 0，且上面五条自检全部通过。任一条不过就不算交付。

## 参考资料

- `assets/README-template.md`：固定骨架，顺序与条件小节的位置都以它为准；落笔时照它填。
- `references/readme-spec.md`：每节必须回答什么、素材从哪来、反例，以及条件小节的触发条件；写草稿前读。
- `references/audit-report.md`：报告的四列、动作词与一份按本骨架填好的范例；写报告前读。
- `references/github-mechanics.md`：GitHub 对 README 的文件名、位置、体积、Outline、锚点与链接的处理，以及每条处理的写作后果；写草稿和校验前读。
- `scripts/check-readme.py`：机械校验脚本，「校验」里的命令就是它。
