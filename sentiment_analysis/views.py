import requests
import json
from django.shortcuts import render
from rest_framework import views, status
from rest_framework.response import Response
from textblob import TextBlob
from .models import TopStories


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
        try:
            is_cached = ('stories' in request.session)

            if not is_cached:
                TopStories.objects.all().delete()
                top_10_stories = requests.get(" https://hacker-news.firebaseio.com/v0/topstories.json").json()[:10]
                stories = []
                for story in top_10_stories:

                    parsed_story = {}
                    story = self.get_story(story)
                    parsed_story['sentiment'] = self.get_story_sentiment(story['title'])
                    parsed_story['story_id'] = story['id']
                    parsed_story['submitted_by'] = story['by']
                    parsed_story['score'] = story['score']
                    parsed_story['title'] = story['title']
                    parsed_story['url'] = story['url']
                    parsed_story['description'] = story['type']
                    stories.append(parsed_story)
                    TopStories.objects.create(**parsed_story)
                request.session['stories'] = stories

            stories = request.session['stories']

            return Response(stories)
        except:
            return Response({})
