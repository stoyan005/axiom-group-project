
from django import forms
from django.contrib.auth.models import User
from .models import Message


class ComposeMessageForm(forms.ModelForm):

    # ModelMultipleChoiceField allows more than one recipient to be selected.
    recipients = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(is_active=True),
        widget=forms.SelectMultiple(attrs={
            'class': 'form-select',
            'size': '6',
        }),
        help_text='Hold Ctrl / Cmd to select multiple recipients.'
    )

    class Meta:
        # This form creates/updates Message objects.
        model = Message
        fields = ['recipients', 'subject', 'body']
        widgets = {
            # Bootstrap classes are applied here so every template using the form
            # automatically gets the correct styling.
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

        if current_user:
            # Only active users are shown and the sender is excluded.
            qs = User.objects.filter(is_active=True).exclude(pk=current_user.pk)
            self.fields['recipients'].queryset = qs.order_by('first_name', 'last_name')

        # Show a human-friendly label in the recipient dropdown.
        self.fields['recipients'].label_from_instance = lambda u: (
            f"{u.get_full_name()} ({u.username})" if u.get_full_name().strip() else u.username
        )
