from django import forms
from .models import Issue, Project
from django.core.exceptions import ValidationError

RESTRICTED_SYMBOLS = ['{', '}', '/', '^', '|']


def restricted_symbols(string):
    for i in RESTRICTED_SYMBOLS:
        if i in string:
            raise ValidationError(f'"{i}" should not include title!')


class XDatepickerWidget(forms.TextInput):
    template_name = 'widgets/xdatepicker_widget.html'


class IssueForm(forms.ModelForm):
    title = forms.CharField(max_length=200, required=True, label='Title', validators=(restricted_symbols,))
    description = forms.CharField(max_length=2000, required=False, label="Description",
                                  widget=forms.Textarea)

    class Meta:
        model = Issue
        fields = ['title', 'description', 'status', 'type']
        widgets = {'type': forms.CheckboxSelectMultiple}

    def clean(self):
        cleaned_data = super().clean()
        errors = []
        title = cleaned_data.get('title')
        description = cleaned_data.get('description')
        if len(title) > len(description):
            errors.append(ValidationError('Text of the title should not be longer than the description!'))
        if errors:
            raise ValidationError(errors)
        return cleaned_data


class SimpleSearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label="Search")


class ProjectForm(forms.ModelForm):
    start_date = forms.DateField(required=True, label='Start Date', input_formats=['%Y-%m-%d'],
                                 widget=XDatepickerWidget)
    end_date = forms.DateField(required=False, label='End Date', input_formats=['%Y-%m-%d'],
                               widget=XDatepickerWidget)

    class Meta:
        model = Project
        fields = ['name', 'description', 'start_date', 'end_date']
