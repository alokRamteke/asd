from django.db import models
from .search import TopStoriesIndex


class TopStories(models.Model):

    story_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=100)
    submitted_by = models.CharField(max_length=30)
    description = models.CharField(max_length=20)
    sentiment = models.CharField(max_length=10)
    score = models.IntegerField()
    url = models.URLField()

    def __str__(self):
        return self.title


    def indexing(self):
       obj = TopStoriesIndex(
          meta={'id': self.id},
          title=self.title,
          submitted_by=self.submitted_by,
          description=self.description,
          score=self.score,
       )
       obj.save()
       return obj.to_dict(include_meta=True)
