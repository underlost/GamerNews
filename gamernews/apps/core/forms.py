from django import forms
from django.forms import widgets, Select
from django.utils.safestring import mark_safe
from django.contrib.auth import authenticate
from django.utils.translation import ugettext, ugettext_lazy as _

from .models import Account

class AccountForm(forms.ModelForm):
    #Assumes that the Account instance passed in has an associated User
    #object. The view (see views.py) takes care of that
    class Meta(object):
        model = Account
        fields = ['about', 'location', 'url', 'gender', ]
    email = forms.EmailField(required=False)

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        if instance:
            kwargs.setdefault('initial', {}).update({'email': instance.email})
        super(AccountForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(AccountForm, self).save(commit=commit)
        if 'email' in self.cleaned_data:
            instance.email = self.cleaned_data['email']
            if commit:
                instance.save()
        return instance


class UserCreationForm(forms.ModelForm):
    error_messages = {
        'duplicate_username': _("A user with that username already exists."),
    }
    username = forms.RegexField(label=_("Username"), max_length=30, regex=r'^[\w-]+$')
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ("username", "email")

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM.
        username = self.cleaned_data["username"]
        try:
            Account._default_manager.get(username=username)
        except Account.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
        

class AccountModelForm(forms.ModelForm):

	class Meta:
		model = Account
		exclude = (
			'username', 'password', 'is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined',
			'hide_mobile', 'last_seen_on', 'last_seen_ip', 'preferences', 'view_settings', 'send_emails',
			'secret_token', 'send_emails', 'is_beta',
			)
		widgets = {
		
			#Account
			'first_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name',}),
			'last_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name',}),	
			'email': forms.TextInput(attrs={'type':'email', 'class':'form-control', 'placeholder':'Email address',}),	
			
			#Profile
			'about': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Site Description', 'rows':'2'}),
			'location': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Collection name',}),
			'url': forms.TextInput(attrs={'type':'url', 'class':'form-control', 'placeholder':'Link to your other website?',}),
			'gender': forms.Select(attrs={'class':'form-control',}),
			'timezone': forms.Select(attrs={'class':'form-control',}),
			
		}