# README 小节规范

骨架只有一份：`assets/README-template.md`。这份文件不重复它，按骨架顺序逐节写：这节必须回答什么、事实取自哪些探查项、写成什么样算坏。

全篇适用的三条：

- 不适用的条件小节整节省略：标题、正文、注释一起删，不留空标题，也不留「暂无」「TBD」这类占位。
- 仓库内的链接用相对路径，链接文本写在一行内。
- 产出英文；命令、包名、路径、环境变量保持仓库里的原样。

## 标题与开篇

- **必须回答**：这是什么、给谁用、为什么有用。两三句之内让第一次访问的人决定要不要往下读。
- **素材**：顶层目录树（模块划分与语言）；清单文件里的 `name`、`description`；已有 README 的首段，仍然准确才沿用。
- **反例**：

```markdown
# utils

A collection of useful utilities.
```

项目名是目录名，一句话换成任何仓库都成立。读者看完仍不知道它解决什么问题。

## 徽章

- **触发**：项目发布到包管理器（npm、PyPI、crates.io 等）、有可展示的 CI 状态、或接了覆盖率与下载量服务。三者都没有，这一行整行不出现。
- **必须回答**：一行之内给出可核验的当前状态，每个徽章都链接到它的来源。
- **素材**：`git remote`（owner/repo 与宿主）；清单文件（包名）；`.github/workflows/`（工作流名与分支）。
- **反例**：

```markdown
![build passing](https://img.shields.io/badge/build-passing-brightgreen)
```

文本写死的假徽章，不连任何工作流：构建红了它照旧显示通过，读者据此判断项目可用，与事实相反。

## 截图与演示

- **触发**：项目有可看的界面——图形界面，或值得展示的终端输出。纯库、纯脚本不写这一行。
- **必须回答**：一张图或一段终端录制，让读者知道用起来是什么样；图片走仓库内相对路径，配一行说明。
- **素材**：顶层目录树里的图片目录；已有 README 里的截图路径；`docs/` 里的截图。
- **反例**：

```markdown
![demo](screenshots/demo.gif)
```

`screenshots/` 不在仓库里，渲染出来是裂图，读者只看到替代文本，比没有还差。

## Status

- **必须回答**：一行说清维护状态——维护中、实验性、还是已弃用。读者据此判断能不能依赖它。
- **素材**：维护意图不在探查清单里，问人；已有 README 里仍然准确的一行可以沿用。
- **反例**：

```markdown
## Status

TBD
```

占位符，读者仍然不知道现在能不能用；写成 `Coming soon` 也一样。

## Getting started

- **必须回答**：前置要求（运行时与版本）、安装、构建、运行，按读者动手的顺序排列，每条命令照抄可用。
- **素材**：清单文件（运行时版本、依赖、`engines`）；`scripts` 段与 `Makefile` / `justfile`；`.github/workflows/`（CI 里跑通的命令与平台矩阵）；顶层目录树。
- **反例**：

````markdown
## Getting started

```bash
npm install
npm start
```
````

没写 Node 版本，也没写要先 `npm run build`；读者在旧版本运行时上装完就卡在第一步，README 承诺的「照抄可用」当场失效。

## Usage

- **必须回答**：一个能跑的示例——代码或命令——加上它的预期输出。照抄能得到同样结果。
- **素材**：清单文件里的入口（`bin`、`main`、`exports`）与 `scripts` 段；`.github/workflows/` 里实际调用过的命令；已有 README 里验证过能跑的例子。
- **反例**：

```markdown
## Usage

Call `validate(path, options)` to check a skill directory.
```

只有签名，没有调用，也没有输出。读者不知道传什么进去、返回什么算成功。

## Configuration

