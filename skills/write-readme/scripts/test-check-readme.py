#!/usr/bin/env python3
"""用 fixture 验证 check-readme.py 的外部行为：退出码与点名的违规项。

每个 fixture 是一个最小样本；测试只从命令行调用被测脚本，不 import 其内部函数。
oversized 一例在临时目录里把样本重复到 500 KiB 以上，仓库里不存大文件。

退出码：0 全部通过，1 有失败。
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHECKER = HERE / "check-readme.py"
FIXTURES = HERE / "fixtures"
MAX_BYTES = 500 * 1024
FILLER = "This line exists only to push the fixture past 500 KiB.\n"


def ensure_utf8_streams() -> None:
    """输出被管道捕获时改用 UTF-8，避免 Windows 控制台代码页把被检查脚本的输出弄成乱码。"""
    for stream in (sys.stdout, sys.stderr):
        try:
            if not stream.isatty():
                stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):  # pragma: no cover - 老解释器或已关闭的流
            pass


@dataclass
class Case:
    name: str
    target: Path | None
    expected_code: int
    expected_check: str | None = None
    cwd: Path | None = None


def run_checker(case: Case) -> tuple[int, str]:
    command = [sys.executable, str(CHECKER)]
    if case.target is not None:
        command.append(str(case.target))
    completed = subprocess.run(
        command,
        cwd=case.cwd or HERE,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=60,
    )
    return completed.returncode, (completed.stdout or "") + (completed.stderr or "")


def check_case(case: Case) -> bool:
    expected = f"exit {case.expected_code}"
    if case.expected_check is not None:
        expected += f" with {case.expected_check!r}"
    try:
        code, output = run_checker(case)
    except (OSError, subprocess.TimeoutExpired) as exc:
        print(f"FAIL  {case.name}: expected {expected}; actual could not run: {exc}")
        return False

    matched = code == case.expected_code and (
        case.expected_check is None or case.expected_check in output
    )
    if matched:
        print(f"PASS  {case.name}: expected {expected}; actual exit {code}")
        return True

    actual = f"exit {code}"
    if case.expected_check is not None and case.expected_check not in output:
        actual += f", but {case.expected_check!r} is missing from the output"
    print(f"FAIL  {case.name}: expected {expected}; actual {actual}")
    for line in output.splitlines():
        print(f"      | {line}")
    return False


def main() -> int:
    ensure_utf8_streams()

    cases = [
        Case("clean-directory", FIXTURES / "clean", 0),
        Case("clean-file", FIXTURES / "clean" / "README.md", 0),
        Case("default-path", None, 0, cwd=FIXTURES / "clean"),
        Case("missing-readme", FIXTURES / "missing", 1, "file-location"),
        Case("wrong-name", FIXTURES / "wrong-name", 1, "file-location"),
        Case("broken-link", FIXTURES / "broken-link", 1, "relative-link"),
        Case(
            "multiline-link-text",
            FIXTURES / "multiline-link-text",
            1,
            "single-line-link-text",
        ),
        Case("hand-written-toc", FIXTURES / "toc", 1, "hand-written-toc"),
        Case("absolute-in-repo-url", FIXTURES / "absolute-url", 1, "in-repo-absolute-url"),
        Case("missing-path", FIXTURES / "does-not-exist", 2),
    ]

    results = [check_case(case) for case in cases]

    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp)
        base = (FIXTURES / "oversized" / "README.md").read_text(encoding="utf-8")
        repeats = MAX_BYTES // len(FILLER) + 100
        (target / "README.md").write_text(base + "\n" + FILLER * repeats, encoding="utf-8")
        results.append(check_case(Case("oversized", target, 1, "file-size")))

    passed = sum(results)
    failed = len(results) - passed
    print(f"\n{len(results)} cases, {passed} passed, {failed} failed.")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
