#!/usr/bin/env python3
"""检查 README 是否满足 GitHub 的机械约束。

用法：python check-readme.py [PATH]
  PATH 是被审计目录（缺省为 .）：按 .github/、仓库根、docs/ 的优先级找 GitHub 会展示的那一份。
  PATH 是文件：直接检查该文件。
  路径不存在：退出码 2。

六类判据，每类可独立触发：
  1. file-location           文件名严格是 README.md，且位于 GitHub 会展示的位置。
  2. relative-link           相对链接、引用式链接、Markdown 图片与 <img src> 的目标在磁盘上存在；
                             跳过 http(s)、mailto、纯锚点和协议相对 URL。
  3. single-line-link-text   链接文本写在一行内。
  4. hand-written-toc        全文没有手写目录（标题后跟锚点列表项，或连续锚点列表项）。
  5. file-size               小于 500 KiB，超过会被 GitHub 截断。
  6. in-repo-absolute-url    没有指向本仓库已有文件的绝对 URL；这类链接换成相对链接即可。

边界：只判机械项。每节是否有真实内容、命令是否真能执行、许可证名是否与 LICENSE 一致，
这类语义判断不在本脚本范围内。6 号判据把 URL 的 owner/repo 与 git remote 的 origin 比对，
据此识别同仓链接；没有 origin 时改用被审计目录名，owner/repo 判断不出就跳过。不联网。

退出码：0 通过，1 有违规，2 环境或用法问题。
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote

MAX_BYTES = 500 * 1024
SURFACED_LOCATIONS = ((".github", ".github/"), (".", "仓库根目录"), ("docs", "docs/"))
TOC_TITLES = {"contents", "table of contents", "toc", "目录"}

FENCE_START = ("```", "~~~")
INLINE_CODE_RE = re.compile(r"`+[^`\n]*`+")
LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)]*)\)")
REF_LINK_RE = re.compile(r"(!?)\[([^\]]*)\]\[([^\]]*)\]")
REF_DEFINITION_RE = re.compile(r"^\s{0,3}\[([^\]]+)\]:\s*(.*?)\s*$")
IMG_SRC_RE = re.compile(
    r"<img\b[^>]*?\bsrc\s*=\s*(?:\"([^\"]*)\"|'([^']*)'|([^\s>]+))",
    re.IGNORECASE,
)
HEADING_RE = re.compile(r"^\s{0,3}(#{1,6})\s+(.*?)\s*#*\s*$")
ANCHOR_ITEM_RE = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+\[[^\]]+\]\(\s*#[^)\s]*\s*\)\s*$")
SCHEME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")
GITHUB_URL_RE = re.compile(
    r"^https?://(?:www\.)?github\.com/([^/]+)/([^/]+)/(?:blob|tree|raw)/[^/]+/(.+)$",
    re.IGNORECASE,
)
RAW_URL_RE = re.compile(
    r"^https?://raw\.githubusercontent\.com/([^/]+)/([^/]+)/[^/]+/(.+)$",
    re.IGNORECASE,
)
REMOTE_RE = re.compile(
    r"github\.com[:/]([^/]+)/([^/]+?)(?:\.git)?/?$",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class Violation:
    check: str
    line: int | None
    message: str


def ensure_utf8_streams() -> None:
    """输出被管道捕获时改用 UTF-8，避免 Windows 控制台代码页把中文变成乱码。"""
    for stream in (sys.stdout, sys.stderr):
        try:
            if not stream.isatty():
                stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):  # pragma: no cover - 老解释器或已关闭的流
            pass


def find_readme(directory: Path) -> tuple[Path | None, str]:
    """返回 (README 路径, 位置说明)，按 GitHub 的展示优先级查找。

    GitHub 在 .github/、仓库根、docs/ 三处找 README；三处都有时 .github/ 胜出。
    只认 README.md，大小写或扩展名不对的文件也返回，好让 file-location 报出具体文件名。
    逐个读目录项而不是直接拼 README.md，因为 Windows 文件系统大小写不敏感。
    """
    for relative, label in SURFACED_LOCATIONS:
        location = directory / relative
        if not location.is_dir():
            continue
        try:
            files = sorted(path for path in location.iterdir() if path.is_file())
        except OSError:
            continue
        exact = [path for path in files if path.name == "README.md"]
        if exact:
            return exact[0], label
        matches = [path for path in files if path.name.casefold().startswith("readme")]
        if matches:
            return matches[0], label
    return None, ""


def mask_code(text: str) -> str:
    """把代码块和行内代码替换成空格，保留换行与字符偏移；行号因此仍然对得上。"""
    chars = list(text)
    fence: str | None = None
    offset = 0
    for line in text.splitlines(keepends=True):
        body = line.rstrip("\r\n")
        stripped = body.lstrip()
        marker = stripped[:3] if stripped.startswith(FENCE_START) else None
        if fence is not None or marker is not None:
            mask_range(chars, offset, offset + len(line))
            if fence is None:
                fence = marker
            elif marker is not None and stripped.startswith(fence):
                fence = None
        else:
            for match in INLINE_CODE_RE.finditer(body):
                mask_range(chars, offset + match.start(), offset + match.end())
        offset += len(line)
    return "".join(chars)


def mask_range(chars: list[str], start: int, end: int) -> None:
    for index in range(start, end):
        if chars[index] not in "\r\n":
            chars[index] = " "


def line_at(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def normalize_target(raw: str) -> str:
    """从 (...) 里取出目标，去掉 Markdown 标题和尖括号。"""
    raw = raw.strip()
    if not raw:
        return ""
    if raw.startswith("<"):
        end = raw.find(">")
        if end != -1:
            return raw[1:end].strip()
    return raw.split()[0]


def strip_fragment(target: str) -> str:
    """去掉 #锚点 和 ?查询串，只留文件路径。"""
    return target.split("#", 1)[0].split("?", 1)[0]


