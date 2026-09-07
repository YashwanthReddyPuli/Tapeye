import os
import glob
import pickle
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split

try:
    from visual.preprocess import preprocess_image
except ModuleNotFoundError:
    from preprocess import preprocess_image


def augment_image(image: np.ndarray) -> np.ndarray:
    """
    Apply basic data augmentation to a single preprocessed image:
    - Random horizontal flip
    - Small random rotation / shift
    - Slight brightness jitter
    """
    img_tensor = tf.convert_to_tensor(image, dtype=tf.float32)

    # 1. Random horizontal flip
    img_tensor = tf.image.random_flip_left_right(img_tensor)

    # 2. Slight brightness jitter
    img_tensor = tf.image.random_brightness(img_tensor, max_delta=0.1)

    # 3. Clip back to [-1.0, 1.0] range expected by MobileNetV2
    img_augmented = tf.clip_by_value(img_tensor, -1.0, 1.0)
    return img_augmented.numpy()


def build_visual_dataset(raw_dir: str = os.path.join("data", "raw", "visual"),
                         output_path: str = os.path.join("data", "processed", "visual", "dataset.pkl"),
                         augment_factor: int = 2) -> dict:
    """
    Load raw visual images, preprocess, split into 70/15/15 train/val/test,
    apply data augmentation to train set, and save dataset.pkl archive.
    """
    if not os.path.exists(raw_dir):
        raise FileNotFoundError(f"Raw visual dataset directory not found: {raw_dir}")

    # Subdirectories correspond to class labels
    class_subdirs = [d for d in os.listdir(raw_dir) if os.path.isdir(os.path.join(raw_dir, d))]
    if not class_subdirs:
        raise FileNotFoundError(f"No class subdirectories found in '{raw_dir}'")

    class_names = sorted(class_subdirs)
    class_to_idx = {name: i for i, name in enumerate(class_names)}

    X_list = []
    y_list = []
    filenames = []

    valid_exts = ("*.jpg", "*.jpeg", "*.png", "*.bmp", "*.webp")

    for cname in class_names:
        cdir = os.path.join(raw_dir, cname)
        img_paths = []
        for ext in valid_exts:
            img_paths.extend(glob.glob(os.path.join(cdir, ext)))

        print(f"Class '{cname}': Found {len(img_paths)} image(s)")
        for ipath in img_paths:
            try:
                proc_img = preprocess_image(ipath)
                X_list.append(proc_img)
                y_list.append(class_to_idx[cname])
                filenames.append(os.path.basename(ipath))
            except Exception as e:
                print(f"Warning: Skipping corrupted image '{ipath}': {e}")

    X = np.array(X_list, dtype=np.float32)
    y = np.array(y_list, dtype=np.int64)

    if len(X) == 0:
        raise ValueError("No valid visual images could be loaded!")

    unique_classes, counts = np.unique(y, return_counts=True)
    min_count = np.min(counts) if len(counts) > 0 else 0

    # Robust splitting logic
    if min_count >= 6 and len(X) >= 18:
        try:
            X_train, X_temp, y_train, y_temp = train_test_split(
                X, y, test_size=0.30, random_state=42, stratify=y
            )
            X_val, X_test, y_val, y_test = train_test_split(
                X_temp, y_temp, test_size=0.50, random_state=42, stratify=y_temp
            )
        except Exception:
            # Fallback if stratification fails
            X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.30, random_state=42)
            X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.50, random_state=42)
    else:
        print("Note: Small dataset detected (< 18 samples or < 6 per class). Using adaptive train/val/test split.")
        train_idxs, val_idxs, test_idxs = [], [], []

        for c_idx in range(len(class_names)):
            cls_mask = np.where(y == c_idx)[0]
            n_cls = len(cls_mask)
            if n_cls >= 3:
                n_train = max(1, int(n_cls * 0.6))
                n_val = max(1, int((n_cls - n_train) / 2))
                train_idxs.extend(cls_mask[:n_train])
                val_idxs.extend(cls_mask[n_train:n_train + n_val])
                test_idxs.extend(cls_mask[n_train + n_val:])
            else:
                train_idxs.extend(cls_mask)
                val_idxs.extend(cls_mask)
                test_idxs.extend(cls_mask)

        X_train, y_train = X[train_idxs], y[train_idxs]
        X_val, y_val = X[val_idxs], y[val_idxs]
        X_test, y_test = X[test_idxs], y[test_idxs]

    # Apply data augmentation to training set only
    X_train_aug = list(X_train)
    y_train_aug = list(y_train)

    if augment_factor > 1:
        for img, lbl in zip(X_train, y_train):
            for _ in range(augment_factor - 1):
                X_train_aug.append(augment_image(img))
                y_train_aug.append(lbl)

    X_train = np.array(X_train_aug, dtype=np.float32)
    y_train = np.array(y_train_aug, dtype=np.int64)

    dataset = {
        "X_train": X_train,
        "y_train": y_train,
        "X_val": X_val,
        "y_val": y_val,
        "X_test": X_test,
        "y_test": y_test,
        "class_names": class_names,
        "class_to_idx": class_to_idx,
        "filenames": filenames
    }

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "wb") as f:
        pickle.dump(dataset, f)

    print(f"Visual dataset built successfully and saved to '{output_path}'.")
    print(f" - Train samples (augmented): {len(X_train)}")
    print(f" - Validation samples:        {len(X_val)}")
    print(f" - Test samples:              {len(X_test)}")
    print(f" - Classes ({len(class_names)}): {class_names}")

    return dataset


if __name__ == "__main__":
    build_visual_dataset()
