# GitHub 平台机制

GitHub 怎么展示 README，决定了写作时把内容放在哪、链接怎么写、长度留多少余量。下面只记平台行为和对应的写作后果：每节写什么由 `references/readme-spec.md` 定，机械项由 `scripts/check-readme.py` 判。

## 文件名与位置

GitHub 只认文件名严格为 `README.md` 的文件：扩展名必须是 `.md`，大小写敏感。仓库首页展示的 README，GitHub 只在 `.github/`、仓库根目录、`docs/` 三处查找，优先级依次从高到低；三处都有 README 时，展示的是 `.github/` 那一份。浏览某个子目录时，GitHub 在文件列表下方渲染该目录自己的 `README.md`。

写作后果：

- 文件名写成 `Readme.md`、`README.MD`、`README` 都不渲染，改名是交付的一部分。
- 先按优先级确定要改的是哪一份：只更新了根目录的 README 而 `.github/README.md` 还在，读者看到的仍是旧内容。
- 代码包的 README 放代码包顶层；`docs/` 是 GitHub 的兜底查找位置，不是默认位置，挪进去会让它降到第三顺位。
- monorepo 的子包 README 只在浏览到该子包时出现，不会进仓库首页；先判断它写给谁看，再决定要不要套完整骨架。

## 500 KiB 截断

README 在 GitHub 页面上渲染时，超过 500 KiB 的内容会被截断，页面只显示前面的部分；磁盘上的文件不变。

写作后果：

- README 是入口，不是全量文档。接近 500 KiB 说明内容该拆到 `docs/` 或 wiki，而不是赌刚好不越界。
- 长表格、变更历史、完整 API 清单不占 README 的预算，换成指向它们的链接。

## Outline 按标题自动生成

GitHub 为仓库里任何 Markdown 文件（包括 README）的渲染页按其中的标题自动生成目录，README 页右上角的 Outline 图标展开它。

写作后果：

- 标题就是导航，H2 的顺序决定 Outline 的顺序；正文里再手写一份目录，只会和 Outline 重复。
- 标题写成能扫懂的名词短语；「更多」「其他」在 Outline 里不提供信息。
- 读者在 Outline 里看到的就是骨架：必写节一个不能少，条件节不成立就整节删掉，不在 Outline 里留空位。

## 章节锚点

每个带标题的小节都有 GitHub 自动生成的锚点；悬停标题会露出链接图标，点开就能拿到该锚点的地址，因此可以直接链接到某一节（`#锚点`）。

写作后果：

- 引用某一节时链接到它的标题，而不是行号；标题文字改了，指向旧锚点的链接就断了，被别处引用的小节标题保持稳定。
- 锚点由平台生成，正文里不用手写 `<a name>`。

## 相对链接与图片路径

相对链接以当前文件为基准解析，GitHub 按当前分支改写它，所以在哪个分支上都能点开。以 `/` 开头的路径相对仓库根，`./` 与 `../` 都可用。指向仓库内文件的绝对 URL（`https://github.com/owner/repo/blob/...`）不随分支、改名、fork 调整，克隆到本地后也点不开。

写作后果：

- 仓库内的文件一律用相对路径：同目录写 `name.md`，子目录写 `docs/name.md`，跨目录用 `../`。
- README 在 `docs/` 或子包目录时，`/` 开头的路径要从仓库根算起；按当前文件算相对路径更不容易错层。
- 图片走同一套解析规则；目标不存在时页面渲染成裂图，替代文本顶上来，比不放图更糟。
- 仓库外的资源用完整 URL，仓库内的一律相对。

## 链接文本单行

链接文本跨行时链接不成立：`[Contribution` 换行再写 `guidelines for this project](docs/CONTRIBUTING.md)`，GitHub 不会把它渲染成链接。

写作后果：

- 链接文字和 `](...)` 写在同一行；说明性长句放在链接外，链接文本保持短名词短语。
- 正文、列表、表格里的链接都受同一条约束。

## README 与 wiki 的边界

README 只承担让开发者开始使用和贡献这个项目所需的信息；更长的文档更适合放 wiki，仓库自己的 `docs/` 同理。Google 的最低要求是 README 至少给出一个指向用户文档的链接。

写作后果：

- 安装、运行、一个示例、求助入口、贡献入口留在 README；教程、设计文档、完整 API 表移出去。
- 有独立文档就给链接；没有就省略 Documentation 节，不为了凑节把长文塞回 README。

## Profile README

公开仓库的根目录 README，如果仓库名与用户名相同（`<username>/<username>`），会自动出现在个人主页上，并支持 GFM。

写作后果：

- 这种仓库的根 README 是个人主页内容，不是项目文档；套项目骨架会把主页改成安装说明。被审计目录命中它时，先确认读者是来看人还是看项目。

## 依据

- GitHub Docs, [About the repository README file](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)
- Google docguide, [READMEs](https://google.github.io/styleguide/docguide/READMEs.html)
