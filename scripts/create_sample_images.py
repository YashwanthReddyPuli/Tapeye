import os
import cv2
import numpy as np

def generate_synthetic_fruit_image(category: str, seed: int = 42) -> np.ndarray:
    """
    Generate a synthetic 256x256 image simulating a fruit:
    - 'good': Vibrant green/red fruit, smooth surface, no dark spots
    - 'borderline': Yellowish/orange fruit, minor surface spots
    - 'bad': Dark brownish/decayed fruit, large dark blemishes
    """
    np.random.seed(seed)
    img = np.zeros((256, 256, 3), dtype=np.uint8)

    
    # Background (neutral grey lab bench)
    img[:, :] = [180, 180, 180]
    
    # Draw circular fruit body
    center = (128, 128)
    radius = 90
    
    if category == "good":
        # Vibrant green apple/tomato
        base_color = (40, 180, 50)  # BGR
    elif category == "borderline":
        # Ripening yellow/orange fruit with small spots
        base_color = (30, 170, 220)  # BGR
    else:  # 'bad'
        # Overripe / bruised brown fruit
        base_color = (30, 60, 110)  # BGR

    # Fill fruit base
    cv2.circle(img, center, radius, base_color, -1)
    
    # Add subtle gradient/texture noise
    noise = np.random.randint(-15, 15, (256, 256, 3), dtype=np.int16)
    mask = np.zeros((256, 256), dtype=np.uint8)
    cv2.circle(mask, center, radius, 255, -1)
    
    textured = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    img = np.where(mask[:, :, None] == 255, textured, img)
    
    # Add category-specific blemishes
    if category == "borderline":
        # Add 3-5 small brownish spots
        for _ in range(4):
            spot_center = (
                int(center[0] + np.random.randint(-50, 50)),
                int(center[1] + np.random.randint(-50, 50))
            )
            cv2.circle(img, spot_center, np.random.randint(4, 10), (20, 50, 80), -1)
    elif category == "bad":
        # Add large dark decay patches
        for _ in range(3):
            patch_center = (
                int(center[0] + np.random.randint(-40, 40)),
                int(center[1] + np.random.randint(-40, 40))
            )
            cv2.circle(img, patch_center, np.random.randint(18, 35), (15, 30, 50), -1)
            
    return img

def main():
    base_dir = os.path.join("data", "raw", "visual")
    categories = ["good", "borderline", "bad"]
    
    total_created = 0
    for cat in categories:
        cat_dir = os.path.join(base_dir, cat)
        os.makedirs(cat_dir, exist_ok=True)
        
        for i in range(5):
            img = generate_synthetic_fruit_image(cat, seed=i*10 + len(cat))
            filename = f"{cat}_fruit_{i+1}.jpg"
            filepath = os.path.join(cat_dir, filename)
            cv2.imwrite(filepath, img)
            total_created += 1

    print(f"Generated {total_created} synthetic produce images across 'good/', 'borderline/', 'bad/' in '{base_dir}'.")

if __name__ == "__main__":
    main()
