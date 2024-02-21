from django import forms
from book.models import Books
from django.contrib.auth.models import User

class BookForm(forms.ModelForm):
    class Meta:
        model=Books
        fields="__all__"

        widgets={
            "name":forms.TextInput(attrs={"class":"form-control"}),
            "price":forms.NumberInput(attrs={"class":"form-control"}),
            "author":forms.TextInput(attrs={"class":"form-control"}),
            "publisher":forms.TextInput(attrs={"class":"form-control"}),
        }


class RegisterationForm(forms.ModelForm):
    class Meta:
        model=User
        fields=["username","email","password"]

        widgets={
            "username":forms.TextInput(attrs={"class":"form-control"}),
            "email":forms.TextInput(attrs={"class":"form-control"}),
            "password":forms.TextInput(attrs={"class":"form-control"})

        }



class LoginForm(forms.Form):
    username=forms.CharField(widget=(forms.TextInput(attrs={"class":"form-control","placeholder":"enter username"})))
    password=forms.CharField(widget=(forms.PasswordInput(attrs={"class":"form-control","placeholder":"enter password"})))

