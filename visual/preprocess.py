import os
import cv2
import numpy as np
import tensorflow as tf

def preprocess_image(image_path: str) -> np.ndarray:
    """
    Load an image from disk, convert to RGB, resize to 224x224,
    and normalize pixel values as required by MobileNetV2.

    Parameters:
        image_path (str): Path to input image (.jpg, .png, etc.)

    Returns:
        np.ndarray: Normalized image array of shape (224, 224, 3) ready for model input.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Visual image file not found: {image_path}")

    # Load image using OpenCV (BGR format)
    img_bgr = cv2.imread(image_path)
    if img_bgr is None:
        raise ValueError(f"Failed to decode image at path: {image_path}")

    # Convert BGR to RGB
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

    # Resize to 224x224 (MobileNetV2 standard input dimension)
    img_resized = cv2.resize(img_rgb, (224, 224), interpolation=cv2.INTER_AREA)

    # Convert float32 and normalize via MobileNetV2 preprocess_input (scales to [-1, 1])
    img_array = img_resized.astype(np.float32)
    processed_img = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)

    return processed_img
