#!/usr/bin/env python3
"""v1.8-harness-check-minimal — check workline task completeness and consistency.

Requires:
  pip install -r requirements-dev.txt

Usage:
  python tools/check_workline_task.py --task <task-dir> --mode quick
  python tools/check_workline_task.py --task <task-dir> --mode full [--strict] [--report <path>]

Exit codes:
  0 = PASS
  1 = WARNING
  2 = BLOCKED
"""

import argparse
import os
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Missing dependency: PyYAML")
    print("Install with:")
    print("  pip install -r requirements-dev.txt")
    sys.exit(2)


# ── helpers ──────────────────────────────────────────────────────────

def _missing(path):
    return not os.path.exists(path)

def _load_yaml(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {}
    except Exception:
        return {}

def _status(ok):
    return "✅" if ok else "❌"


# ── report builder ───────────────────────────────────────────────────

class CheckReport:
    def __init__(self, task_id, mode):
        self.task_id = task_id
        self.mode = mode
        self.blocks = []
        self.warnings = []
        self.passes = []
        self.file_rows = []
        self.metric_rows = []
        self.scope_rows = []

    def file_check(self, name, path, required):
        exists = os.path.exists(path)
        row = f"| {name} | {'✅' if exists else '❌'} | {'BLOCKED' if required and not exists else 'OK'} |"
        self.file_rows.append(row)
        if required and not exists:
            self.blocks.append(f"Missing required file: {name}")
        elif not required and not exists:
            self.warnings.append(f"Missing optional file: {name}")
        else:
            self.passes.append(f"File present: {name}")
        return exists

    def metric_check(self, field, present):
        row = f"| {field} | {'✅' if present else '❌'} | {'BLOCKED' if not present else 'OK'} |"
        self.metric_rows.append(row)
        if not present:
            self.blocks.append(f"Missing metrics field: {field}")
        else:
            self.passes.append(f"Metrics field OK: {field}")

    def consistency_check(self, label, ok, severity="BLOCKED"):
        row = f"| {label} | {'✅' if ok else '❌'} | {severity if not ok else 'OK'} |"
        self.scope_rows.append(row)
        if not ok:
            if severity == "BLOCKED":
                self.blocks.append(label)
            else:
                self.warnings.append(label)
        else:
            self.passes.append(label)

    @property
    def result(self):
        if self.blocks:
            return "BLOCKED"
        if self.warnings:
            return "WARNING"
        return "PASS"

    @property
    def exit_code(self):
        return {"PASS": 0, "WARNING": 1, "BLOCKED": 2}[self.result]

    def write(self, path):
        report = []
        report.append("# Harness Check Report\n")
        report.append("## Summary\n")
        report.append(f"- task_id: {self.task_id}")
        report.append(f"- mode: {self.mode}")
        report.append(f"- result: **{self.result}**\n")

        report.append("## Required Files\n")
        report.append("| File | Status | Severity |")
        report.append("|---|---|---|")
        report.extend(self.file_rows)
        report.append("")

        report.append("## Metrics Check\n")
        report.append("| Field | Status | Severity |")
        report.append("|---|---|---|")
        report.extend(self.metric_rows)
        report.append("")

        report.append("## Scope Check\n")
        report.append("| Item | Status | Severity |")
        report.append("|---|---|---|")
        report.extend(self.scope_rows)
        report.append("")

        report.append("## Violations\n")
        if self.blocks:
            for b in self.blocks:
                report.append(f"- [BLOCKED] {b}")
        if self.warnings:
            for w in self.warnings:
                report.append(f"- [WARNING] {w}")
        if not self.blocks and not self.warnings:
            report.append("- None")
        report.append("")

        report.append("## Recommended Action\n")
        if self.blocks:
            report.append("- Fix BLOCKED items before proceeding.")
        elif self.warnings:
            report.append("- Review WARNING items; may proceed with caution.")
        else:
            report.append("- All checks passed. Task is compliant.")
        report.append("")

        with open(path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report))


# ── checkers ─────────────────────────────────────────────────────────