- **触发**：项目从环境变量、配置文件或命令行参数读设置，且这些值可以由使用者改。没有可改项就整节省略。
- **必须回答**：每个可配置项的名字、含义、默认值、一个取值示例；凭据类写清从哪来，不写进仓库。
- **素材**：源码里读取环境变量或配置的位置；配置示例文件（`.env.example`、`config.example.*`）；清单文件的配置字段；`scripts` 段。
- **反例**：

```markdown
## Configuration

| Name | Meaning |
|---|---|
| see source | see source |
```

一张把读者推回源码的表格；三个配置项里两个默认值写 `N/A` 同样是写坏了。

## Architecture

- **触发**：项目由两个以上模块或包组成，目录结构本身能帮读者理解它。单文件、单脚本项目整节省略。
- **必须回答**：有几块、每块负责什么、依赖往哪个方向流；需要时配一棵只列关键目录的树。
- **素材**：顶层目录树；清单文件的 workspaces 与 packages 字段；入口文件的位置。
- **反例**：

````markdown
## Architecture

```text
├── .github/workflows/validate.yml   # CI
├── AGENTS.md                        # agent notes
├── CONTRIBUTING.md                  # contribution guide
... one line per file, forty more
```
````

把 `git ls-tree -r` 的输出整段贴进来，每个文件一行注释。几十行读完，读者仍不知道模块之间怎么调用。

## Documentation

- **触发**：仓库有独立文档——`docs/` 目录、wiki、或外部站点。三者都没有就整节省略，不写空的 Documentation 节。
- **必须回答**：给出入口链接，每个链接一行说明它覆盖什么。
- **素材**：`docs/` 是否存在及其一级文件；`git remote` 推出的 wiki 地址；已有 README 里的文档链接。
- **反例**：

```markdown
## Documentation

See the docs.
```

`docs/` 明明在仓库里，却不给链接；或者把链接写成 `https://github.com/owner/repo/blob/main/docs/x.md`——clone 到本地或仓库改名之后断掉，应该用相对路径。

## Getting help

- **必须回答**：卡住时去哪问——issue 区、讨论区、或维护者联系方式，给可直接点的链接。
- **素材**：`git remote`（GitHub Issues 地址）；`CONTRIBUTING.md` 里的联系渠道；人问出来的联系人。
- **反例**：

```markdown
## Getting help

Feel free to reach out.
```

没有渠道，没有地址，读者只能自己猜；指向一个已经关闭的 issue 区是同一个错。

## Contributing

- **必须回答**：贡献入口指向 `CONTRIBUTING.md`，并用一两句说清 PR 流程——从哪开分支、合并前要过什么、描述写什么。
- **素材**：`CONTRIBUTING.md` 是否存在及其实质内容；`.github/workflows/`（合并前跑的检查）；`.github/pull_request_template.md`。
- **反例**：

```markdown
## Contributing

PRs welcome.
```

读者不知道从哪开分支、合并前要过什么，也没拿到 `CONTRIBUTING.md` 的入口；把整份 `CONTRIBUTING.md` 复制进来，是同一个错的两个方向。

## License

- **必须回答**：许可证名，加一个指向 `LICENSE` 的相对链接。
- **素材**：`LICENSE` 是否存在、首行写的是什么；清单文件的 license 字段。
- **反例**：

```markdown
## License

See LICENSE.
```

不给许可证名，读者得自己打开文件辨认；写 `MIT` 但仓库里没有 `LICENSE` 文件，则是另一种写坏。

## 尾部小节

- **触发**：有需要点名致谢的人或项目、有相关或后继项目、或仓库带 `CITATION.cff`。每条触发只开对应的小节，一条都不成立就整节省略。
- **必须回答**：致谢给出名字和它做了什么；相关项目给链接和与它的关系；引用给一段可直接粘贴的 BibTeX 或引用格式。
- **素材**：`CITATION.cff`；`docs/` 里的引用说明；已有 README；人名和出处问人。
- **反例**：

```markdown
## Acknowledgements

Thanks to everyone who contributed.
```

没有一个名字，读者无法跟进，也不构成致谢。
