from django.shortcuts import render
from textblob import TextBlob
from googletrans import Translator
from googletrans import LANGUAGES
from collections import Counter
import re
from transformers import pipeline,AutoTokenizer
import PyPDF2
from newspaper import Article
from django.http import JsonResponse

import os

def index(request):
    return render(request, 'index.html')  



def sentiment_analysis(request):
    sentiment = None
    sentiment_value = None
    text = ""
    
    if request.method == "POST":
        text = request.POST.get('text')
        blob = TextBlob(text)
        sentiment_value = blob.sentiment.polarity
        if sentiment_value > 0:
             sentiment = "Positive"
        elif sentiment_value < 0:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"
    
    return render(request, 'sentiment_analysis.html', {
        'feature': 'Sentiment Analysis',
        'sentiment': sentiment,
        'sentiment_value': sentiment_value,
        'text': text,
    })


def language_translation(request):
   
   
    languages = LANGUAGES
    
    translated_text = None
    target_language = 'en'  
    text = ""

    if request.method == "POST":
        # Get the form data
        text = request.POST.get("text", "")
        target_language = request.POST.get("language", "en")  
        
        if text.strip():  
            translator = Translator()
            translated_text = translator.translate(text, dest=target_language).text

    context = {
        "text": text,
        "translated_text": translated_text,
        "target_language": target_language,
        "languages": languages,  
    }
    return render(request, "language_translator.html", context)


def text_analytics(request):
    analytics = {}
    text = ""
    
    if request.method == "POST":
        text = request.POST.get("text", "")
        
        # Perform text analytics
        word_count = len(re.findall(r'\b\w+\b', text))
        char_count = len(text)
        sentences = re.split(r'[.!?]+', text)
        sentence_count = len([s for s in sentences if s.strip()])
        avg_sentence_length = word_count / sentence_count if sentence_count else 0
        word_freq = Counter(re.findall(r'\b\w+\b', text.lower()))
        most_common_words = word_freq.most_common(5)

     
        analytics = {
            "word_count": word_count,
            "char_count": char_count,
            "sentence_count": sentence_count,
            "avg_sentence_length": avg_sentence_length,
            "most_common_words": most_common_words,
        }

    return render(request, "text_analytics.html", {"analytics": analytics, "text": text})



summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")

def chunk_text(text, max_tokens=1024):
    """Chunk the input text into smaller parts with a maximum token length."""
    tokens = tokenizer.encode(text, truncation=False)  
    chunks = []

    # Split the text into manageable chunks
    for i in range(0, len(tokens), max_tokens):
        chunk = tokenizer.decode(tokens[i:i + max_tokens], skip_special_tokens=True)  
        if chunk.strip():  
            chunks.append(chunk)

    return chunks

def summarize_large_text(text):
    """Summarize large text by splitting it into chunks and summarizing each chunk."""
   
    chunks = chunk_text(text)
    if not chunks:
        return "The text provided is empty or invalid."

    partial_summaries = []

  
    for chunk in chunks:
        try:
            summary = summarizer(chunk, max_length=256, min_length=40, do_sample=False)[0]['summary_text']
            partial_summaries.append(summary)
        except Exception as e:
            print(f"Error summarizing chunk: {e}")

   
    combined_summary = " ".join(partial_summaries)
    if len(tokenizer.encode(combined_summary)) > 1024:  
        final_summary = summarizer(combined_summary, max_length=256, min_length=50, do_sample=False)[0]['summary_text']
    else:
        final_summary = combined_summary

    return final_summary

def extract_text_from_pdf(pdf_file, max_pages=5):
    """Extract text from the first N pages of the PDF."""
    try:
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page_num in range(min(max_pages, len(reader.pages))):
            text += reader.pages[page_num].extract_text() or ""
        return text
    except Exception as e:
        return f"Error reading PDF: {e}"

def extract_text_from_url(url):
    """Extract text from the provided URL using newspaper3k."""
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except Exception as e:
        return f"Error fetching article: {e}"
    



def summarize_text(request):
    """Handle text summarization based on user input with error handling."""
    summary = ""
    error = ""

    if request.method == "POST":
        try:
            action = request.POST.get("action", "").strip()
            text = request.POST.get("text", "").strip()
            pdf_file = request.FILES.get("pdf_file")
            url = request.POST.get("url", "").strip()

            if action == "summarize_text" and text:
                if len(text.split()) < 10: 
                    error = "The input text is too short to summarize. Please provide more content."
                else:
                    summary = summarize_large_text(text)
            
            elif action == "summarize_pdf" and pdf_file:
                try:
                    pdf_text = extract_text_from_pdf(pdf_file)
                    if pdf_text.strip():
                        summary = summarize_large_text(pdf_text)
                    else:
                        error = "Failed to extract text from the uploaded PDF. It might be empty or contain unsupported content."
                except Exception as e:
                    error = f"An error occurred while processing the PDF: {str(e)}"
            
            elif action == "summarize_url" and url:
                if "youtube" in url.lower():
                    error = "Summarization of YouTube videos is not supported."
                else:
                    try:
                        url_text = extract_text_from_url(url)
                        if url_text.strip():
                            summary = summarize_large_text(url_text)
                        else:
                            error = "Failed to extract text from the provided URL. Please ensure it contains valid content."
                    except Exception as e:
                        error = f"An error occurred while extracting text from the URL: {str(e)}"
            
            else:
                error = "Invalid action or input. Please check your submission."
        
        except Exception as e:
            error = f"An unexpected error occurred: {str(e)}"

    return render(request, "summarize.html", {"summary": summary, "error": error})






def save_editor_content(request):
    return render(request, "text_editor.html")
