from django import forms

class ChatForm(forms.Form):
    user_input=forms.CharField(widget=forms.Textarea)