import random
import string 
from django import forms
from flesh.models import Company, Masters, Masters_Content, Operations, Order, OperationsDetailNas
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage, Storage
from django.contrib.auth.models import User
from django.forms.widgets import ClearableFileInput, Textarea
#from PIL import Image
from django.forms import formset_factory, formsets

letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

# class OperationForm(forms.ModelForm):
#     class Meta:
#         model  = Operations
#         fields = ['operation','description', 'cash', 'time']

#         widgets ={
#             'operaion':forms.TextInput(attrs={'class':'form-control'}),
#             'description':forms.TextInput(attrs={'class':'form-control'}),
#             'cash':forms.NumberInput(attrs={'class':'form-control'}),
#             'time':forms.TimeInput(attrs={'class':'form-control'}),
#         }

class MastersCabinetForm(forms.ModelForm):
    class Meta:
        model  = Masters
        fields = ['name_m', 'number_m', 'image']

        widgets = {
            'name_m':forms.TextInput(attrs={'class':'form-control'}),
            'number_m':forms.NumberInput(attrs={'class':'form-control'}),
            'image': forms.ImageField(widget=ClearableFileInput)
        }

class MastersForm(forms.ModelForm):
    class Meta:
        model  = Masters
        fields = ['name_m', 'number_m']

        widgets = {
            'name_m':forms.TextInput(attrs={'class':'form-control'}),
            'number_m':forms.TextInput(attrs={'class':'form-control'})
        }

    def save(self, company):
        master = Masters(name_m=self.cleaned_data['name_m'],number_m=self.cleaned_data['number_m'],company=company, slug=random.choice(str(letters))+str(self.cleaned_data['number_m'])+random.choice(str(letters))+random.choice(str(letters)))
        master.save()
        return master

    def clear_number_m(self):
        new_number = self.cleaned_data['number']
        for i in new_number:
            if (ord(i)<48 and ord(i)>57) or ord(i)!=43:
                raise ValidationError('Введите коректный номер')
        return new_number


#Проверить на поле на загрузку файлов возможно лучше использовать filefield 
class MastresFoto(forms.Form):
    file = forms.ImageField(widget=ClearableFileInput)


class ForingMastersCabinetForm(forms.Form):
    name_m   = forms.CharField(max_length= 25,widget=forms.TextInput(attrs={'class':'form-control'}))
    number_m = forms.CharField(max_length= 25,widget=forms.TextInput(attrs={'class':'form-control'}))
    image = forms.ImageField(widget=ClearableFileInput)
    files = forms.FileField(widget=ClearableFileInput)
    diplom_m  = forms.ImageField(widget=ClearableFileInput)
    diplom_discription_m = forms.CharField(max_length= 25,widget=forms.TextInput(attrs={'class':'form-control'}))
    content_m  = forms.ImageField(widget=ClearableFileInput)
    content_discription_m = forms.CharField(max_length= 25,widget=forms.TextInput(attrs={'class':'form-control'}))

    def clean_data(self):
        name_m   = self.cleaned_data['name_m']
        number_m = self.cleaned_data['number_m']
        diplom_discription_m = self.cleaned_data['diplom_discription_m']
        content_discription_m = self.cleaned_data['content_discription_m']
        return self.clean_data


class CompanyCabinetForm(forms.ModelForm):
    """
    Основная форма для определения параметров компании и её описаний 
    """
    class Meta:
        model  = Company
        fields = ['number', 'body', 'image', 'city', 'start_time', 'end_time']

        widgets = {
            'number':forms.TextInput(attrs={'class':'form-control'}),
            'body':forms.TextInput(attrs={'class':'form-control', 'rows':'3'}),
            'image': forms.ImageField(widget=ClearableFileInput),#storage=FileSystemStorage(location='/media/cabinet/images/'),
            'city': forms.TextInput(attrs={'class':'form-control'}),
            'start_time': forms.TimeField(),
            'end_time': forms.TimeField(),
        }


class CompanyFormProbOriginal(forms.Form):
    number = forms.CharField(max_length= 25,widget=forms.TextInput(attrs={'class':'form-control'}))
    image = forms.ImageField(widget=ClearableFileInput)
    files = forms.FileField(widget=ClearableFileInput)
    diplom_m  = forms.ImageField(widget=ClearableFileInput)
    diplom_discription_m = forms.CharField(max_length= 25,widget=forms.TextInput(attrs={'class':'form-control'}))
    content_m  = forms.ImageField(widget=ClearableFileInput)
    content_discription_m = forms.CharField(max_length= 25,widget=forms.TextInput(attrs={'class':'form-control'}))


class CreateOperations(forms.Form):
    name = forms.CharField(max_length= 25,widget=forms.TextInput(attrs={'class':'form-control'}))


class DetailCreateOperations(forms.Form):
    name = forms.CharField(max_length= 25,widget=forms.TextInput(attrs={'class':'form-control'}))
    cash = forms.ImageField()
    time = forms.TimeField()
    description = forms.Textarea()

    def createDetailOperations(self, master):
        # obj = OperationsDetail(name=self.cleaned_data['name'],cash=self.cleaned_data['cash'],time=self.cleaned_data['time'],description=self.cleaned_data['description'])
        pass