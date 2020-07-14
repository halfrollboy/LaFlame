import random
import string 
from django import forms
from .models import Company, Masters, Masters_Content, Operations, Order, Review, Clients, NewCompany
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.forms.widgets import ClearableFileInput
from captcha.fields import CaptchaField


letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'


class LoginForm(forms.Form):
    username = forms.CharField(max_length= 25,widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(max_length= 30,widget=forms.PasswordInput(attrs={'class':'form-control'}))
    captcha  = CaptchaField(label='Введите текст с картинки', error_messages={'invalid':'Неправильный текст'})

    def clean_data(self):
        new_login = self.cleaned_data['username']
        new_password = self.cleaned_data['password']

        if new_login == 'administration' or new_login =='admin':
            raise ValidationError('Eror you not admin :)')
        
        return self.clean_data


class Logform(forms.ModelForm):
    
    captcha = CaptchaField()
    class Meta:
        model = User
        fields = ['username', 'password', 'captcha']

        widgets = {
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'password':forms.PasswordInput(attrs={'class':'form-control'}),
        }



class AdministrationForm(forms.ModelForm):
    """Форма компания, исполбзуется наследование от ModelForm, 
        у него есть некоторые методы тип save"""
    captcha = CaptchaField()
    class Meta:
        model = Company
        fields = ['login', 'password','captcha']

        widgets = {
            'login':forms.TextInput(attrs={'class':'form-control'}),
            'password':forms.PasswordInput(attrs={'class':'form-control'})
        }

    def clean_login(self):
        new_login = self.cleaned_data['login']
        
        if new_login == 'administration' or new_login =='admin':
            raise ValidationError('Eror you are not admin :)')
        obj=Company.objects.get(login=new_login)
        if self.cleaned_data.filter(login=obj.login).exists():
            return new_login
        else:
            raise ValidationError('Login or password erors')
        return new_login


# class DateScheduleForm(forms.ModelForm):#Расписание работы
#     class Meta:
#         model  = Date
#         fields = ['date_as', 'day', 'month','time']

#         widgets = {
#             'date_as' :forms.DateInput(attrs={'class':'form-control'}),
#             'year'    :forms.NumberInput(attrs={'class':'form-control'}),
#             'day'     :forms.NumberInput(attrs={'class':'form-control'}),
#             'month'   :forms.NumberInput(attrs={'class':'form-control'}),
#             'time'    :forms.TimeInput(attrs={'class':'form-control'}),
#         }


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name','body','image','number']

        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'body':forms.TextInput(attrs={'class':'form-control','rows':'3'}),
            'images':forms.ImageField(widget=ClearableFileInput),
            'number':forms.TextInput(attrs={'class':'form-control'})
        }

# class OperationForm(forms.ModelForm):
#     class Meta:
#         model  = Operations
#         fields = ['operation', 'cash', 'time']

#         widgets ={
#             'operaion':forms.TextInput(attrs={'class':'form-control'}),
#             'cash':forms.NumberInput(attrs={'class':'form-control'}),
#             'time':forms.TimeInput(attrs={'class':'form-control'}),
#         }

class OrderForm(forms.ModelForm):
    class Meta:
        model  = Order
        fields = ['name','telephone']

        widgets ={
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'telephone':forms.TextInput(attrs={'class':'form-control'}),
        }


class CommentsForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('name', 'number', 'reviews')

        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control rounded-pill'}),
            'number':forms.TextInput(attrs={'class':'form-control rounded-pill'}),
            'reviews':forms.Textarea(attrs={'class':'form-control rounded-top rounded-bottom', 'id':'exampleFormControlTextarea1', 'rows':'4'}),
        }

    def clear_number(self):
        new_number = self.cleaned_data['number']
        for i in new_number:
            if (ord(i)<48 and ord(i)>57) or ord(i)!=43:
                raise ValidationError('Введите коректный номер')
        return new_number


class NewCompanyForm(forms.ModelForm):
    class Meta:
        modal = NewCompany
        fields = ('number','name','discription')

        widgets = {
            'number':forms.TextInput(attrs={'class':'form-control'}),
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'discription':forms.Textarea(attrs={'class':'form-control rounded-top rounded-bottom', 'id':'exampleFormControlTextarea1', 'rows':'4'}),
        }