from __future__ import annotations

import json
from pathlib import Path

from guard_core import check_security_v2, optimize_prompt_v1


FIXTURE_PATH = Path(__file__).resolve().parent.parent / "references" / "test_prompts.jsonl"


def main() -> None:
    failures = []
    for line_number, line in enumerate(FIXTURE_PATH.read_text(encoding="utf-8").splitlines(), start=1):
        case = json.loads(line)
        result = check_security_v2(case["message"], enable_semantic=False)
        if result["suggested_action"] != case["expected_action"]:
            failures.append((line_number, "suggested_action", case["expected_action"], result["suggested_action"]))
        if result["detector"] != case["expected_detector"]:
            failures.append((line_number, "detector", case["expected_detector"], result["detector"]))

    if failures:
        for line_number, field, expected, actual in failures:
            print(f"FAIL line {line_number}: {field} expected {expected!r}, got {actual!r}")
        raise SystemExit(1)

    optimization_result = optimize_prompt_v1("make a product launch video")
    if optimization_result["optimized"] or optimization_result["implemented"]:
        print("FAIL optimization stub: reserved module must not report implemented optimization.")
        raise SystemExit(1)

    print("Smoke tests passed.")


if __name__ == "__main__":
    main()