def is_external(target: str) -> bool:
    """http(s)、mailto、其他 scheme、纯锚点、协议相对 URL 都不按相对路径检查。"""
    if target.startswith(("#", "//")):
        return True
    return bool(SCHEME_RE.match(target))


def github_url_target(target: str) -> tuple[str, str, str] | None:
    """拆出 GitHub 绝对 URL 的 (owner, repo, 仓库内路径)；不是这类 URL 时返回 None。"""
    clean = strip_fragment(target)
    for pattern in (GITHUB_URL_RE, RAW_URL_RE):
        match = pattern.match(clean)
        if match:
            owner = match.group(1).casefold()
            repo = match.group(2).casefold()
            if repo.endswith(".git"):
                repo = repo[:-4]
            return owner, repo, unquote(match.group(3)).strip("/")
    return None


def find_git_root(start: Path) -> Path | None:
    """向上找最近的含 .git 的目录，作为仓库根。"""
    current = start.resolve()
    while True:
        if (current / ".git").exists():
            return current
        if current.parent == current:
            return None
        current = current.parent


def read_remote_url(git_root: Path) -> str | None:
    """读 origin 的 URL；没有 git、没有 origin 或命令失败时返回 None。"""
    try:
        completed = subprocess.run(
            ["git", "-C", str(git_root), "config", "--get", "remote.origin.url"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if completed.returncode != 0:
        return None
    return completed.stdout.strip() or None


def parse_remote_identity(url: str) -> tuple[str, str] | None:
    """从 remote URL 解析 github.com 的 (owner, repo)；非 GitHub 远端返回 None。"""
    match = REMOTE_RE.search(url)
    if not match:
        return None
    repo = match.group(2).casefold()
    if repo.endswith(".git"):
        repo = repo[:-4]
    return match.group(1).casefold(), repo


def repository_context(audited_root: Path) -> tuple[Path, tuple[str | None, str] | None]:
    """返回 (仓库根, 身份)。

    身份是 (owner, repo)；没有远端时 owner 为 None、repo 取被审计目录名。
    owner/repo 判断不出（例如远端不是 GitHub）时身份为 None，6 号判据跳过。
    """
    git_root = find_git_root(audited_root)
    if git_root is None:
        return audited_root, (None, audited_root.name.casefold())

    remote = read_remote_url(git_root)
    if remote is None:
        return git_root, (None, audited_root.name.casefold())
    return git_root, parse_remote_identity(remote)


def check_name(readme: Path, root: Path) -> list[Violation]:
    violations: list[Violation] = []
    if readme.name != "README.md":
        violations.append(
            Violation(
                "file-location",
                1,
                f"文件名必须是 README.md（大小写敏感），实际是 {readme.name}",
            )
        )
        return violations
    parent = readme.parent
    if parent == root or parent.name in {".github", "docs"}:
        return violations
    violations.append(
        Violation(
            "file-location",
            1,
            "README.md 不在 GitHub 展示的位置：仓库根目录、.github/ 或 docs/",
        )
    )
    return violations


def normalize_label(label: str) -> str:
    return re.sub(r"\s+", " ", label).strip().casefold()


def collect_reference_definitions(masked: str) -> dict[str, str]:
    """收集 `[ref]: path` 形式的链接定义。"""
    definitions: dict[str, str] = {}
    for line in masked.splitlines():
        match = REF_DEFINITION_RE.match(line)
        if not match:
            continue
        label = normalize_label(match.group(1))
        target = normalize_target(match.group(2))
        if label and target:
            definitions.setdefault(label, target)
    return definitions


def check_target(
    target: str,
    line: int,
    readme: Path,
    repo_root: Path,
    identity: tuple[str | None, str] | None,
    violations: list[Violation],
) -> None:
    """检查一条链接目标：外链判同仓绝对 URL，其余按相对路径落盘检查。"""
    if is_external(target):
        if identity is None:
            return
        parsed = github_url_target(target)
        if parsed is None:
            return
        owner, repo, repo_path = parsed
        identity_owner, identity_repo = identity
        if repo != identity_repo:
            return
        if identity_owner is not None and owner != identity_owner:
            return
        if repo_path and (repo_root / repo_path).exists():
            violations.append(
                Violation(
                    "in-repo-absolute-url",
                    line,
                    f"绝对 URL 指向本仓库已有文件：{target}；改用相对链接",
                )
            )
        return

    path_part = strip_fragment(target)
    if not path_part:
        return
    path_part = unquote(path_part)
    if path_part.startswith("/"):
        resolved = repo_root / path_part.lstrip("/")
    else:
        resolved = readme.parent / path_part
    if not resolved.exists():
        violations.append(
            Violation("relative-link", line, f"相对链接目标不存在：{target}")
        )


def check_single_line(line: int, text: str, violations: list[Violation]) -> None:
    if "\n" in text:
        violations.append(
            Violation(
                "single-line-link-text",
                line,
                "链接文本跨行；链接文本要写在一行内",
            )
        )


def check_links(
    readme: Path,
    repo_root: Path,
    identity: tuple[str | None, str] | None,
    masked: str,
) -> list[Violation]:
    violations: list[Violation] = []

    for match in LINK_RE.finditer(masked):
        line = line_at(masked, match.start())
        target = normalize_target(match.group(2))
        if not target:
            continue
        check_single_line(line, match.group(1), violations)
        check_target(target, line, readme, repo_root, identity, violations)

    definitions = collect_reference_definitions(masked)
    for match in REF_LINK_RE.finditer(masked):
        line = line_at(masked, match.start())
        text = match.group(2)
        label = normalize_label(match.group(3) or text)
        check_single_line(line, text, violations)
        target = definitions.get(label)
        if target is None:
            violations.append(
                Violation(
                    "relative-link",
                    line,
                    f"引用式链接没有对应的定义：[{match.group(3).strip() or text.strip()}]",
                )
            )
            continue
        check_target(target, line, readme, repo_root, identity, violations)

    for match in IMG_SRC_RE.finditer(masked):
        target = next(group for group in match.groups() if group is not None)
        if not target.strip():
            continue
        check_target(
            normalize_target(target),
            line_at(masked, match.start()),
            readme,
            repo_root,
            identity,
            violations,
        )

    return violations


def is_toc_title(text: str) -> bool:
    normalized = re.sub(r"[`*_]", "", text).strip().rstrip("#").strip().casefold()
    normalized = re.sub(r"\s+", " ", normalized)
    return normalized in TOC_TITLES


def check_toc(masked: str) -> list[Violation]:
    lines = masked.splitlines()

    for index, line in enumerate(lines):
        match = HEADING_RE.match(line)
        if not match or not is_toc_title(match.group(2)):
            continue
        for following in lines[index + 1 :]:
            if not following.strip():
                continue
            if ANCHOR_ITEM_RE.match(following):
                return [
                    Violation(
                        "hand-written-toc",
                        index + 1,
                        f"手写目录：标题 {match.group(2).strip()!r} 重复了 GitHub 自动生成的 Outline",
                    )
                ]
            break

    run_start: int | None = None
    run_length = 0
    for number, line in enumerate(lines, start=1):
        if ANCHOR_ITEM_RE.match(line):
            if run_start is None:
                run_start = number
            run_length += 1
            continue
        if run_length >= 2:
            return [
                Violation(
                    "hand-written-toc",
                    run_start,
                    f"手写目录：{run_length} 个锚点列表项，GitHub 会按标题自动生成 Outline",
                )
            ]
        run_start = None
        run_length = 0
    if run_length >= 2 and run_start is not None:
        return [
            Violation(
                "hand-written-toc",
                run_start,
                f"手写目录：{run_length} 个锚点列表项，GitHub 会按标题自动生成 Outline",
            )
        ]
    return []


def check_size(readme: Path) -> list[Violation]:
    size = readme.stat().st_size
    if size <= MAX_BYTES:
        return []
    return [
        Violation(
            "file-size",
            1,
            f"文件 {size} 字节（{size / 1024:.1f} KiB），超过 500 KiB 会被 GitHub 截断",
        )
    ]


def path_label(readme: Path, root: Path) -> str:
    parent = readme.parent
    if parent == root:
        return "仓库根目录"
    if parent.name in {".github", "docs"}:
        return f"{parent.name}/"
    return str(parent)


def display_path(readme: Path, root: Path) -> str:
    try:
        return readme.relative_to(root).as_posix()
    except ValueError:
        return str(readme)


def main(argv: list[str] | None = None) -> int:
    ensure_utf8_streams()

    parser = argparse.ArgumentParser(description="检查 README 的机械约束")
    parser.add_argument(
        "path", nargs="?", default=".", help="被审计目录（缺省 .）或 README 文件"
    )
    args = parser.parse_args(argv)
    argument = Path(args.path)

    if not argument.exists():
        print(f"找不到路径：{argument}", file=sys.stderr)
        return 2

    if argument.is_dir():
        root = argument.resolve()
        readme, label = find_readme(root)
        if readme is None:
            print(f"README：未找到（{root}）")
            print(
                f"{root}:1: file-location: 没有 README.md；"
                "GitHub 会展示的位置是 .github/、仓库根目录、docs/"
            )
            print("\n1 个违规。")
            return 1
        display = display_path(readme, root)
    elif argument.is_file():
        readme = argument.resolve()
        parent = readme.parent
        root = parent.parent if parent.name in {".github", "docs"} else parent
        label = path_label(readme, root)
        display = display_path(readme, root)
    else:
        print(f"路径既不是文件也不是目录：{argument}", file=sys.stderr)
        return 2

    try:
        text = readme.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        print(f"读取失败：{readme}：{exc}", file=sys.stderr)
        return 2

    print(f"README：{display}（{label}）")

    repo_root, identity = repository_context(root)
    masked = mask_code(text)
    violations = (
        check_name(readme, root)
        + check_links(readme, repo_root, identity, masked)
        + check_toc(masked)
        + check_size(readme)
    )

    for violation in violations:
        location = display if violation.line is None else f"{display}:{violation.line}"
        print(f"{location}: {violation.check}: {violation.message}")

    print(f"\n{len(violations)} 个违规。")
    if violations:
        return 1
    print("检查通过。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
