from django.db import models

from django.contrib.auth.models import User

from django.db import models

class Sentence(models.Model):

    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('ar', 'Arabic'),
        ('fr', 'French'),
        ('es', 'Spanish'),
    ]

    text = models.TextField()
    language = models.CharField(
        max_length=10,
        choices=LANGUAGE_CHOICES,
        default='en'
    )

    def __str__(self):
        return f"{self.text} ({self.language})"

class Attempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sentence = models.ForeignKey(Sentence, on_delete=models.CASCADE)
    audio_file = models.FileField(upload_to='audio/')
    recognized_text = models.TextField(blank=True)
    score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.score}%"