from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView
import numpy as np 

from .models import Quote


PAGINATE_BY = 10


class TopQuoteList(ListView):
    model = Quote
    template_name = 'quote/toplist.html'
    paginate_by = PAGINATE_BY
    queryset = Quote.objects.all()


class RandomQuote(DetailView):
    model = Quote
    template_name = 'quote/random_quote.html'

    def get_object(self):
        ids, weights = zip(*Quote.objects.values_list('id', 'weight'))
        if not ids:
            return
        weights = np.array(weights, dtype=np.uint8)
        weights = weights / weights.sum()
        random_id = np.random.choice(ids, p=weights)
        return Quote.objects.get(pk=random_id)
