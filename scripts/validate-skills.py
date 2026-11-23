#!/usr/bin/env python3
"""校验 skills/ 下每个 skill 的结构与文件引用。

硬失败 5 条：
  1. frontmatter 能被 YAML 解析
  2. name 存在，且等于目录名
  3. name 匹配 ^[a-z0-9-]{1,64}$
  4. description 存在，且不超过 1024 字符
  5. 正文里的 references/、scripts/、assets/ 相对路径真实存在

其余问题只告警。退出码：0 通过，1 有硬失败，2 环境问题。
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover - 环境缺失时给出可执行的下一步
    print("缺少 PyYAML。运行：python -m pip install pyyaml", file=sys.stderr)
    sys.exit(2)

NAME_RE = re.compile(r"^[a-z0-9-]{1,64}$")
REF_RE = re.compile(r"(?:references|scripts|assets)/[A-Za-z0-9._/#-]+")
FENCE_RE = re.compile(r"```.*?```", re.S)

MAX_DESCRIPTION = 1024
MIN_DESCRIPTION_WARN = 20
MAX_BODY_LINES_WARN = 500
TRAILING = ".,;:、。）)]}"


class Findings:
    """按 skill 收集错误和告警，最后统一打印。"""

    def __init__(self) -> None:
        self.errors: list[tuple[str, str]] = []
        self.warnings: list[tuple[str, str]] = []

    def error(self, where: str, message: str) -> None:
        self.errors.append((where, message))

    def warn(self, where: str, message: str) -> None:
        self.warnings.append((where, message))


def split_frontmatter(text: str) -> tuple[dict | None, str, str | None]:
    """返回 (frontmatter, body, 错误信息)。"""
    if not text.startswith("---"):
        return None, text, "文件开头没有 frontmatter 分隔符 ---"

    lines = text.splitlines()
    end = None
    for index in range(1, len(lines)):
        if lines[index].strip() in {"---", "..."}:
            end = index
            break
    if end is None:
        return None, text, "frontmatter 没有结束分隔符 ---"

    raw = "\n".join(lines[1:end])
    body = "\n".join(lines[end + 1 :])

    try:
        data = yaml.safe_load(raw)
    except yaml.YAMLError as exc:
        return None, body, f"frontmatter 不是合法 YAML：{exc}"

    if data is None:
        data = {}
    if not isinstance(data, dict):
        return None, body, "frontmatter 必须是键值对"
    return data, body, None


def check_references(skill_dir: Path, body: str, where: str, findings: Findings) -> None:
    scan = FENCE_RE.sub("", body)
    seen: set[str] = set()
    for match in REF_RE.finditer(scan):
        ref = match.group(0).rstrip(TRAILING)
        if ref in seen:
            continue
        seen.add(ref)
        if not (skill_dir / ref).exists():
            findings.error(where, f"引用了不存在的路径：{ref}")


def check_skill(skill_dir: Path, findings: Findings) -> None:
    where = skill_dir.name
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.is_file():
        findings.error(where, "缺少 SKILL.md")
        return

    text = skill_file.read_text(encoding="utf-8")
    data, body, problem = split_frontmatter(text)
    if problem is not None or data is None:
        findings.error(where, problem or "frontmatter 解析失败")
        return

    name = data.get("name")
    if not isinstance(name, str) or not name.strip():
        findings.error(where, "frontmatter 缺少 name")
    else:
        if name != skill_dir.name:
            findings.error(where, f"name 是 {name!r}，与目录名 {skill_dir.name!r} 不一致")
        if not NAME_RE.match(name):
            findings.error(where, "name 只允许小写字母、数字和连字符，最长 64 字符")

    description = data.get("description")
    if not isinstance(description, str) or not description.strip():
        findings.error(where, "frontmatter 缺少 description")
    else:
        length = len(description)
        if length > MAX_DESCRIPTION:
            findings.error(where, f"description 有 {length} 字符，超过 {MAX_DESCRIPTION}")
        elif length < MIN_DESCRIPTION_WARN:
            findings.warn(where, f"description 只有 {length} 字符，可能触发不到")

    metadata = data.get("metadata")
    if not isinstance(metadata, dict):
        findings.warn(where, "缺少 metadata 块（version / tags）")
    else:
        if not metadata.get("version"):
            findings.warn(where, "metadata 缺少 version")
        if not metadata.get("tags"):
            findings.warn(where, "metadata 缺少 tags")

    if not any(line.startswith("## ") for line in body.splitlines()):
        findings.warn(where, "正文没有二级标题")

    body_lines = len(body.splitlines())
    if body_lines > MAX_BODY_LINES_WARN:
        findings.warn(where, f"正文 {body_lines} 行，考虑把资料移到 references/")

    check_references(skill_dir, body, where, findings)


def ensure_utf8_streams() -> None:
    """输出被管道捕获时改用 UTF-8，避免 Windows 控制台代码页把中文变成乱码。"""
    for stream in (sys.stdout, sys.stderr):
        try:
            if not stream.isatty():
                stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):  # pragma: no cover - 老解释器或已关闭的流
            pass


def main(argv: list[str] | None = None) -> int:
    ensure_utf8_streams()

    parser = argparse.ArgumentParser(description="校验 skills/ 下的 skill 结构")
    parser.add_argument("--root", default=None, help="仓库根目录，默认取脚本所在目录的上级")
    parser.add_argument("--strict", action="store_true", help="把告警也当失败")
    args = parser.parse_args(argv)

    root = Path(args.root).resolve() if args.root else Path(__file__).resolve().parent.parent
    skills_dir = root / "skills"

    if not skills_dir.is_dir():
        print(f"找不到 skills/ 目录：{skills_dir}", file=sys.stderr)
        return 2

    skill_dirs = sorted(path for path in skills_dir.iterdir() if path.is_dir())
    if not skill_dirs:
        print("skills/ 里没有 skill，跳过校验。")
        return 0

    findings = Findings()
    for skill_dir in skill_dirs:
        check_skill(skill_dir, findings)

    for where, message in findings.errors:
        print(f"  ERROR  {where}: {message}")
    for where, message in findings.warnings:
        print(f"  WARN   {where}: {message}")

    failed = bool(findings.errors) or (args.strict and bool(findings.warnings))
    print(
        f"\n{len(skill_dirs)} 个 skill，"
        f"{len(findings.errors)} 个错误，{len(findings.warnings)} 个告警。"
    )
    if failed:
        print("校验未通过。")
        return 1
    print("校验通过。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
