#!/usr/bin/env python3
"""检查 workline 任务输出的完整性和真实性。

用法:
  python scripts/check_workline_outputs.py <任务目录>

检查项:
  1. 4 份报告是否存在
  2. TestReport 是否包含真实命令输出
  3. metrics.yaml 是否存在且包含三段式字段
  4. ChangedFiles 是否列出修改文件
  5. 是否疑似伪造测试结果
"""

import os
import sys
import yaml

REQUIRED_REPORTS = ["REVIEW.md", "ChangedFiles.md", "TestReport.md", "RiskReport.md"]
REQUIRED_METRICS = "metrics.yaml"

FAKE_SIGNALS = [
    # TestReport 声称通过但没有命令输出
    ("通过", "未执行"),
    ("0 GC", "未执行"),
    ("passed", "UNVERIFIED"),
]


def check_reports(task_dir):
    issues = []
    for report in REQUIRED_REPORTS:
        path = os.path.join(task_dir, report)
        if not os.path.exists(path):
            issues.append(f"MISSING: {report}")

        if "TestReport" in report and os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
                if "```" not in content:
                    issues.append(f"SUSPICIOUS: TestReport.md has no code blocks — likely no real output")

                for claim, flag in FAKE_SIGNALS:
                    if claim in content and flag in content:
                        issues.append(f"SUSPICIOUS: TestReport claims '{claim}' but marks '{flag}' — possible fake")

        if "ChangedFiles" in report and os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
                if "|---" not in content:
                    issues.append(f"WEAK: ChangedFiles.md has no table — likely no file list")

    return issues


def check_metrics(task_dir):
    issues = []
    for f in os.listdir(task_dir):
        if f.endswith("metrics.yaml") or f.endswith("metrics.yml"):
            path = os.path.join(task_dir, f)
            with open(path, "r", encoding="utf-8") as fh:
                data = yaml.safe_load(fh)

            required_sections = ["agent_reported", "mentor_verified", "evidence"]
            if isinstance(data, dict):
                for section in required_sections:
                    if section not in data:
                        issues.append(f"MISSING: metrics.yaml lacks '{section}' section")
                    elif section == "mentor_verified" and all(v is False or v is None for v in data[section].values()):
                        issues.append(f"WEAK: mentor_verified section is all false/null — no Mentor signoff")
            break
    else:
        issues.append("MISSING: no metrics.yaml found")

    return issues


def main():
    if len(sys.argv) < 2:
        print("Usage: python check_workline_outputs.py <task_dir>")
        sys.exit(1)

    task_dir = sys.argv[1]
    all_issues = []

    all_issues.extend(check_reports(task_dir))
    all_issues.extend(check_metrics(task_dir))

    if all_issues:
        print(f"ISSUES ({len(all_issues)}):")
        for i in all_issues:
            print(f"  - {i}")
        sys.exit(1)
    else:
        print("ALL CHECKS PASSED")
        sys.exit(0)


if __name__ == "__main__":
    main()
