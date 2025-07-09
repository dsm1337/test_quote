from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.db.models import Case, IntegerField, Sum, When
from django.urls import reverse
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, DetailView, ListView
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
        current_vote = Opinion.objects.filter(
            user=request.user, quote=quote
        ).first()
        if current_vote and current_vote.value == int(vote):
            current_vote.delete()
        else:
            Opinion.objects.update_or_create(
                user=request.user,
                quote=quote,
                defaults={'value': int(vote)}
            )
        self.object = quote
        if getattr(self, 'use_redirect_on_post', False):
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(
                self.get_context_data(object=self.object)
            )
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
    '''Топ лист цитат'''
    model = Quote
    template_name = 'quote/toplist.html'
    paginate_by = PAGINATE_BY
    queryset = Quote.objects.all()

    def get_queryset(self):
        return Quote.objects.annotate(
            total_likes=Sum(
                Case(
                    When(likes__value=1, then=1),
                    default=0,
                    output_field=IntegerField()
                )
            )
        ).order_by('-total_likes', '-created_at')


class RandomQuote(LikeDislikeMixin, DetailView):
    '''Случайная цитата'''
    model = Quote
    template_name = 'quote/quote-random.html'
    use_redirect_on_post = True

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_object(self):
        quote_id = self.request.GET.get('quote_id')
        if quote_id:
            return get_object_or_404(Quote, pk=quote_id)

        
        try:
            ids, weights = zip(*Quote.objects.values_list('id', 'weight'))
        except ValueError:
            ids, weights = [], []
        if not ids:
            return redirect('quote:top_quotes')
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
    '''Создание цитаты'''
    model = Quote
    template_name = 'quote/create.html'
    form_class = CreateQuoteForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        try:
            return super().form_valid(form)
        except ValidationError as e:
            form.add_error(None, e)
            return self.form_invalid(form)


class QuoteDetail(LikeDislikeMixin, DetailView):
    '''Отедельная цитата'''
    model = Quote
    template_name = 'quote/quote-detail.html'
    pk_url_kwarg = 'quote_id'
    use_redirect_on_post = False

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.views += 1
        self.object.save(update_fields=['views'])
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)
