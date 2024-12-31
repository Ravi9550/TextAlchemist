
from django.urls import path
from . import views  


urlpatterns = [
    path('', views.index, name='index'),  
    path('sentiment_analysis/', views.sentiment_analysis, name='sentiment'),
    path('language_translation/', views.language_translation, name='language_translation'),
    path('text-analytics/', views.text_analytics, name='text_analytics'),
    path('summarize/', views.summarize_text, name='summarize_text'),
    path("editor/", views.save_editor_content, name="editor"),

]
