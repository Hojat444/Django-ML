# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('results/', views.get_topics, name='results'),
    path('analyze_sentiment/', views.analyze_sentiment, name='analyze_sentiment'),


]
