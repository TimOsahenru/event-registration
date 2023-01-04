from django.forms import ModelForm
from .models import Submission, User
from django.contrib.auth.forms import UserCreationForm


class SubmissionForm(ModelForm):
	class Meta:
		model = Submission
		fields = ['details']
		
		
class CustomUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'name', 'email', 'password1', 'password2']


class UserForm(ModelForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'bio', 'avatar']
