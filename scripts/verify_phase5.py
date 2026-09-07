import os
import sys
import subprocess

# Ensure repository root is on sys.path
repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from scripts.evaluate_system import evaluate_full_system

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

def test_phase5_pipeline():
    audio_sample = os.path.join("data", "raw", "acoustic", "good_tap_1.wav")
    image_sample = os.path.join("data", "raw", "visual", "good", "good_fruit_1.jpg")

    txt_report_path = os.path.join("models", "system_evaluation_report.txt")
    json_report_path = os.path.join("models", "system_evaluation_metrics.json")

    # 1. Test system evaluation suite
    evaluate_full_system(txt_report_path=txt_report_path, json_report_path=json_report_path)
    assert os.path.exists(txt_report_path), "Text evaluation report missing"
    assert os.path.exists(json_report_path), "JSON evaluation metrics missing"

    # 2. Test run_scan.py CLI entry point
    python_exe = sys.executable
    cmd = [python_exe, "run_scan.py", "--audio", audio_sample, "--image", image_sample]
    res = subprocess.run(cmd, capture_output=True, text=True)

    assert res.returncode == 0, f"run_scan.py failed with return code {res.returncode}. Stderr: {res.stderr}"
    assert "FINAL VERDICT" in res.stdout, "run_scan.py output missing 'FINAL VERDICT'"
    assert "Fusion Confidence" in res.stdout, "run_scan.py output missing 'Fusion Confidence'"

    # 3. Test run_scan.py graceful error handling
    cmd_err = [python_exe, "run_scan.py", "--audio", "non_existent.wav", "--image", image_sample]
    res_err = subprocess.run(cmd_err, capture_output=True, text=True)

    assert res_err.returncode != 0, "run_scan.py should exit with non-zero code on missing file"
    assert "TapEye Scanner Error" in res_err.stdout or "TapEye Scanner Error" in res_err.stderr, "Error handling output missing friendly error banner"

    print("\n[Phase 5 Verification Passed] All end-to-end scanner CLI, error handling, and system evaluation suite tests passed successfully!\n")

if __name__ == "__main__":
    test_phase5_pipeline()
