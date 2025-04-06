from django import forms
from .models import *

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'details', 'category', 'total_target', 'tags', 'start_time', 'end_time']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter campaign title'}),
            'details': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Provide campaign details'}),
            'category': forms.Select(attrs={'class': 'form-control'}, choices=[('', 'Select a category')]),
            'total_target': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter total target amount'}),
            'tags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Comma-separated tags'}),
            'start_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['amount']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter donation amount'})
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Add a comment...'}),
        }