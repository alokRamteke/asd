from django.conf.urls import url
from .views import TopStoriesSentiment, searching, search_result

urlpatterns = [
    url(r'sentiment-analysis', TopStoriesSentiment.as_view()),
    url(r'^search-result/searching/$', searching, name="searching"),
    url(r'^search-result/$', search_result, name="search_result"),
]
