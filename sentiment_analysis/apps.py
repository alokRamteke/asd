from django.apps import AppConfig


class SentimentAnalysisConfig(AppConfig):
    name = 'sentiment_analysis'

    def ready(self):
        import sentiment_analysis.signals
