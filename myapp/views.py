from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from googletrans import Translator
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import nltk
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.views import generic


try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')



def login_decarator(func):
    return login_required(func, login_url='login_page')


@login_decarator
def logout_page(request):
    logout(request)
    return redirect('login_page')


def login_page(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, password=password, username=username)

        if user is not None:
            login(request, user)
            return redirect("home_page")

    return render(request, 'login.html')


@login_decarator
def home_page(request):
    return render(request, 'index.html')



class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('home_page')
    template_name = "signup.html"


@login_decarator
def index(request):
    result = None
    original_text = ""
    translator = Translator()

    if request.method == 'POST':
        original_text = request.POST.get('user_text', '')
        select_lang = request.POST.get('target_lang')
        action = request.POST.get('action')


        if original_text.strip():  # Matn bo'sh emasligini tekshirish
            try:
                if action == 'translate':
                    # Matnni ingliz tiliga tarjima qilish
                    translation = translator.translate(original_text, dest=select_lang)
                    result = translation.text


                elif action == 'summarize':
                    # Sumy orqali qisqacha mazmun yaratish
                    parser = PlaintextParser.from_string(original_text, Tokenizer("english"))
                    summarizer = LsaSummarizer()

                    # Matndan eng muhim 3 ta gapni tanlab oladi
                    summary = summarizer(parser.document, 3)

                    result_list = [str(sentence) for sentence in summary]
                    result = " ".join(result_list)

                    if not result:
                        result = "Matn juda qisqa, qisqartirish uchun kamida bir necha gap yozing."

            except Exception as e:
                result = f"Xatolik yuz berdi: {str(e)}"
        else:
            result = "Iltimos, avval matn kiriting!"

    return render(request, 'index.html', {
        'result': result,
        'original_text': original_text

    })
