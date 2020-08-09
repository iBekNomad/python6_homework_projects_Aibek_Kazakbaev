from django import forms
from .models import Issue, Type, Status


class IssueForm(forms.Form):
    title = forms.CharField(max_length=200, required=True, label='Title')
    description = forms.CharField(max_length=2000, required=True, label="Description",
                                  widget=forms.Textarea)
    status = forms.ModelChoiceField(queryset=Status.objects.all(), required=True, initial='New', label='Status')
    type = forms.ModelChoiceField(queryset=Type.objects.all(), required=True, label='Type')


class IssueStatusForm(forms.Form):
    status = forms.CharField(max_length=40, required=True, label='Status')


class IssueTypeForm(forms.Form):
    type = forms.CharField(max_length=40, required=True, label='Type')
