from django.shortcuts import render

# Create your views here.
import os
import speech_recognition as sr
import Levenshtein

from django.shortcuts import render
from django.http import JsonResponse
from .models import Sentence, Attempt


from django.shortcuts import render
from .models import Sentence


from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def signup_view(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        confirm = request.POST['confirm']

        if password != confirm:
            messages.error(request, "Passwords do not match")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('signup')

        user = User.objects.create_user(username=username, password=password)
        login(request, user)

        return redirect('home')

    return render(request, 'signup.html')


def login_view(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid login")

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')

def home(request):
    sentences = Sentence.objects.all()

    sentence_id = request.GET.get("sentence_id")

    if sentence_id:
        sentence = Sentence.objects.get(id=sentence_id)
    else:
        sentence = sentences.first()

    return render(request, 'home.html', {
        'sentence': sentence,
        'sentences': sentences
    })

import os
import speech_recognition as sr
import Levenshtein
from pydub import AudioSegment
from django.http import JsonResponse
from .models import Sentence

def upload_audio(request):

    if request.method == "POST":
        try:

            audio_file = request.FILES.get('audio')
            sentence_id = request.POST.get("sentence_id")

            sentence = Sentence.objects.get(id=int(sentence_id))

            print("Sentence:", sentence.text)
            print("Language:", sentence.language)

            webm_path = "temp.webm"
            with open(webm_path, "wb") as f:
                for chunk in audio_file.chunks():
                    f.write(chunk)

            wav_path = "temp.wav"
            sound = AudioSegment.from_file(webm_path, format="webm")
            sound.export(wav_path, format="wav")

            recognizer = sr.Recognizer()

            with sr.AudioFile(wav_path) as source:
                audio = recognizer.record(source)

            language_map = {
                "en": "en-US",
                "ar": "ar-SA",
                "fr": "fr-FR",
                "es": "es-ES",
            }

            lang_code = language_map.get(sentence.language, "en-US")

            print("Recognizer language:", lang_code)

            try:
                recognized_text = recognizer.recognize_google(audio, language=lang_code)
            except Exception as e:
                print("Speech recognition error:", e)
                recognized_text = ""

            score = Levenshtein.ratio(
                sentence.text.lower(),
                recognized_text.lower()
            ) * 100

            return JsonResponse({
                "recognized_text": recognized_text,
                "score": round(score, 2)
            })

        except Exception as e:
            print("SERVER ERROR:", e)
            return JsonResponse({"error": str(e)}, status=500)
    
from django.shortcuts import render, redirect
from .forms import SentenceForm


def add_sentence(request):
    if request.method == "POST":
        form = SentenceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect after saving
    else:
        form = SentenceForm()

    return render(request, 'add_sentence.html', {'form': form})

from django.contrib.auth.decorators import login_required

@login_required
def home(request):

    sentences = Sentence.objects.all()
    sentence_id = request.GET.get("sentence_id")

    if sentence_id:
        sentence = Sentence.objects.get(id=sentence_id)
    else:
        sentence = sentences.first()

    return render(request, 'home.html', {
        'sentence': sentence,
        'sentences': sentences
    })

from django.shortcuts import get_object_or_404


def sentence_list(request):
    sentences = Sentence.objects.all().order_by('-id')

    return render(request, 'sentence_list.html', {
        'sentences': sentences
    })


def update_sentence(request, pk):

    sentence = get_object_or_404(Sentence, pk=pk)

    if request.method == "POST":
        form = SentenceForm(request.POST, instance=sentence)
        if form.is_valid():
            form.save()
            return redirect('sentence_list')
    else:
        form = SentenceForm(instance=sentence)

    return render(request, 'add_sentence.html', {'form': form})


def delete_sentence(request, pk):

    sentence = get_object_or_404(Sentence, pk=pk)

    sentence.delete()

    return redirect('sentence_list')