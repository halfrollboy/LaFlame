from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import pre_save
from django.dispatch import receiver
import datetime
import os
from PIL import Image

#Create your model here

class Company(models.Model):
    """В этой таблице записывается компания и её основные параметры"""
    class Meta:
        db_table = 'company'
        verbose_name = "Компания"
        verbose_name_plural = "Компании"

    TYPE_CHOICES = (
        ('full','Full'),
        ('one-time','One-time')
    )

    name       = models.CharField("Название", unique = True, max_length=30)
    number     = models.IntegerField("Номер телефона фирмы", unique=True)
    slug       = models.SlugField(max_length=150)
    body       = models.TextField("Описание фирмы", blank=True)
    start_time = models.TimeField()
    end_time   = models.TimeField()
    city       = models.CharField('Город', max_length=30)
    image      = models.ImageField('Картинка ',blank=True, upload_to='image_comp',unique=True)
    login      = models.CharField("Логин", max_length=20,unique = True)
    password   = models.CharField("Пароль",max_length=20,unique = True)
    commission = models.CharField(max_length=10, choices=TYPE_CHOICES, default='one-time')
    objects    = models.Manager()

    def save(self, *args, **kwargs):
        new_group, created = Group.objects.get_or_create(name=self.slug)
        if new_group is not None:
            new_user = User.objects.create_user(username=self.login, password=self.password, *args,**kwargs)
            new_group.user_set.add(new_user)
            new_user.save()
            new_group.save()
        return super(Company, self).save(*args, **kwargs)

    def get_persent(self, arg, val):
        if arg == 'full':
            return val
        elif arg=='one-time':
            return val+5

    # def delete(self, *args, **kwargs):
    #     group=Group.objects.get(name=self.slug)
    #     group.delete()
    #     return super(Company, self).delete(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("company_detail_url", kwargs={"slug": self.slug})

    def __str__(self):
        return 'company: {0}\n number: {1}\n city:{2}\n'.format(self.name,self.number,self.city)


class CompanyOrder(models.Model):
    
    threy_month = models.DecimalField(max_digits=15, default=0, decimal_places=2)
    month       = models.DecimalField(max_digits=15, default=0, decimal_places=2)
    day         = models.DecimalField(max_digits=15, default=0, decimal_places=2)
    company     = models.ForeignKey(Company, on_delete=models.CASCADE)


class Clients(models.Model):
    """Здесь записываются клиенты"""
    objects          = models.Manager()
    name             = models.CharField("Название", unique = True, max_length=50)
    visits           = models.IntegerField("Посещений")
    number_telephone = models.CharField("Номер телефона",max_length=13,unique = True)
    company          = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return 'name: {0}\n number: {1}\n'.format(self.name,self.number_telephone)


class CompanyOtherSettings(models.Model):
    """Все доп настройки компаний"""
    objects    = models.Manager()
    company    = models.ForeignKey(Company, on_delete=models.CASCADE)
    reiting    = models.DecimalField(max_digits=3, default=0, decimal_places=2)
    menuColor  = models.CharField("Цвет главного меню", max_length=7)


class Review(models.Model):
    """Таблица для отзывов"""
    reviews    = models.TextField('Отзыв',blank=True)
    company_r  = models.ForeignKey(Company, on_delete=models.CASCADE)
    created    = models.DateTimeField(auto_now_add=True)
    active     = models.BooleanField(default=True)
    updated    = models.DateTimeField(auto_now=True)
    number     = models.CharField("Номер телефона",max_length=13,unique = True)
    name       = models.CharField("ФИО",max_length=50,unique = True)


class Masters(models.Model):#TODO Сделать статистику мастера 
    """В этой таблице записываются мастера"""
    class Meta:
        db_table = 'masters'
        verbose_name = "Мастер"
        verbose_name_plural = "Мастера"

    name_m   = models.CharField("Имя мастера", max_length=30)
    number_m = models.CharField("Номер мастера", max_length=12 ,blank=True, unique = True)
    company  = models.ForeignKey(Company, on_delete=models.CASCADE)
    slug     = models.SlugField(max_length=100, blank = True)
    image    = models.ImageField('Фото ',blank=True, upload_to='flesh/static/images/dinamic_img/')
    objects  = models.Manager()

    # def delete(self, *args, **kwargs):
    #     group=Masters.objects.filter(slug=self.slug, name_m=self.name_m, number_m=self.number_m)
    #     group.delete()
    #     return super(Masters, self).delete(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("company_detail_url", kwargs={"slug": self.slug})

    def __str__(self):
        return '{}'.format(self.name_m)


class MasterOtherSettings(models.Model):
    """"""
    objects  = models.Manager()
    master   = models.ForeignKey(Masters, on_delete=models.CASCADE)
    reiting    = models.DecimalField(max_digits=3, default=0, decimal_places=2)
    menuColor  = models.CharField("Цвет главного меню", max_length=7)


class MasterStatistics(models.Model):
    objects = models.Manager()
    persent = models.DecimalField("Оценка качества",default=0,max_digits=5, decimal_places=2)
    klients = models.IntegerField('Кол-во клиентов',default=0)
    master  = models.OneToOneField(Masters, on_delete=models.CASCADE, to_field=None)
    

