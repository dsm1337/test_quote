from django import forms

from .models import Quote, Source, WorkType


class CreateQuoteForm(forms.ModelForm):
    source = forms.ModelChoiceField(
        queryset=Source.objects.all(), required=False, label='Источник'
    )
    added_source = forms.CharField(
        max_length=100, required=False, label='Новый источник'
    )
    added_source_type = forms.ModelChoiceField(
        queryset=WorkType.objects.all(),
        required=False,
        label='Тип произведения'
    )
    weight = forms.IntegerField(min_value=1, max_value=100, label='Вес')

    class Meta:
        model = Quote
        fields = (
            'text', 'weight', 'source', 'added_source', 'added_source_type'
        )

    def clean(self):
        cleaned_data = super().clean()
        source = cleaned_data.get('source')
        new_source = cleaned_data.get('added_source')
        new_source_type = cleaned_data.get('added_source_type')

        if not source and (not new_source or not new_source_type):
            raise forms.ValidationError(
                'Укажите источник!'
            )

        if new_source:
            if Source.objects.filter(
                title__iexact=new_source.strip(), source_type=new_source_type
            ).exists():
                raise forms.ValidationError(
                    'Такой источник уже существует! Выберите из предложенных'
                )

    def save(self):
        source = self.cleaned_data.get('source')
        new_source = self.cleaned_data.get('added_source')
        new_source_type = self.cleaned_data.get('added_source_type')
        if new_source:
            source_obj = Source.objects.create(
                title=new_source, source_type=new_source_type
            )
        else:
            source_obj = source
        quote = super().save(commit=False)
        quote.source = source_obj
        quote.save()
        return quote
