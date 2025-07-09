from django.urls import path

from .views import TopQuoteList, RandomQuote, QuoteDetail, CreateQuote


app_name = 'quote'
urlpatterns = [
    path('', TopQuoteList.as_view(), name='top_quotes'),
    path('random-quote/', RandomQuote.as_view(), name='random_quote'),
    path('<int:quote_id>/', QuoteDetail.as_view(), name='quote_detail'),
    path('create/', CreateQuote.as_view(), name='create_quote')
]