def check_quick(task_dir, strict=False):
    r = CheckReport(os.path.basename(task_dir), "quick")

    # files
    r.file_check("WorklineSummary.md", os.path.join(task_dir, "WorklineSummary.md"), True)
    r.file_check("metrics-lite.yaml", os.path.join(task_dir, "metrics-lite.yaml"), True)

    # metrics
    m = _load_yaml(os.path.join(task_dir, "metrics-lite.yaml"))
    for f in ["task_id", "mode", "result"]:
        r.metric_check(f, f in m)
    for f in ["changed_files", "build", "user_verified", "scope", "auto_upgrade"]:
        r.metric_check(f, f in m)
    build = m.get("build", {}) or {}
    scope = m.get("scope", {}) or {}
    auto = m.get("auto_upgrade", {}) or {}
    r.metric_check("build.passed", "passed" in build)

    # consistency
    mode_ok = m.get("mode") == "quick"
    result = m.get("result")
    bp = build.get("passed", None)
    uv = m.get("user_verified", None)
    viols = scope.get("violations", []) or []
    au_req = auto.get("required", False)

    r.consistency_check("mode == quick", mode_ok)
    r.consistency_check("result=approved requires build.passed=true",
                        not (result == "approved" and bp is False))
    r.consistency_check("result=approved requires user_verified=true",
                        not (result == "approved" and uv is False))
    r.consistency_check("auto_upgrade.required=true cannot have result=approved",
                        not (au_req is True and result == "approved"))
    r.consistency_check("scope.violations empty when result=approved",
                        not (viols and result == "approved"))

    return r


def check_full(task_dir, strict=False):
    r = CheckReport(os.path.basename(task_dir), "full")

    # required files
    required = {
        "SDD.md": os.path.join(task_dir, "SDD.md"),
        "ConflictReport.md": os.path.join(task_dir, "ConflictReport.md"),
        "REVIEW.md": os.path.join(task_dir, "REVIEW.md"),
        "TestReport.md": os.path.join(task_dir, "TestReport.md"),
        "metrics.yaml": os.path.join(task_dir, "metrics.yaml"),
    }
    for name, path in required.items():
        r.file_check(name, path, True)

    # optional files
    optional = {
        "TaskSpec.md": os.path.join(task_dir, "TaskSpec.md"),
        "ChangedFiles.md": os.path.join(task_dir, "ChangedFiles.md"),
        "RiskReport.md": os.path.join(task_dir, "RiskReport.md"),
        "retrospective.md": os.path.join(task_dir, "retrospective.md"),
    }
    for name, path in optional.items():
        r.file_check(name, path, strict)

    # metrics
    m = _load_yaml(os.path.join(task_dir, "metrics.yaml"))
    for f in ["task_id", "mode", "result"]:
        r.metric_check(f, f in m)
    for f in ["build", "review", "scope", "user_verified", "regression_required", "skill_patch_required"]:
        r.metric_check(f, f in m)
    build = m.get("build", {}) or {}
    review = m.get("review", {}) or {}
    scope = m.get("scope", {}) or {}
    r.metric_check("build.attempted", "attempted" in build)
    r.metric_check("build.passed", "passed" in build)
    r.metric_check("review.attempted", "attempted" in review)
    r.metric_check("review.verdict", "verdict" in review)
    r.metric_check("scope.unrelated_files_changed", "unrelated_files_changed" in scope)
    r.metric_check("scope.violations", "violations" in scope)

    # consistency
    mode_ok = m.get("mode") == "full"
    result = m.get("result")
    bp = build.get("passed", None)
    ba = build.get("attempted", None)
    uv = m.get("user_verified", None)
    rv = review.get("verdict", None)
    ufc = scope.get("unrelated_files_changed", 0)
    viols = scope.get("violations", []) or []

    r.consistency_check("mode == full", mode_ok)
    r.consistency_check("result=approved requires build.passed=true",
                        not (result == "approved" and bp is False))
    r.consistency_check("result=approved requires user_verified=true",
                        not (result == "approved" and uv is False))
    r.consistency_check("review.verdict=REJECTED cannot have result=approved",
                        not (rv == "REJECTED" and result == "approved"))
    r.consistency_check("scope.unrelated_files_changed == 0",
                        ufc == 0)
    r.consistency_check("scope.violations empty when result=approved",
                        not (viols and result == "approved"))

    return r


# ── main ─────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="v1.8 Harness Check — minimal")
    parser.add_argument("--task", required=True, help="task directory")
    parser.add_argument("--mode", required=True, choices=["quick", "full"])
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--report", default=None)
    args = parser.parse_args()

    task_dir = args.task
    if not os.path.isdir(task_dir):
        print(f"ERROR: task directory not found: {task_dir}")
        sys.exit(2)

    if args.mode == "quick":
        report = check_quick(task_dir, args.strict)
    else:
        report = check_full(task_dir, args.strict)

    report_path = args.report or os.path.join(task_dir, "HarnessCheckReport.md")
    report.write(report_path)

    print(f"task: {report.task_id}")
    print(f"mode: {report.mode}")
    print(f"result: {report.result}")
    if report.blocks:
        for b in report.blocks:
            print(f"  [BLOCKED] {b}")
    if report.warnings:
        for w in report.warnings:
            print(f"  [WARNING] {w}")
    print(f"\nReport: {report_path}")
    sys.exit(report.exit_code)


if __name__ == "__main__":
    main()
