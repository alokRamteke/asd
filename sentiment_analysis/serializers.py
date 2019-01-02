from rest_framework import serializers


class TopStoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopStories
        fields = '__all__'
