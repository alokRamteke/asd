from django.conf.urls import url
from .views import TopStoriesSentiment

urlpatterns = [
    url(r'sentiment-analysis', TopStoriesSentiment.as_view())
]
