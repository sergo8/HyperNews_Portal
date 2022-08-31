from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.conf import settings
from datetime import datetime
from .forms import CreateNewsForm, SearchNewsForm
import random
import json


class MainPaigeView(View):
    def get(self, request,  *args, **kwargs):
        text = '<h2>Coming soon</h2>'
        return redirect('/news/')


class NewsView(View):
    def get(self, request, link,  *args, **kwargs):
        with open(settings.NEWS_JSON_PATH, 'r') as json_file:
            content = json.load(json_file)
            for article in content:
                if article['link'] == link:
                    return render(request, "news/news.html", context={'article': article})

    @staticmethod
    def read_json():
        with open(settings.NEWS_JSON_PATH, 'r') as json_file:
            content = json.load(json_file)
        return content


class AllNewsView(View):
    def get(self, request, *args, **kwargs):
        articles_list = NewsView.read_json()
        articles = []
        form = SearchNewsForm(request.GET)

        for date in articles_list:
            date['created'] = date['created'][0:10]
            articles.append(date)

        q = request.GET.get('q')
        # title_dict = {article['title']: article['link'] for article in articles_list}

        if q:
            filtered_articles = []
            for article in articles:
                if q in article["title"]:
                    filtered_articles.append(article)
            articles = filtered_articles

        return render(request, 'news/all_news.html', context={'articles': articles})


class CreateNewsView(View):
    def get(self, request):
        return render(request, 'news/create.html')

    def post(self, request, *args, **kwargs):
        form = CreateNewsForm(request.POST)

        created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        content = NewsView.read_json()
        list_of_links = [article["link"] for article in content]

        while True:
            link = random.randint(1, 100000)
            if link not in list_of_links:
                if form.is_valid():
                    text = request.POST.get('text')
                    title = request.POST.get('title')
                    content.append({"created": created, "text": text, "title": title, "link": link})
                with open(settings.NEWS_JSON_PATH, 'w') as json_file:
                    json.dump(content, json_file)
                    return redirect('/news/')
            else:
                continue
