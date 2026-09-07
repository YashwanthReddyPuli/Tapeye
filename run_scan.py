import os
import sys
import argparse

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

def main():
    parser = argparse.ArgumentParser(
        description="TapEye - Dual-Modal (Acoustic + Visual) Produce Quality Scanner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example Usage:
  python run_scan.py --audio data/raw/acoustic/good_tap_1.wav --image data/raw/visual/good/good_fruit_1.jpg
        """
    )
    parser.add_argument("--audio", type=str, required=True, help="Path to produce tap recording (.wav)")
    parser.add_argument("--image", type=str, required=True, help="Path to produce surface photo (.jpg, .png)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON format instead of terminal dashboard")

    args = parser.parse_args()

    # 1. Validate Input Files
    if not os.path.exists(args.audio):
        print(f"\n[TapEye Scanner Error] Audio file not found: '{args.audio}'")
        print("Please check the path and try again.\n")
        sys.exit(1)

    if not os.path.exists(args.image):
        print(f"\n[TapEye Scanner Error] Image file not found: '{args.image}'")
        print("Please check the path and try again.\n")
        sys.exit(1)

    # 2. Check Trained Model Files
    model_paths = {
        "Acoustic Classifier": os.path.join("models", "acoustic_classifier.pkl"),
        "Visual Classifier": os.path.join("models", "visual_classifier.keras"),
        "Fusion Meta-Classifier": os.path.join("models", "fusion_classifier.pkl")
    }

    missing_models = [name for name, path in model_paths.items() if not os.path.exists(path)]
    if missing_models:
        print("\n[TapEye Scanner Error] Missing required trained model binaries:")
        for name in missing_models:
            print(f" - {name} ({model_paths[name]})")
        print("\nPlease run the model training scripts first:")
        print("  python acoustic/train_classifier.py")
        print("  python visual/train_classifier.py")
        print("  python fusion/train_meta_classifier.py\n")
        sys.exit(1)

    # 3. Execute Dual-Modal Inference
    try:
        from fusion.predict import predict_final_verdict
        result = predict_final_verdict(args.audio, args.image)
    except Exception as e:
        print(f"\n[TapEye Processing Error] Failed to process produce scan: {e}")
        sys.exit(1)

    if args.json:
        import json
        print(json.dumps(result, indent=2))
        return

    # 4. Render Formatted Console Scanner Dashboard
    verdict = result["final_verdict"].upper()
    if verdict == "BAD":
        display_verdict = "REJECT / BAD"
        color_code = "\033[91m"  # Red
    elif verdict == "BORDERLINE":
        display_verdict = "BORDERLINE"
        color_code = "\033[93m"  # Yellow
    else:
        display_verdict = "GOOD"
        color_code = "\033[92m"  # Green
    reset_code = "\033[0m"

    ac_pred = result["acoustic_branch"]["predicted_class"].upper()
    ac_conf = result["acoustic_branch"]["probabilities"].get(result["acoustic_branch"]["predicted_class"], 0.0) * 100

    vis_pred = result["visual_branch"]["predicted_class"].upper()
    vis_conf = result["visual_branch"]["probabilities"].get(result["visual_branch"]["predicted_class"], 0.0) * 100

    fusion_conf = result["fusion_confidence"] * 100

    print("\n" + "=" * 60)
    print("           TapEye Produce Quality Scan Result")
    print("=" * 60)
    print(f" Audio Input:  {args.audio}")
    print(f" Image Input:  {args.image}")
    print("-" * 60)

    print(f" FINAL VERDICT:     {color_code}>>> {display_verdict} <<<{reset_code}")
    print(f" Fusion Confidence: {fusion_conf:.2f}%")
    print("-" * 60)

    print(" Multimodal Branch Analysis:")
    print(f"  - Acoustic Branch (Internal Impact):  {ac_pred:10s} (Confidence: {ac_conf:5.1f}%)")
    print(f"  - Visual Branch   (External Surface): {vis_pred:10s} (Confidence: {vis_conf:5.1f}%)")

    # Conflict Warning Banner
    if ac_pred != vis_pred:
        print("-" * 60)
        print(" [!] NOTICE: Acoustic & Visual branches reported conflicting findings.")
        print("     The late-fusion meta-classifier prioritized the combined modal evidence.")

    print("=" * 60 + "\n")

if __name__ == "__main__":
    main()
