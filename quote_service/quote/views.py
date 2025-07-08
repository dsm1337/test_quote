from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, CreateView, DetailView, FormView
import numpy as np

from .forms import CreateQuoteForm
from .models import Quote, Opinion


PAGINATE_BY = 10


class LikeDislikeMixin:
    '''Миксин для добавления лайков'''
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        quote_id = request.POST.get('quote_id')
        if not quote_id:
            return redirect('quote:random_quote')

        quote = get_object_or_404(Quote, pk=quote_id)
        vote = request.POST.get('vote')
        if vote not in ('1', '-1'):
            return HttpResponseBadRequest("Некорректное значение vote")
        Opinion.objects.update_or_create(
            user=request.user,
            quote=quote,
            defaults={'value': int(vote)}
        )
        self.object = quote
        return redirect(self.get_success_url())

    def get_success_url(self):
        return self.request.path

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        votes = self.object.likes.all()
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
    template_name = 'quote/quote-random.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_object(self):
        quote_id = self.request.GET.get('quote_id')
        if quote_id:
            return get_object_or_404(Quote, pk=quote_id)

        ids, weights = zip(*Quote.objects.values_list('id', 'weight'))
        if not ids:
            return
        weights = np.array(weights, dtype=np.uint8)
        weights = weights / weights.sum()
        random_id = int(np.random.choice(ids, p=weights))
        quote = Quote.objects.get(pk=random_id)
        quote.views += 1
        quote.save(update_fields=['views'])
        return quote

    def get_success_url(self):
        return f'{reverse('quote:random_quote')}?quote_id={self.object.id}'


class CreateQuote(LoginRequiredMixin, CreateView):
    model = Quote
    template_name = 'quote/create.html'
    form_class = CreateQuoteForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class QuoteDetail(LikeDislikeMixin, DetailView):
    model = Quote
    template_name = 'quote/quote-detail.html'
    pk_url_kwarg = 'quote_id'

    def get_success_url(self):
        return reverse(
            'quote:quote_detail',
            kwargs={self.pk_url_kwarg: self.get_object().pk}
        )
