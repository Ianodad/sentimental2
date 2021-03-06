from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from .forms import userinput
from . apicall import getdata
from chartjs.views.lines import BaseLineChartView
from . models import SentimentsTwitterHashtag
import datetime


# Create your views here.


def home(request):
    # hall = 'trump'
    # random = getdata(hall)
    # print(random)
    word = "word of the home"
    return render(request, 'home.html', {"word": word})


# class LineChartJSONView(BaseLineChartView):
#     template_name = 'home.html'

#     def get_labels(self):
#         """Return 7 labels for the x-axis."""
#         return ["January", "February", "March", "April", "May", "June", "July"]

#     def get_providers(self):
#         """Return names of datasets."""
#         return ["Central", "Eastside", "Westside"]

#     def get_data(self):
#         """Return 3 datasets to plot."""

#         return [[75, 44, 92, 11, 44, 95, 35],
#                 [41, 92, 18, 3, 73, 87, 92],
#                 [87, 21, 94, 3, 90, 13, 65]]


def analyse(request):
    user_input = userinput(request.GET or None)
    if request.GET and user_input.is_valid():
        input_hastag = user_input.cleaned_data['q']
        # print(input_hastag)
        data = getdata(input_hastag)
        topic = '#' + data['Topic']
        sample = data['Sample']
        positive = data['Positive']
        neutral = data['Neutral']
        negative = data['Negative']
        negative_tweets = data['Nagative_tweets'][0:3]
        neutral_tweets = data['Neutral_tweets'][0:3]
        postive_tweets = data['Postive_tweets'][0:3]

        time_positive = data['time_positive']

        listt = time_positive.keys()
        print(min(listt))
        # print(data['Positive'])
        # print(nagative_tweets)
        # print(data)
        sentiments = SentimentsTwitterHashtag(topic=topic,
                                              sample_size=sample,
                                              postive_count=positive,
                                              neutral_count=neutral,
                                              negative_count=negative,
                                              negative_tweets=negative_tweets,
                                              neutral_tweets=neutral_tweets,
                                              postive_tweets=postive_tweets,
                                              publication_date=datetime.datetime.now()

                                              )
        sentiments.save()
        return render(request, "results.html", {'data': data, 'topic': topic, 'positive': positive, 'sample': sample, 'neutral': neutral, 'negative': negative, 'negative_tweets': negative_tweets, 'neutral_tweets': neutral_tweets, 'postive_tweets': postive_tweets})
    return render(request, "search.html", {'input_hastag': user_input})
