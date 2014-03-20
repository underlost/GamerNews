from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import UserCreationForm
from .models import Account

class MyUserCreationForm(UserCreationForm):
	def clean_username(self):
		# Since User.username is unique, this check is redundant,
		# but it sets a nicer error message than the ORM. See #13147.
		username = self.cleaned_data["username"]
		try:
			Account._default_manager.get(username=username)
		except Account.DoesNotExist:
			return username
		raise forms.ValidationError(self.error_messages['duplicate_username'])

	class Meta(UserCreationForm.Meta):
		model = Account

class AccountChangeForm(UserChangeForm):
	class Meta(UserChangeForm.Meta):
		model = Account

class AccountAdmin(UserAdmin):
	list_display = ( 'username', 'is_staff', 'last_login', 'date_joined',)
	list_filter = ('is_staff', 'is_active', 'is_superuser', 'is_beta', )
	form = AccountChangeForm
	add_form = MyUserCreationForm
	fieldsets = UserAdmin.fieldsets + (
			(None, {'fields': (
				'gender', 'location', 'url', 'about',
				'hide_mobile', 'last_seen_on', 'last_seen_ip', 'preferences', 'view_settings', 'send_emails',
				'timezone', 'is_beta',
			)}),
	)


admin.site.register(Account, AccountAdmin)
