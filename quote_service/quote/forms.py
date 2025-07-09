from django import forms
from unidecode import unidecode

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

        if not source and not new_source:
            raise forms.ValidationError(
                'Укажите источник!'
            )

        if new_source and not new_source_type:
            raise forms.ValidationError(
                'Укажите тип добавляемого источника!'
            )

        if new_source:
            normalized_title = unidecode(new_source.strip().lower())
            for existing_source in Source.objects.filter(
                source_type=new_source_type
            ):
                if (
                    unidecode(existing_source.title.strip().lower())
                    == normalized_title
                ):
                    raise forms.ValidationError(
                        'Такой источник уже существует! '
                        'Выберите из предложенных'
                    )

        if source and Quote.objects.filter(source=source).count() >= 3:
            raise forms.ValidationError(
                'Нельзя добавлять источнику больше 3 цитат!'
            )
        return cleaned_data

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
