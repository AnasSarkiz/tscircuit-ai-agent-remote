"""Exercise the Linux supervisor without routing or generating board copper."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time

if sys.platform != "linux":
    raise SystemExit("Linux cloud only; no supervisor execution on the Mac.")

root = Path(__file__).resolve().parents[2]
wrapper = root / "scripts/cloud/run_with_budget.py"
output = root / "evidence/cloud-setup-smoke"
output.mkdir(parents=True, exist_ok=True)


def invoke(case, command, budget):
    return [sys.executable, str(wrapper), "--log", str(output / (case + ".log")),
            *budget, "--", sys.executable, "-c", command]


results = []
with tempfile.TemporaryDirectory(prefix="ai-remote-supervisor-") as temporary:
    cases = [
        ("success", "print('completed small command')", ["--seconds", "5"], 0, None),
        ("timeout", "import time; time.sleep(30)", ["--seconds", "1"], 124,
         "TIME_BUDGET_REACHED"),
        ("memory", "import time; allocation=bytearray(128*1024**2); time.sleep(30)",
         ["--seconds", "10", "--memory-mib", "32"], 124, "MEMORY_BUDGET_REACHED"),
    ]
    for name, command, budget, expected_code, expected_reason in cases:
        completed = subprocess.run(invoke(name, command, budget), cwd=temporary,
                                   capture_output=True, text=True, timeout=30)
        outcome = json.loads((output / (name + ".log.outcome.json")).read_text())
        if completed.returncode != expected_code or outcome["termination"] != expected_reason:
            raise RuntimeError({"case": name, "returncode": completed.returncode,
                                "outcome": outcome, "stderr": completed.stderr})
        results.append({"case": name, "passed": True, "outcome": outcome})
    holder = subprocess.Popen(invoke("lock-holder", "import time; time.sleep(2)",
                                     ["--seconds", "5"]), cwd=temporary,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        deadline = time.monotonic() + 5
        while not (Path(temporary) / ".cloud-routing.lock").exists():
            if holder.poll() is not None or time.monotonic() > deadline:
                raise RuntimeError("Lock holder did not acquire supervisor lock")
            time.sleep(.05)
        rejected = subprocess.run(invoke("lock-rejected", "print('must not run')",
                                         ["--seconds", "5"]), cwd=temporary,
                                  capture_output=True, text=True, timeout=10)
        if rejected.returncode != 2 or "Another cloud operation" not in rejected.stderr:
            raise RuntimeError("Concurrent operation was not rejected")
        holder.communicate(timeout=10)
        if holder.returncode != 0 or (Path(temporary) / ".cloud-routing.lock").exists():
            raise RuntimeError("Lock holder failed or left its lock behind")
        results.append({"case": "exclusive-lock", "passed": True})
    finally:
        if holder.poll() is None:
            holder.terminate()
            holder.communicate(timeout=15)
receipt = {"checks": results, "native_routing_executed": False,
           "fabrication_approval_inferred": False}
(output / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps({"passed_checks": len(results), "receipt": str(output / "receipt.json")}))
