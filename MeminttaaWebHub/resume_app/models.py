from django.db import models

class UserProfile(models.Model):
    """Основной профиль владельца сайта"""
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=150)  # Например: Indie Game Dev / Digital Artist
    bio = models.TextField()
    github_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

class Skill(models.Model):
    """Навыки (3D Modeling, Pixel Art, Django, Python и т.д.)"""
    CATEGORY_CHOICES = [
        ('gamedev', 'Game Development & 3D'),
        ('web', 'Web Backend & DevOps'),
        ('art', 'Digital & Physical Crafts'),
    ]
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    level = models.IntegerField(default=50) # Процент владения от 0 до 100

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"

class AIMultinomialLog(models.Model):
    """Логирование работы текстовой нейросети для отчета практик"""
    input_text = models.TextField()
    predicted_category = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Log {self.id}: {self.predicted_category} at {self.created_at.strftime('%Y-%m-%d %H:%M')}"