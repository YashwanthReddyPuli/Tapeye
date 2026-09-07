import os
import numpy as np

def verify_extracted_features():
    processed_dir = os.path.join("data", "processed", "acoustic")
    files = [f for f in os.listdir(processed_dir) if f.endswith(".npz")]
    assert len(files) >= 3, f"Expected at least 3 feature files, found {len(files)}"
    
    expected_keys = {
        "signal", "sample_rate", "duration", "fft_magnitude",
        "fft_freqs", "mfcc", "spectral_centroid", "zero_crossing_rate", "rms_energy"
    }

    for fname in files:
        filepath = os.path.join(processed_dir, fname)
        data = np.load(filepath)
        keys = set(data.files)
        missing = expected_keys - keys
        assert not missing, f"File {fname} is missing keys: {missing}"
        
        # Verify shape requirements
        assert data["mfcc"].shape[0] == 13, f"MFCC coefficients must be 13, got shape {data['mfcc'].shape}"
        assert len(data["signal"]) > 0, "Signal array is empty"
        assert float(data["duration"]) > 0, "Duration must be positive"
        assert float(data["sample_rate"]) > 0, "Sample rate must be positive"

        print(f"Verified {fname}: {len(keys)} feature keys present, MFCC shape={data['mfcc'].shape}, SR={data['sample_rate']}Hz, duration={data['duration']:.2f}s")

if __name__ == "__main__":
    verify_extracted_features()
