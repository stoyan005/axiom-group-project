from django import forms
from django.contrib.auth.models import User
from .models import Message


class ComposeMessageForm(forms.ModelForm):
    """
    Form for composing a new message or editing a draft.
    Recipients are selected from all active users (excluding the sender).
    """
    recipients = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(is_active=True),
        widget=forms.SelectMultiple(attrs={
            'class': 'form-select',
            'size': '6',
        }),
        help_text='Hold Ctrl / Cmd to select multiple recipients.'
    )

    class Meta:
        model = Message
        fields = ['recipients', 'subject', 'body']
        widgets = {
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Subject...',
                'maxlength': 255,
            }),
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 12,
                'placeholder': 'Write your message here...',
            }),
        }

    def __init__(self, *args, current_user=None, **kwargs):
        super().__init__(*args, **kwargs)
        # Exclude the sender from recipient choices
        if current_user:
            qs = User.objects.filter(is_active=True).exclude(pk=current_user.pk)
            self.fields['recipients'].queryset = qs.order_by('first_name', 'last_name')

        # Show "Full Name (username)" in the dropdown
        self.fields['recipients'].label_from_instance = lambda u: (
            f"{u.get_full_name()} ({u.username})" if u.get_full_name().strip() else u.username
        )
