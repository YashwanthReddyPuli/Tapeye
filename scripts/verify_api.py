import os
import sys
import json
import urllib.request
import uuid

def encode_multipart_formdata(fields, files):
    boundary = uuid.uuid4().hex
    body = []
    
    for key, value in fields.items():
        body.append(f'--{boundary}'.encode('utf-8'))
        body.append(f'Content-Disposition: form-data; name="{key}"'.encode('utf-8'))
        body.append(b'')
        body.append(str(value).encode('utf-8'))
        
    for key, (filename, content, content_type) in files.items():
        body.append(f'--{boundary}'.encode('utf-8'))
        body.append(f'Content-Disposition: form-data; name="{key}"; filename="{filename}"'.encode('utf-8'))
        body.append(f'Content-Type: {content_type}'.encode('utf-8'))
        body.append(b'')
        body.append(content)
        
    body.append(f'--{boundary}--'.encode('utf-8'))
    body.append(b'')
    
    content_type_header = f'multipart/form-data; boundary={boundary}'
    return content_type_header, b'\r\n'.join(body)

def test_api():
    print("=== Testing TapEye FastAPI Backend ===")
    
    # 1. Test GET /api/performance
    try:
        req = urllib.request.Request("http://localhost:8000/api/performance")
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            print("\n[SUCCESS] GET /api/performance returned:")
            print(json.dumps(data, indent=2))
    except Exception as e:
        print(f"\n[ERROR] GET /api/performance failed: {e}")

    # 2. Test POST /api/scan with sample files
    audio_path = os.path.abspath("data/raw/acoustic/good_tap_1.wav")
    image_path = os.path.abspath("data/raw/visual/good/good_fruit_1.jpg")

    if not os.path.exists(audio_path) or not os.path.exists(image_path):
        print(f"\n[SKIP] Test audio or image file missing: {audio_path}, {image_path}")
        return

    try:
        with open(audio_path, 'rb') as f_audio, open(image_path, 'rb') as f_image:
            audio_bytes = f_audio.read()
            image_bytes = f_image.read()

        content_type, body = encode_multipart_formdata(
            fields={},
            files={
                'audio': ('good_tap_1.wav', audio_bytes, 'audio/wav'),
                'image': ('good_fruit_1.jpg', image_bytes, 'image/jpeg')
            }
        )

        req = urllib.request.Request(
            "http://localhost:8000/api/scan",
            data=body,
            headers={'Content-Type': content_type}
        )

        with urllib.request.urlopen(req) as resp:
            res_data = json.loads(resp.read().decode())
            print("\n[SUCCESS] POST /api/scan returned:")
            print(json.dumps(res_data, indent=2))

    except Exception as e:
        print(f"\n[ERROR] POST /api/scan failed: {e}")

if __name__ == "__main__":
    test_api()
