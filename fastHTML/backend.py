from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import cv2
import numpy as np
import mediapipe as mp
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import random

app = FastAPI()

def generate_fortune():
    fortunes = [
        "The stars align in your favor. Great opportunities await you.",
        "A journey of self-discovery lies ahead. Embrace the unknown.",
        "Your creativity will lead you to unexpected treasures.",
        "A challenge you've been facing will soon resolve itself.",
        "Love and harmony will enter your life in a surprising way.",
        "Your persistence will pay off. Keep pushing forward.",
        "An old friend will bring exciting news.",
        "Your intuition is strong. Trust your inner voice.",
        "A dream you've long held will soon become reality.",
        "Unexpected kindness will brighten your path."
    ]
    return random.choice(fortunes)

@app.post("/detect_face/")
async def detect_face(file: UploadFile = File(...)):
    contents = await file.read()
    img = cv2.imdecode(np.frombuffer(contents, np.uint8), cv2.IMREAD_COLOR)
    rgb_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    base_options = python.BaseOptions(model_asset_path='face_landmarker_v2_with_blendshapes.task')
    options = vision.FaceLandmarkerOptions(
        base_options=base_options,
        output_face_blendshapes=True,
        output_facial_transformation_matrixes=True,
        num_faces=1
    )
    detector = vision.FaceLandmarker.create_from_options(options)
    
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)
    detection_result = detector.detect(mp_image)
    
    if not detection_result.face_landmarks:
        raise HTTPException(status_code=400, detail="No face detected")

    return JSONResponse(content={"fortune": generate_fortune()})