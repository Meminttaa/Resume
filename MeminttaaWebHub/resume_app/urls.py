from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_page, name='index'),
    path('ai/analyze-text/', views.analyze_text_view, name='analyze_text'),
    path('ai/recognize-faces/', views.recognize_faces_view, name='recognize_faces'),
]