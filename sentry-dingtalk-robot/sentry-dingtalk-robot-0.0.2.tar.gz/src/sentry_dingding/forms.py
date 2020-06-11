# coding: utf-8

from django import forms


class DingDingOptionsForm(forms.Form):
    access_token = forms.CharField(
        max_length=255,
        help_text='DingTalk robot access_token'
    )
    title = forms.CharField(
        max_length=255,
        initial="New alert from {name}",
        help_text='DingTalk robot message title {name}'
    )
    content = forms.Textarea(
        max_length=1000,
        initial="#### {title} \n > {message} [href]({url})",
        help_text='DingTalk robot message content (markdown) {title, message, url}'
    )