import os
import json
import joblib
import requests
from django.shortcuts import render
from django.http import JsonResponse
from .models import UserProfile, Skill

MODEL_FILE = "text_classifier.pkl"
VECTORIZER_FILE = "vectorizer.pkl"
FASTAPI_URL = "http://127.0.0.1:8001/api/scan-faces/"  # Стало 8001 # Адрес нашего асинхронного ИИ-сервера

def index_page(request):
    profile = UserProfile.objects.first()
    skills = Skill.objects.all()
    context = {'profile': profile, 'skills': skills}
    return render(request, "resume_app/index.html", context)


def analyze_text_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_text = data.get('text', '').strip()
            if not user_text:
                return JsonResponse({'success': False, 'error': 'Пустой текст'})

            if os.path.exists(MODEL_FILE) and os.path.exists(VECTORIZER_FILE):
                model = joblib.load(MODEL_FILE)
                vectorizer = joblib.load(VECTORIZER_FILE)
                X_test = vectorizer.transform([user_text])
                prediction = model.predict(X_test)[0]
                probabilities = model.predict_proba(X_test)[0]
                
                classes = {3: "ПОЗИТИВНЫЙ 😊", 2: "НЕЙТРАЛЬНЫЙ 😐", 1: "СМЕШАННЫЙ 🏎", 0: "НЕГАТИВНЫЙ 😡"}
                proba_dict = {i: float(probabilities[i] * 100) for i in range(4)}
                
                return JsonResponse({
                    'success': True,
                    'verdict': classes[prediction],
                    'confidence': float(probabilities[prediction] * 100),
                    'probabilities': proba_dict
                })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Неверный метод'})


def recognize_faces_view(request):
    """Отправляет загруженное фото на обработку в асинхронный FastAPI-сервер"""
    if request.method == 'POST' and request.FILES.get('file'):
        try:
            image_file = request.FILES['file']
            
            # Пересылаем файл в FastAPI
            files = {'file': (image_file.name, image_file.read(), image_file.content_type)}
            response = requests.post(FASTAPI_URL, files=files)
            
            if response.status_code == 200:
                fastapi_data = response.json()
                return JsonResponse(fastapi_data)
            else:
                return JsonResponse({'success': False, 'error': 'ИИ-сервер вернул ошибку'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
            
    return JsonResponse({'success': False, 'error': 'Файл не получен'})