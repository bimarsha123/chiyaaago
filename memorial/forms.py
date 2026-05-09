from django import forms
from .models import ContactSubmission


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactSubmission
        fields = ["name", "email", "subject", "message"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "w-full px-4 py-3 rounded-xl bg-ember-surface ring-1 ring-white/10 text-white placeholder-white/30 focus:outline-none focus:ring-ember-primary/50 transition-all duration-300",
                    "placeholder": "Your Name",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "w-full px-4 py-3 rounded-xl bg-ember-surface ring-1 ring-white/10 text-white placeholder-white/30 focus:outline-none focus:ring-ember-primary/50 transition-all duration-300",
                    "placeholder": "Your Email",
                }
            ),
            "subject": forms.TextInput(
                attrs={
                    "class": "w-full px-4 py-3 rounded-xl bg-ember-surface ring-1 ring-white/10 text-white placeholder-white/30 focus:outline-none focus:ring-ember-primary/50 transition-all duration-300",
                    "placeholder": "Subject",
                }
            ),
            "message": forms.Textarea(
                attrs={
                    "class": "w-full px-4 py-3 rounded-xl bg-ember-surface ring-1 ring-white/10 text-white placeholder-white/30 focus:outline-none focus:ring-ember-primary/50 transition-all duration-300 resize-none",
                    "placeholder": "Your Message",
                    "rows": 6,
                }
            ),
        }

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if len(name.strip()) < 2:
            raise forms.ValidationError("Name must be at least 2 characters.")
        return name.strip()

    def clean_message(self):
        message = self.cleaned_data.get("message")
        if len(message.strip()) < 10:
            raise forms.ValidationError("Message must be at least 10 characters.")
        return message.strip()
