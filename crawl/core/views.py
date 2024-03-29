from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from textblob import TextBlob
import cv2
import numpy as np
from django.core.files.storage import FileSystemStorage
def index(request):
    return render(request, 'index.html')


@csrf_exempt
def get_topics(request):
    if request.method == 'POST':
        url = request.POST.get('url')

        # Scrape the content of the webpage
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        text = soup.get_text()

        # Perform topic modeling on the text using LDA
        vectorizer = CountVectorizer(stop_words='english', max_df=1.0, min_df=1)
        X = vectorizer.fit_transform([text])
        lda = LatentDirichletAllocation(n_components=5, max_iter=5, learning_method='online', learning_offset=50., random_state=0)
        lda.fit(X)

        # Get the top words for each topic
        feature_names = list(vectorizer.vocabulary_.keys())

        topic_words = []
        for topic_idx, topic in enumerate(lda.components_):
            top_words = [feature_names[i] for i in topic.argsort()[:-11:-1]]
            topic_words.append({'topic': f'Topic {topic_idx+1}', 'words': top_words})

        # Render the results page with the top words for each topic
        context = {'topic_words': topic_words}
        return render(request, 'results.html', context)

    else:
        return HttpResponse('Invalid request method.')
    
    
    

def analyze_sentiment(request):
    if request.method == 'POST':
        product_url = request.POST['text']
        response = requests.get(product_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        comments = []
        sentiment_score = []
        comment_elements = soup.find_all('div', class_='fdbk-container__details__comment')
        for comment_element in comment_elements:
            comment_text = comment_element.text.strip()
            comments.append(comment_text)
            sentiment_score.append(analyze_comments_sentiment(comments))
        
        
        sentiment_label = []
        
        
        for i in sentiment_score:
            
            if i < -0.2:
                sentiment_label.append('منفی')
            elif i> 0.2:
                sentiment_label.append('مثبت')
            else:
                sentiment_label.append('خنثی')
        
        
        return render(request, 'sentiment.html', {'sentiment_score': sentiment_score, 'sentiment_label': sentiment_label, 'comments': comments})
    else:
        return render(request, 'sentiment.html')

def analyze_comments_sentiment(comments):
    blob = TextBlob('\n'.join(comments))
    return blob.sentiment.polarity


