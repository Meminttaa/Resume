import os
import cv2
import numpy as np
import face_recognition
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Crimson Face Recognition Async API")

# Разрешаем CORS, чтобы Django мог без проблем общаться с FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATASET_FOLDER = "dataset"
known_faces = []
known_names = []

@app.on_event("startup")
async def load_dataset():
    """Асинхронная инициализация: загружаем лица из базы при старте сервера"""
    global known_faces, known_names
    known_faces.clear()
    known_names.clear()
    
    if not os.path.exists(DATASET_FOLDER):
        os.makedirs(DATASET_FOLDER)
        return

    print("=== [FastAPI] Начинаю асинхронное сканирование базы датасета ===")
    for person_name in os.listdir(DATASET_FOLDER):
        person_folder = os.path.join(DATASET_FOLDER, person_name)
        if not os.path.isdir(person_folder):
            continue
            
        for filename in os.listdir(person_folder):
            if filename.lower().endswith((".jpg", ".jpeg", ".png")):
                path = os.path.join(person_folder, filename)
                try:
                    img = cv2.imread(path)
                    if img is None:
                        continue
                    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    encodings = face_recognition.face_encodings(rgb_img)
                    if len(encodings) > 0:
                        known_faces.append(encodings[0])
                        known_names.append(person_name)
                except Exception as e:
                    print(f"Ошибка при чтении {filename}: {e}")
                    
    print(f"=== [FastAPI] База готова! Успешно загружено {len(known_faces)} лиц ===")


@app.post("/api/scan-faces/")
async def scan_faces(file: UploadFile = File(...)):
    """Асинхронный эндпоинт для распознавания лиц на фото"""
    try:
        # Читаем файл из сети в память
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        img_bgr = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img_bgr is None:
            return {"success": False, "error": "Не удалось прочитать изображение"}
            
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        
        # Находим лица через dlib
        face_locations = face_recognition.face_locations(img_rgb)
        face_encodings = face_recognition.face_encodings(img_rgb, face_locations)
        
        detected_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_faces, face_encoding, tolerance=0.55)
            name = "Unknown"
            
            if True in matches:
                face_distances = face_recognition.face_distance(known_faces, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_names[best_match_index]
            
            detected_names.append(name)
            
        return {
            "success": True,
            "faces_count": len(detected_names),
            "names": detected_names
        }
    except Exception as e:
        return {"success": False, "error": str(e)}