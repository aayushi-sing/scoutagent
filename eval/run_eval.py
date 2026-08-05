"""
Lightweight eval harness for ScoutAgent.
Run from repo root:  python eval/run_eval.py

For each test case, checks:
  - pipeline completes without raising
  - Memory Manager JSON parsed (not the silent fallback in pipeline.py)
  - startup count >= min_startups
  - every startup has a Critic score
  - report contains all 5 required sections
  - latency

Writes eval/results/<timestamp>.json (raw) and prints a summary table.
"""

import sys, os, time, json
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pipeline import run_pipeline
from eval.test_cases import TEST_CASES, REQUIRED_REPORT_SECTIONS

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "results")
LATENCY_BUDGET_SEC = 180  # flag anything over 3 min as a latency failure


def check_run(topic, min_startups, result: dict, elapsed: float) -> dict:
    failures = []

    startups = result.get("startups", [])
    scores = result.get("scores", {})
    report = result.get("report", "")

    # 1. did the memory-manager JSON parse succeed?
    # pipeline.py's fallback produces run_quality == 0 with empty lists —
    # treat that pattern as a parse failure, not a genuine "0 startups found".
    if result.get("quality", 0) == 0 and not startups:
        failures.append("memory_json_parse_failed")

    # 2. startup count
    if len(startups) < min_startups:
        failures.append(f"too_few_startups (got {len(startups)}, expected >= {min_startups})")

    # 3. every startup scored
    unscored = [s for s in startups if s not in scores]
    if unscored:
        failures.append(f"missing_scores_for: {unscored}")

    # 4. report sections present
    missing_sections = [s for s in REQUIRED_REPORT_SECTIONS if s not in report]
    if missing_sections:
        failures.append(f"missing_report_sections: {missing_sections}")

    # 5. report not suspiciously short (truncated / near-empty)
    if len(report) < 200:
        failures.append(f"report_too_short ({len(report)} chars)")

    # 6. latency
    if elapsed > LATENCY_BUDGET_SEC:
        failures.append(f"latency_over_budget ({elapsed:.1f}s > {LATENCY_BUDGET_SEC}s)")

    return {
        "pass": len(failures) == 0,
        "failures": failures,
        "latency_sec": round(elapsed, 1),
        "startup_count": len(startups),
        "quality_score": result.get("quality", 0),
    }


def run_eval():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    run_log = []

    for case in TEST_CASES:
        print(f"\n=== Running {case['id']}: '{case['topic']}' ===")
        start = time.time()
        try:
            result = run_pipeline(case["topic"])
            elapsed = time.time() - start
            outcome = check_run(case["topic"], case["min_startups"], result, elapsed)
        except Exception as e:
            elapsed = time.time() - start
            outcome = {
                "pass": False,
                "failures": [f"exception: {type(e).__name__}: {e}"],
                "latency_sec": round(elapsed, 1),
                "startup_count": 0,
                "quality_score": 0,
            }

        outcome["id"] = case["id"]
        outcome["topic"] = case["topic"]
        run_log.append(outcome)

        status = "PASS" if outcome["pass"] else "FAIL"
        print(f"[{status}] {case['id']} — {outcome['latency_sec']}s — "
              f"{outcome['startup_count']} startups — "
              f"{'; '.join(outcome['failures']) if outcome['failures'] else 'no issues'}")

    # summary
    total = len(run_log)
    passed = sum(1 for r in run_log if r["pass"])
    avg_latency = sum(r["latency_sec"] for r in run_log) / total if total else 0

    print("\n" + "=" * 50)
    print(f"SUMMARY: {passed}/{total} passed  |  avg latency: {avg_latency:.1f}s")
    if passed < total:
        print("\nFailure breakdown:")
        for r in run_log:
            if not r["pass"]:
                print(f"  - {r['id']}: {r['failures']}")
    print("=" * 50)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = os.path.join(RESULTS_DIR, f"eval_{ts}.json")
    with open(out_path, "w") as f:
        json.dump({
            "timestamp": ts,
            "total": total,
            "passed": passed,
            "avg_latency_sec": round(avg_latency, 1),
            "runs": run_log,
        }, f, indent=2)
    print(f"\nResults written to {out_path}")


if __name__ == "__main__":
    run_eval()