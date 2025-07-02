from django.urls import path

from .views import TopQuoteList, RandomQuote


app_name = 'quote'
urlpatterns = [
    path('top-quotes/', TopQuoteList.as_view()),
    path('random-quote/', RandomQuote.as_view())
]
