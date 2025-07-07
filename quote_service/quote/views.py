from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, DetailView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
import numpy as np

from .forms import CreateQuoteForm
from .models import Quote, Opinion


PAGINATE_BY = 10


class LikeDislikeMixin:
    '''Миксин для добавления лайков'''
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        quote = self.get_object()
        vote = request.POST.get('vote')
        if vote in ('1', '-1'):
            Opinion.objects.update_or_create(
                user=request.user,
                quote=quote,
                defaults={'value': int(vote)}
            )
        return redirect('quote:random_quote')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        votes = self.get_object().likes.all()
        if self.request.user.is_authenticated:
            try:
                opinion = votes.get(user=self.request.user).value
            except Opinion.DoesNotExist:
                opinion = 0
        else:
            opinion = 0
        context.update(
            {
                'opinion': opinion,
                'likes': votes.filter(value=1).count(),
                'dislikes': votes.filter(value=-1).count()
            }
        )
        return context


class TopQuoteList(ListView):
    model = Quote
    template_name = 'quote/toplist.html'
    paginate_by = PAGINATE_BY
    queryset = Quote.objects.all()


class RandomQuote(LikeDislikeMixin, DetailView):
    model = Quote
    template_name = 'quote/random_quote.html'

    def get_object(self):
        ids, weights = zip(*Quote.objects.values_list('id', 'weight'))
        if not ids:
            return
        weights = np.array(weights, dtype=np.uint8)
        weights = weights / weights.sum()
        random_id = int(np.random.choice(ids, p=weights))
        quote = Quote.objects.get(pk=random_id)
        quote.views += 1
        quote.save()
        return quote

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)


class CreateQuote(LoginRequiredMixin, CreateView):
    model = Quote
    template_name = 'quote/create.html'
    form_class = CreateQuoteForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class QuoteDetail(DetailView):
    model = Quote
    template_name = 'quote/random_quote.html'
    pk_url_kwarg = 'quote_id'
