from django import forms

from .models import Quote, Source


class CreateQuoteForm(forms.ModelForm):
    source = forms.ModelChoiceField(
        queryset=Source.objects.all(), label='Источник'
    )
    weight = forms.IntegerField(min_value=1, max_value=100, label='Вес')

    class Meta:
        model = Quote
        fields = ('text', 'source', 'weight')