class Masters_Content(models.Model):
    TYPE_CONTENT = {
        'diplom':{'path':'masters_img/masters_diploma',},
        'content':'masters_img/masters_content',
    }

    objects        = models.Manager()
    description    = models.TextField("Описание деятельности мастера", default='no description')
    master         = models.ForeignKey(Masters, on_delete=models.CASCADE)
    

class MastersImagesDiploma(Masters_Content):#добавить обязательное поле при релизе 
    images_diploma = models.ImageField(verbose_name='MasterImageDiplom', upload_to='masters_img/masters_diploma',unique=True)#добавить обязательное поле при релизе 
    objects        = models.Manager()
    # description_d  = models.TextField("Описание фото")
    # master         = models.ForeignKey(Masters, on_delete=models.CASCADE)

    def __str__(self):
        return "[{}] {}".format(self.pk, self.description)

    def save_img(self):
        image = Image.open(self.images_diploma)
        image.save(self.images_diploma, quality=70, optimize=True)


class MastersImagesContent(Masters_Content):
    objects        = models.Manager()
    images_content = models.ImageField(verbose_name="MasterImageContent", upload_to='masters_img/masters_content',unique=True) 
    
    def __str__(self):
        return "[{}] {}".format(self.pk, self.description)
    
    #TODO Проверить работу сохранялки 
    # def save_img(self):
    #     image = Image.open(self.images_content)
    #     image.save(self.images_content, quality=70, optimize=True)
    
    # @receiver(pre_save, sender=MastersImagesContent)
    # def compressor(self, sender, instance, **kwargs):
    #     instance.image_content = instance.save_img()


class Operations(models.Model):
    class Meta:
        db_table = 'operation'
        verbose_name = "Операция"
        verbose_name_plural = "Операции"
    
    name_operations = models.CharField('Название услуги',unique = True, max_length=50)
    company         = models.ForeignKey(Company, on_delete=models.CASCADE)
    objects         = models.Manager()
        

class OperationsDetail(Operations):
    cash        = models.IntegerField('Стоимость услуги')
    time        = models.TimeField('Время на услугу')
    description = models.TextField('Описание услуги',default='no description')
    master      = models.ForeignKey(Masters, on_delete=models.CASCADE)
    objects     = models.Manager()

class OperationsDetailNas(models.Model):
    cash        = models.IntegerField('Стоимость услуги')
    time        = models.TimeField('Время на услугу')
    description = models.TextField('Описание услуги',default='no description')
    master      = models.ForeignKey(Masters, on_delete=models.CASCADE)
    main        = models.ForeignKey(Operations, on_delete=models.CASCADE)
    objects     = models.Manager()


# class Date(models.Model):
#     """В этой таблице записывается свободное расписание"""
#     class Meta:
#         db_table = 'date'
#         verbose_name = "Дата"
#         verbose_name_plural = "Даты"

#     update    = models.DateTimeField("Дата обновления",auto_now=True) 
#     date_as   = models.DateField("Дата",default=datetime.date.today)
#     year      = models.IntegerField("Год",default=datetime.date.today().year)
#     month     = models.IntegerField("Месяц",default=datetime.date.today().month)
#     day       = models.IntegerField("День", default=datetime.date.today().day)
#     time      = models.TimeField("Время")
#     master    = models.ForeignKey(Masters, on_delete=models.CASCADE)
#     objects   = models.Manager()


#     def get_absolute_url(self):
#         return reverse("date_detail_url", kwargs={"date": self.day})

#     def __str__(self):
#         return '{}'.format(self.day)


class OrderDate(models.Model):
    """В этой таблице записывается свободное расписание"""
    class Meta:
        db_table = 'orderdate'
        verbose_name = "Дата"
        verbose_name_plural = "Даты"

    update    = models.DateTimeField("Дата обновления",auto_now=True) 
    date_as   = models.DateField("Дата",default=datetime.date.today)
    year      = models.IntegerField("Год",default=datetime.date.today().year)
    month     = models.IntegerField("Месяц",default=datetime.date.today().month)
    day       = models.IntegerField("День", default=datetime.date.today().day)
    timestart = models.TimeField("Время")
    endtime   = models.TimeField("Время")
    master    = models.ForeignKey(Masters, on_delete=models.CASCADE)
    objects   = models.Manager()


    def get_absolute_url(self):
        return reverse("date_detail_url", kwargs={"date": self.day})

    def __str__(self):
        return '{}'.format(self.day)


class Order(models.Model):
    class Meta:
        db_table = 'order'
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    name        = models.TextField("Имя Заказщика",default='No_name',unique = True, max_length=50)
    telephone   = models.CharField("Телефон заказчика",default='No_telephone',unique = True, max_length=50)
    data        = models.ForeignKey(OrderDate, on_delete=models.CASCADE)
    company     = models.ForeignKey(Company, on_delete=models.CASCADE)
    operation   = models.ForeignKey(OperationsDetailNas, on_delete=models.CASCADE)
    clients     = models.ForeignKey(Clients, on_delete=models.CASCADE)
    total_cost  = models.DecimalField('Итоговая стоимость',max_digits=10, default=0, decimal_places=2)


class NewCompany(models.Model):
    class Meta:
        db_table = 'new_company'
        verbose_name = "Новая компания"
        verbose_name_plural = "Новые компании"

    number      = models.CharField('Номер телефона', max_length=14, unique=True, blank=True, default='0')
    name        = models.CharField('Имя владельца', max_length=14, default='0')
    discription = models.TextField('Описание')
    date        = models.DateTimeField(auto_now=True)

