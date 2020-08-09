from django import forms
from .models import Issue, Type, Status


class IssueForm(forms.Form):
    title = forms.CharField(max_length=200, required=True, label='Title')
    description = forms.CharField(max_length=2000, required=True, label="Description",
                                  widget=forms.Textarea)
    status = forms.ModelChoiceField(queryset=Status.objects.all(), required=True, initial='New', label='Status')
    type = forms.ModelMultipleChoiceField(queryset=Type.objects.all(), required=True, label='Type',
                                          widget=forms.RadioSelect)
