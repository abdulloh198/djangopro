from django.shortcuts import render
from googletrans import Translator

# Sumy kutubxonasi uchun kerakli qismlar
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import nltk

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')




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
                    # O'zbek tili uchun ham 'english' tokenizeridan foydalanamiz (nuqta va vergulga qarab ajratadi)
                    parser = PlaintextParser.from_string(original_text, Tokenizer("english"))
                    summarizer = LsaSummarizer()

                    # Matndan eng muhim 2 ta gapni tanlab oladi
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