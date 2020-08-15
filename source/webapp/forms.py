from django import forms
from .models import Issue
from django.core.exceptions import ValidationError

RESTRICTED_SYMBOLS = ['{', '}', '/', '^', '|']


def restricted_symbols(string):
    for i in RESTRICTED_SYMBOLS:
        if i in string:
            raise ValidationError(f'"{i}" should not include title!')


class IssueForm(forms.ModelForm):
    title = forms.CharField(max_length=200, required=True, label='Title', validators=(restricted_symbols,))
    description = forms.CharField(max_length=2000, required=False, label="Description",
                                  widget=forms.Textarea)

    class Meta:
        model = Issue
        fields = ['title', 'description', 'status', 'type']

    def clean(self):
        cleaned_data = super().clean()
        errors = []
        title = cleaned_data.get('title')
        description = cleaned_data.get('description')
        if title > description:
            errors.append(ValidationError('Text of the title should not be longer than the description!'))
        if errors:
            raise ValidationError(errors)
        return cleaned_data


class SimpleSearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label="Search")
