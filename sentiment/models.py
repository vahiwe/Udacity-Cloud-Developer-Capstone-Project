from django.db import models

# Create your models here.
class Feedbacks(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    feedback = models.TextField()
    twitter_handle = models.CharField(max_length=50)

    class Meta:
        db_table = "feedbacks"

class Tweets(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    tweet = models.TextField()
    twitter_handle = models.CharField(max_length=50)
    tweet_date = models.DateTimeField(null=True)
    likes = models.PositiveIntegerField()
    retweets = models.PositiveIntegerField()

    class Meta:
        db_table = "tweets"
        indexes = [
            models.Index(fields=['tweet', 'twitter_handle', 'tweet_date']),
        ]