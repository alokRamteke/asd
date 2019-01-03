import requests
import json
from django.shortcuts import render
from rest_framework import views, status
from rest_framework.response import Response
from textblob import TextBlob
from .models import TopStories
from sentiment_analysis.search import *


class TopStoriesSentiment(views.APIView):

    def get_story(self, story_id):
        url = 'https://hacker-news.firebaseio.com/v0/item/{item}.json'.format(item=story_id)
        response = requests.get(url)
        data = response.json()
        if response.status_code == 404:
            return {}
        return data

    def get_story_sentiment(self, title):
        analysis = TextBlob(title)
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def get(self, request):
        
        request.session.set_expiry(300)

        is_cached = ('stories' in request.session)
        try:
            if not is_cached:
                TopStories.objects.all().delete()
                top_10_stories = requests.get(" https://hacker-news.firebaseio.com/v0/topstories.json").json()[:10]
                stories = []
                items = ['title', 'by', 'score','url']
                for story in top_10_stories:
                    story = self.get_story(story)
                    parsed_story = {item:story[item] for item in items if item in story}
                    parsed_story['sentiment'] = self.get_story_sentiment(story['title'])
                    stories.append(parsed_story)
                    TopStories.objects.create(**parsed_story)
                request.session['stories'] = stories

            stories = request.session['stories']

            return Response(stories)
        except:
            return Response({})


def searching(request):
    """
    Basic Searching
    """
    d_list=[]
    data={}
    val=request.GET['val'].lower()
    pdata=search(title=val)
    if pdata:
        for out in pdata:
            title=out.title
            description=out.description
            d_id=out.meta.id
            d_list.append({
                'id':d_id,
                'title':title,
                'description':description,
                })
        data = {'data':list(d_list),'status':'success'}
        return HttpResponse(json.dumps(data),content_type="application/json")
    data = {'message':'Data not found','status':403}
    return HttpResponse(json.dumps(data),content_type="application/json")

def search_result(request):
    """
    """
    if request.method=="POST":
        data=search(title=request.POST['data'].lower())
        return render(request, 'index.html',{ 'data': data })
 
    data_list=TopStories.objects.all()
    # page = request.GET.get('page', 1)
    # paginator = Paginator(data_list, 5)
    # try:
    #     data = paginator.page(page)
    # except PageNotAnInteger:
    #     data = paginator.page(1)
    # except EmptyPage:
    #     data = paginator.page(paginator.num_pages)

    return render(request, 'index.html',{ 'data': data })