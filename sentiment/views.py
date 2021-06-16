import re
import sys
import tweepy
import random
import datetime
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sentiment.config import *
from annoying.functions import get_object_or_None
from sklearn.externals import joblib
from django.shortcuts import render,  redirect
from sentiment.models import Feedbacks, Tweets
from django.core.files.storage import default_storage
from io import BytesIO

# Use seaborn style defaults and set the default figure size
sns.set(rc={})
# Create your views here.
sent = open('model_setup/model.pkl', 'rb')
clf = joblib.load(sent)

# Run pyplot in backend mode
plt.switch_backend('Agg')

def error_404_view(request, exception):
    return render(request, 'error_404.html')

def error_500_view(request):
    return render(request, 'error_500.html')

def home(request):
    if request.method == 'POST':
        # You need to insert your own developer twitter credentials here
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)

        handle = request.POST['handle']
        handle = str(handle)
        request.session['user'] = handle

        if '@' in handle:
            report = "Sorry input your twitter handle without the '@' sign"
            return render(request, 'home.html', {'report': report})

        try:
            api.user_timeline(id=handle, count=1)
            report = "This username is available on Twitter"
        except tweepy.error.TweepError:
            report = "This username is not on Twitter"

        if report == "This username is available on Twitter":
            request.session['user'] = handle
            return redirect('analysis/')
        else:
            return render(request, 'home.html', {'report': report})
    return render(request, 'home.html', {'report': ''})


