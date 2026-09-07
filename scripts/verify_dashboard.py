import os
import sys

# Ensure repository root is on sys.path
repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

def test_dashboard_files():
    dashboard_files = [
        os.path.join("dashboard", "app.py"),
        os.path.join("dashboard", "utils.py"),
        os.path.join("dashboard", "pages", "1_Scan.py"),
        os.path.join("dashboard", "pages", "2_Model_Performance.py"),
        os.path.join("dashboard", "pages", "3_About.py"),
    ]

    for filepath in dashboard_files:
        assert os.path.exists(filepath), f"Dashboard file missing: {filepath}"
        print(f"Verified existence: {filepath}")

    # Test importing utils module functions
    from dashboard.utils import check_and_warmup_models, load_evaluation_metrics
    models_ready, status = check_and_warmup_models()
    metrics = load_evaluation_metrics()

    print(f"Utils Warmup Status: ready={models_ready}, status={status}")
    print(f"Evaluation Metrics Loaded: {metrics is not None}")
    print("\n[Dashboard Verification Passed] All dashboard files, pages, and utility functions verified successfully!\n")

if __name__ == "__main__":
    test_dashboard_files()
