from django import forms
from taskapp.models import Task

from django.contrib.auth.models import User

class TaskForm(forms.ModelForm):
    class Meta:
        model=Task
        exclude=("id","created_date","user_object")

        widgets={
            "title":forms.TextInput(attrs={"class":"form-control"}),
            "status":forms.CheckboxInput(attrs={"class":"mb-3"}),
            # "user":forms.TextInput(attrs={"class":"form-control"})
        }


class RegisterForm(forms.ModelForm):


    class Meta:

        model=User

        fields=["username","email","password"]

        widgets={
             "username":forms.TextInput(attrs={"class":"form-control"}),
             "email":forms.EmailInput(attrs={"class":"form-control"}),
             "password":forms.PasswordInput(attrs={"class":"form-control"}),
        }
        




class LoginForm(forms.Form):
       username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
       password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))


class SummaryForm(forms.Form):
     start_date=forms.DateTimeField(widget=forms.DateInput(attrs={"class":"form-control  mb-4 ","type":"date"}))
    
     end_date=forms.DateTimeField(widget=forms.DateInput(attrs={"class":"form-control mb-4" ,"type":"date"}))