from django import forms

from django.contrib.auth.models import User

class user_login_form(forms.Form):
    username = forms.CharField()
    password = forms.CharField()


class user_register_form(forms.ModelForm):
    password = forms.CharField()
    password2 = forms.CharField()

    class Meta:
        model = User
        fields = ('username','email')

    def check_password(self):
        data = self.cleaned_data
        if data.get('password') == data.get('password2'):
            return data.get('password')
        else:
            raise ValueError('Please enter the same password. Please try again')