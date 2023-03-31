from .models import Product, User
from django import forms
from django.forms import ValidationError
import re
from django.contrib.auth.forms import AuthenticationForm
from captcha.fields import CaptchaField



class UserAuthenticationForm(AuthenticationForm):
    """ A form for authorization users. """
    username = forms.EmailField(widget=forms.EmailInput(
        attrs={ "class" : "form-control", "id" : "floatingInputEmail", "placeholder" : "Адрес электронной почты" }
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={"class" : "form-control", "id" : "floatingInputPassword", "placeholder" : "Пароль"}
    ))
    captcha = CaptchaField()

    def clean_username(self):
        email = self.cleaned_data["username"]
        print(email)
        if User.objects.filter(email=email, is_confirmation=False):
            raise ValidationError("Необходимо подтвердить почту")

        return email
    
        
        

class UserCreationForm(forms.ModelForm):
    # number_phone = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Номер телефона"}))
    # email = forms.EmailField(max_length=100,
    #                            widget=forms.EmailInput(attrs={"placeholder": "Ваша почта"}))
    password1 = forms.CharField(widget=forms.PasswordInput(
                                    attrs={"class" : "form-control", "id" : "Password1", "placeholder" : "Hard password"}
    ))
    password2 = forms.CharField(widget=forms.PasswordInput(
                                    attrs={"class" : "form-control", "id" : "Password2", "placeholder" : "Repeat hard password"}
    ))
    captcha = CaptchaField()
    class Meta:
        model = User
        fields = ("number_phone", "email", 'password1', 'password2')
        widgets = {
            "email" : forms.EmailInput(attrs={"class" : "form-control", "id" : "Email", "placeholder" : "name@example.com"}),
            "number_phone" : forms.TextInput(attrs={"class" : "form-control", "id" : "Phone", "placeholder" : "+79999999999"}),
            # "password1" : forms.PasswordInput(attrs={"class" : "form-control", "id" : "floatingInputPassword1", "placeholder" : "Hard password"}),
            # "password2" : forms.PasswordInput(attrs={"class" : "form-control", "id" : "floatingInputPassword2", "placeholder" : "Repeat hard password"})
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают")
        return password2


    def clean_number_phone(self):
        number_phone = self.cleaned_data["number_phone"]

        if not re.findall("\+?79[0-9]{9}", number_phone):
            raise ValidationError("Номер должен состоять из 11 цифр и начинаться с 79")

        if number_phone.startswith("+") and User.objects.filter(number_phone=number_phone.replace("+", "")).exists():
            raise ValidationError("Номер телефона занят")

        return number_phone

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