def analysis(request):
    previous_url = request.META.get('HTTP_REFERER')
    if previous_url == None:
        return redirect('/')
    if request.method == 'POST':
        # You need to insert your own developer twitter credentials here
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
        handle = request.POST['handle']
        handle = str(handle)
        start = request.POST['start']
        start = str(start)
        end = request.POST['end']
        end = str(end)
        try:
            date_since_obj = datetime.datetime.strptime(start, '%Y-%m-%d')
            date_after_obj = datetime.datetime.strptime(end, '%Y-%m-%d')
        except ValueError:
            report = "Please input duration"
            return render(request, 'analysis.html', {'report': report, 'user': handle})

        tweets = tweepy.Cursor(api.user_timeline, id=handle, lang='en',
                               tweet_mode='extended', since='', until='').items(200)

        non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0x0020)
        dates = []
        test = []
        likes = []
        retweets = []
        bulk_object_create = []
        for tweet in tweets:
            if tweet.created_at < date_after_obj and tweet.created_at > date_since_obj:
                full_date = tweet.created_at
                date = full_date.strftime("%Y-%m-%d")
                like = tweet.favorite_count
                retweet = tweet.retweet_count
                status = tweet
                if 'extended_tweet' in status._json:
                    status_json = status._json['extended_tweet']['full_text']
                elif 'retweeted_status' in status._json and 'extended_tweet' in status._json['retweeted_status']:
                    status_json = status._json['retweeted_status']['extended_tweet']['full_text']
                    like = status._json["retweeted_status"]["favorite_count"]
                elif 'retweeted_status' in status._json:
                    status_json = status._json['retweeted_status']['full_text']
                    like = status._json["retweeted_status"]["favorite_count"]
                else:
                    status_json = status._json['full_text']
                cleaned_tweet = status_json.translate(non_bmp_map) 
                test.append(cleaned_tweet)
                likes.append(like)
                retweets.append(retweet)
                dates.append(date)
                db_tweet = get_object_or_None(Tweets, tweet=cleaned_tweet, twitter_handle=handle, tweet_date=full_date)
                if db_tweet is None:
                    bulk_object_create.append(Tweets(
                        tweet=cleaned_tweet, 
                        likes=like, 
                        retweets=retweet,
                        twitter_handle=handle,
                        tweet_date=full_date
                    ))


        df = pd.DataFrame(list(zip(test, dates, likes, retweets)), columns=[
                          "tweets", "dates", "likes", "retweets"])
        df['dates'] = pd.to_datetime(df['dates'], format='%Y-%m-%d')
        df.set_index(['dates'], inplace=True)
        df.sort_index(inplace=True)

        # check if dataframe is empty
        if df.empty:
            report = "Sorry you don't have any tweets within this period"
            return render(request, 'analysis.html', {'report': report, 'user': handle})

        # check if number of tweets are up to 10
        if df.shape[0] < 11:
            report = "Sorry you don't have enough tweets within this period"
            return render(request, 'analysis.html', {'report': report, 'user': handle})

        # Save tweets to db
        if len(bulk_object_create) > 0:
            Tweets.objects.bulk_create(bulk_object_create)  
        
        # remove twitter handles (@user)
        df['tidy_tweet'] = np.vectorize(remove_pattern)(df['tweets'], "@[\w]*")
        # remove url patterns
        df['tidy_tweet'] = np.vectorize(remove_pattern)(
            df['tidy_tweet'], "http[s]?://\S+")
        # remove 'RT', '#', newline escape character '\n' and trailing whitespaces
        df['tidy_tweet'] = df['tidy_tweet'].str.replace("RT", " ")
        df['tidy_tweet'] = df['tidy_tweet'].str.replace("#", " ")
        df['tidy_tweet'] = df['tidy_tweet'].str.replace("\n", " ")
        df['tidy_tweet'] = np.vectorize(
            remove_pattern)(df['tidy_tweet'], "\s\s+")
        # replace empty strings with NaN
        df['tidy_tweet'].replace('', np.nan, inplace=True)
        # remove rows with NaN in tidy tweet column
        df = df.dropna(subset=['tidy_tweet'])

        # predict
        predicted = clf.predict(df['tidy_tweet'])
        df['mood'] = predicted

        # this changes the labels of the prediction
        df['mood'] = df['mood'].map({4: 1, 0: -1, 2: 0})

        neutral_percentage = (len(df[df['mood'] == 0]) / len(df['mood'])) * 100
        negative_percentage = (
            len(df[df['mood'] == -1]) / len(df['mood'])) * 100
        positive_percentage = (
            len(df[df['mood'] == 1]) / len(df['mood'])) * 100

        labels = ['neutral', 'negative', 'positive']
        sizes = [neutral_percentage, negative_percentage, positive_percentage]
        moodto = dict(zip(labels, sizes))
        moodsort = sorted(moodto.items(), key=lambda x: x[1], reverse=True)

        negative_response = ["Don't be too negative, Add some positivity to your tweets.", "Dilute your tweets with some positivity.", "Once you replace negative thoughts with positive ones, you’ll start having positive results.",
                             "Positive thinking will let you do everything better than negative thinking will.", "Being negative is like sliding down a hill. Being positive is like going up a mountain."]
        positive_response = ["Positivity is great. Positive emotions enhance your life.", "In every day, there are 1,440 minutes. That means we have 1,440 daily opportunities to make a positive impact. Keep being positive",
                             "Positive things happen to positive people.", "All You can control is yourself and just keep having a positive attitude.", "Your positive action combined with positive thinking results in success."]
        neutral_response = ["Neutral is good, But you might want to add some emotion to your tweets.", "Looks like you don't like picking sides",
                            "You keep your emotions in check.", "Looks like you have everything balanced", "You're keeping a well balanced life."]

        random.seed(a=None)
        picked = random.randint(0, 4)
        if moodsort[0][0] == "positive":
            response = positive_response[picked]
        elif moodsort[0][0] == "negative":
            response = negative_response[picked]
        elif moodsort[0][0] == "neutral":
            response = neutral_response[picked]

        # Piechart
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=False)
        ax1.axis('equal')
        plt.title('Moods Composition from ' + date_since_obj.strftime("%A, %d %b %Y") +
                  "\n to " + date_after_obj.strftime("%A, %d %b %Y"))
        
        # Save to file using default plotly function
        # plt.savefig('static/piechart.png', bbox_inches='tight')

        # Use django default media storage to save image
        piechart = BytesIO()
        plt.savefig(piechart, bbox_inches='tight', format='png')
        piechartpath = default_storage.save(f'{handle}-{datetime.datetime.now().isoformat()}-piechart.png', piechart)
        piechartpath = default_storage.url(piechartpath)

        # Specify the data columns we want to include
        data_columns = ['mood']
        # Resample to daily frequency, aggregating with mean
        mood_daily_mean = df[data_columns].resample('D').mean()
        # graph for daily
        ax = mood_daily_mean.plot(
            ylim=(-0.5, 0.5), title='Mood on different days')
        # set labels for both axes
        ax.set(xlabel='Days', ylabel='Mood')
        a = ['', 'Very Negative', 'Negative',
             'Neutral', 'Positive', 'Very Positive', '']
        ax.set_yticklabels(a)

        # Save to file using default plotly function
        # plt.savefig("static/daygraph.png", bbox_inches='tight')

        # Use django default media storage to save image
        daygraph = BytesIO()
        plt.savefig(daygraph, bbox_inches='tight', format='png')
        daygraphpath = default_storage.save(f'{handle}-{datetime.datetime.now().isoformat()}-daygraph.png', daygraph)
        daygraphpath = default_storage.url(daygraphpath)

        # highest retweet and like
        high_retweet = df.loc[df['retweets'] ==
                              df['retweets'].max()]['tweets'][0]
        high_like = df.loc[df['likes'] == df['likes'].max()]['tweets'][0]

        request.session['pie'] = piechartpath
        request.session['daily'] = daygraphpath
        request.session['highretweets'] = high_retweet
        request.session['highlikes'] = high_like
        request.session['response'] = response
        request.session['user'] = handle
        return redirect('/feedback')
    user = request.session.get('user')
    return render(request, 'analysis.html', {'report': '', 'user': user, })


def feedback(request):
    previous_url = request.META.get('HTTP_REFERER')
    if previous_url == None:
        return redirect('/')
    if request.method == 'POST':
        handle = request.POST['handle']
        handle = str(handle)
        message = request.POST['message']
        # Save feedback to DB
        Feedbacks.objects.create(
            feedback=message,
            twitter_handle=handle
        )

        # writing feedback to file
        # message = handle + "," + str(message)
        # feedback = open("feedback.txt", "a+")
        # feedback.write(message+"\n\n")
        # feedback.close()
        return redirect('/')
    piechart = request.session.get('pie')
    dailygraph = request.session.get('daily')
    high_retweet = request.session.get('highretweets')
    high_like = request.session.get('highlikes')
    response = request.session.get('response')
    user = request.session.get('user')
    return render(request, 'feedback.html', {'piechart': piechart, 'dailygraph': dailygraph, 'high_retweet': high_retweet, 'high_like': high_like, 'response': response, 'user': user})


def remove_pattern(input_txt, pattern):
    r = re.findall(pattern, input_txt)
    for i in r:
        input_txt = re.sub(i, '', input_txt)

    return input_txt
