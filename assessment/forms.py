from django import forms
from .models import Sentence

class SentenceForm(forms.ModelForm):
    class Meta:
        model = Sentence
        fields = ['language', 'text']

        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Type sentence or select suggestion'
            })
        }