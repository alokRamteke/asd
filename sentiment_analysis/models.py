from django.db import models
from .search import TopStoriesIndex


class TopStories(models.Model):

    title = models.CharField(max_length=100, blank=True)
    by = models.CharField(max_length=30, blank=True)
    sentiment = models.CharField(max_length=10, blank=True)
    url = models.URLField(blank=True)
    score = models.IntegerField(blank=True)

    def __str__(self):
        return self.title


    def indexing(self):
       obj = TopStoriesIndex(
          meta={'id': self.id},
          title=self.title,
          by=self.by,
          sentiment=self.sentiment,
          score=self.score,
       )
       obj.save()
       return obj.to_dict(include_meta=True)

    def save(self, *args, **kwargs):
        is_new = self.pk
        super(TopStories, self).save(*args, **kwargs)
        payload = self.es_repr()
        if is_new is not None:
            del payload['_id']
            es_client.update(
                index=self._meta.es_index_name,
                doc_type=self._meta.es_type_name,
                id=self.pk,
                refresh=True,
                body={
                    'doc': payload
                }
            )
        else:
            es_client.create(
                index=self._meta.es_index_name,
                doc_type=self._meta.es_type_name,
                id=self.pk,
                refresh=True,
                body={
                    'doc': payload
                }
            )
    def delete(self, *args, **kwargs):
        prev_pk = self.pk
        super(TopStories, self).delete(*args, **kwargs)
        es_client.delete(
            index=self._meta.es_index_name,
            doc_type=self._meta.es_type_name,
            id=prev_pk,
            refresh=True,
        )