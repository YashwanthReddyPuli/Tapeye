import os
import csv
import glob

def create_fusion_manifest():
    raw_dir = os.path.join("data", "raw")
    acoustic_dir = os.path.join(raw_dir, "acoustic")
    visual_dir = os.path.join(raw_dir, "visual")
    manifest_path = os.path.join(raw_dir, "fusion_pairs.csv")

    categories = ["good", "borderline", "bad"]
    pairs = []

    for cat in categories:
        # Find matching audio files
        audio_files = sorted(glob.glob(os.path.join(acoustic_dir, f"{cat}_*.wav")))
        # Find matching visual files
        img_dir = os.path.join(visual_dir, cat)
        image_files = sorted(glob.glob(os.path.join(img_dir, "*.*")))

        num_pairs = min(len(audio_files), len(image_files))
        for i in range(num_pairs):
            rel_audio = os.path.relpath(audio_files[i], start=os.getcwd()).replace("\\", "/")
            rel_img = os.path.relpath(image_files[i], start=os.getcwd()).replace("\\", "/")
            pairs.append((rel_audio, rel_img, cat))

    if not pairs:
        print("Warning: No matching acoustic and visual file pairs found to create manifest.")
        return

    os.makedirs(os.path.dirname(manifest_path), exist_ok=True)
    with open(manifest_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["audio_path", "image_path", "label"])
        writer.writerows(pairs)

    print(f"Created fusion manifest at '{manifest_path}' with {len(pairs)} paired produce items:")
    for a, i, l in pairs:
        print(f" - [{l.upper()}] Audio: {os.path.basename(a)} | Image: {os.path.basename(i)}")

if __name__ == "__main__":
    create_fusion_manifest()
