import os
import sys
import shutil
import tempfile
import json
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Ensure repository root is on sys.path
repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

from fusion.predict import predict_final_verdict

app = FastAPI(
    title="TapEye REST API Engine",
    description="Dual-Modal (Acoustic + Visual) Produce Quality Scanner Backend API",
    version="2.0.0"
)

# Enable CORS for Next.js React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {
        "status": "online",
        "service": "TapEye Dual-Modal REST API Engine",
        "version": "2.0.0"
    }


@app.post("/api/scan")
async def scan_produce(audio: UploadFile = File(...), image: UploadFile = File(...)):
    """
    Accepts dual-modal produce inputs (audio .wav recording and surface image photo),
    executes acoustic & visual feature extraction, late-fusion inference, and returns verdict JSON payload.
    """
    if not audio.filename.endswith((".wav", ".WAV")):
        raise HTTPException(status_code=400, detail="Audio file must be a valid .wav format.")

    if not image.filename.endswith((".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG")):
        raise HTTPException(status_code=400, detail="Image file must be a valid .jpg, .jpeg, or .png format.")

    # Create temporary directory for processing uploaded files
    temp_dir = tempfile.mkdtemp()
    try:
        audio_path = os.path.join(temp_dir, audio.filename)
        image_path = os.path.join(temp_dir, image.filename)

        with open(audio_path, "wb") as f_aud:
            shutil.copyfileobj(audio.file, f_aud)

        with open(image_path, "wb") as f_img:
            shutil.copyfileobj(image.file, f_img)

        # Run late-fusion prediction
        verdict_result = predict_final_verdict(audio_path, image_path)

        # Format clean response payload
        response_payload = {
            "success": True,
            "filename_audio": audio.filename,
            "filename_image": image.filename,
            "final_verdict": verdict_result["final_verdict"],
            "fusion_confidence": float(verdict_result["fusion_confidence"]),
            "fused_probabilities": verdict_result["fused_probabilities"],
            "acoustic_branch": {
                "predicted_class": verdict_result["acoustic_branch"]["predicted_class"],
                "probabilities": verdict_result["acoustic_branch"]["probabilities"]
            },
            "visual_branch": {
                "predicted_class": verdict_result["visual_branch"]["predicted_class"],
                "probabilities": verdict_result["visual_branch"]["probabilities"]
            }
        }
        return JSONResponse(content=response_payload)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference execution failed: {str(e)}")
    finally:
        # Cleanup temporary files
        shutil.rmtree(temp_dir, ignore_errors=True)


@app.get("/api/performance")
def get_performance_metrics():
    """
    Returns benchmark performance evaluation metrics comparing Acoustic-Only, Visual-Only, and Late-Fusion models.
    """
    json_path = os.path.join("models", "system_evaluation_metrics.json")
    if not os.path.exists(json_path):
        raise HTTPException(
            status_code=444,
            detail="Evaluation metrics report not found. Run scripts/evaluate_system.py first."
        )

    try:
        with open(json_path, "r", encoding="utf-8") as f:
            metrics_data = json.load(f)
        return JSONResponse(content=metrics_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read metrics file: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
