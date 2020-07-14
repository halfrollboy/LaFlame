
from django.views.generic import View,TemplateView
from django.views.generic.edit import FormView
from .forms import AdministrationForm, LoginForm,Logform,LoginForm,CompanyForm, CommentsForm, NewCompanyForm
from .models import Company, Masters, Operations, Clients, Review, NewCompany
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, render_to_response, get_object_or_404, reverse 
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect ,JsonResponse
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from web_project.celery import celery_app
from django.core.mail import send_mail
from django.conf import settings
from django.template import Engine, Context


"""
Шаблоны для отправки электронных писем
"""
def render_template(template, context):
    engine = Engine.get_default()

    tmpl = engine.get_template(template)
    return tmpl.render(Context(context))

@celery_app.task
def send_mail_task(recipients, subject, template, context):
    send_mail(
        subject=subject,
        message=render_template(f'{template}.txt', context),
        from_email=settings,
        recipient_list=recipients,
        fail_silently=False,
        html_message=render_template(f'{template}.html', context))

def masters_ajax(request):
    if request.method =='GET':
        print('hi!')
        return HttpResponse('ok')

def create_user(request):
    if request.method =='POST':
        date_as = request.POST['date_as']
        day = request.POST['day']
        month = request.POST['month']
        time = request.POST['time']

    # Date.objects.create(
    #     date_as=date_as,
    #     day = day,
    #     month = month,
    #     time = time, 
    # )
    return HttpResponse('')

def post_list(request):
    return render(request,'flesh/index.html')

def login_page(request):
    print(request, "Зашли в login_page")
    pass

def logout_user(request):
    logout(request)
    return redirect('administration_url')

class MixinDetail(object):
    """Общий класс для вывода деталей мастеров и комапаний"""
    model=None
    template=None

    def get(self,request, slug):
        obj = get_object_or_404(self.model, slug__iexact=slug)
        return render(request, self.template, context={self.model.__name__.lower():obj})


class MixinList(object):
    """Общий класс для вывода списков мастеров и комапаний"""
    model=None
    template=None

    def get(self, request):
        obj = self.model.objects.all()
        return render(request, self.template, context={self.model.__name__.lower():obj})


class CompanyDetail(TemplateView):
    model    = Company
    template = 'flesh/company_detail.html'
    
    def get(self,request, slug):
        obj = get_object_or_404(self.model, slug__iexact=slug)
        comments = obj.review_set.filter(active=True)
        comments_form = CommentsForm()
        return render(request, self.template, context={self.model.__name__.lower():obj, 'comments_form':comments_form, 'comments':comments})

    def post(self, slug, request):
        if request.method == 'POST':
            comments_form = CommentsForm(request.POST)
            if comments_form.is_valid():
                number = comments_form.cleaned_data['number']
                obj = get_object_or_404(self.model, slug__iexact=slug)
                comments=obj.review_set.all()
                try:
                    client=obj.clients_set.filter(number_telephone=number)
                except:
                    erors_m='Извините, но пользователь с такими данными не посещал этот салон.'
                    return self.render_to_response(self.get_context_data(erors_m=erors_m, comments_form=comments_form, comments=comments))
                new_comment = comments_form.save(commit=False)
                new_comment.company_r = obj
                new_comment.save()
                comments_form = CommentsForm()
                return self.render_to_response(self.get_context_data( comments_form = comments_form, comments=comments, new_comment=new_comment))
            else:
                comments_form.clean()
                erors_m='Форма заполненна неверно, попробуйте снова'
                return self.render_to_response(self.get_context_data(erors_m=erors_m, comments_form=comments_form, comments=comments))

        
class MainHelloPage(MixinList, View):
    model=Operations
    template= 'flesh/index.html'


class MasterDetail(MixinDetail, View):
   model=Masters
   template='flesh/masters_detail.html'


class CompanyList(MixinList, View):
    model=Company
    template='flesh/company_list.html'


class MastersList(MixinList, View):
    model=Masters
    template='flesh/masters_list.html'


class Administration(View):

    def get(self, request):
        form = LoginForm()
        return render(request, 'flesh/administration.html', context={'form':form})

    def post(self, request):
        bound_form = LoginForm(request.POST)
        eror=None
        if bound_form.is_valid():
            cd = bound_form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('cabinet:cabinet_main_page', slug=request.user.username) 
            else:
                eror = 'Не правильный логин или пароль'
                return render(request, 'flesh/administration.html',context={'form':bound_form, 'error':eror})

        return render(request, 'flesh/administration.html',context={'form':bound_form,'error':eror})


class CreateNewCompany(View):
    def get(self, request):
        form = NewCompanyForm()
        return render(request, 'flesh/new_company.html', context={'form':form})
    
    def post(self, request):
        bound_form = NewCompanyForm(request.POST)
        eror = None
        if bound_form.is_valid():
            cd = bound_form.cleaned_data
            comp = NewCompany(number=bound_form.cleaned_data['number'],name=bound_form.cleaned_data['name'],discription=bound_form.cleaned_data['discription'])
            comp.save()
            bound_form = NewCompanyForm()
            return render(request, 'flesh/new_company.html', context={'form':bound_form})
        else:
            return redirect('administration_url')


# class AjaxComments(View):
#     def post(self, request):
#         if request.method == "POST":
            
#             create_operations = CommentsForm(request.POST)
#             if create_operations.is_valid():
#                 create_operations.clean()
#                 try:
#                     obj = get_object_or_404(Company, slug__iexact=request.POST['slug'])
#                 except:
#                     return redirect('administration_url')
#                 new_oper = create_operations.cleaned_data['name'].lower()
#                 new_oper = new_oper[0].upper()+new_oper[1:]
#                 if Operations.objects.filter(name_operations='new_oper'):
#                     errors = 'ОШИБКА проверьте пожалуйста данные возможно такая услуга присутствует в базе'
#                 else:
#                     oper = Operations(name_operations=new_oper, company=obj)
#                     oper.save()
#                     errors = ''
#             else:
#                 errors = 'ОШИБКА проверьте пожалуйста данные'       
#             return JsonResponse({'new_oper':new_oper, 'errors':errors})
#         else: 
#             return redirect('administration_url')


# class CabinetCompany(View):

#     @login_required
#     def get(self,request):
#         form = MastersForm()
#         return render(request, 'flesh/createmaster.html', context={'forma':form})
#_____________________________________________________________________________________________________
"""Класс формы для кабинета

попробовать def form_valid(self, form):
        title = form.cleaned_data['title']

"""

# class CompanyFormView(FormView):
#     """Класс формы для кабинета"""
#     template_name = 'flesh/base_cabinet.html'
#     success_url = reverse_lazy('cabinet_company_url')

#     def post(self, request, *args, **kwargs):
#         prostoform = self.form_class(request.POST)
#         mastersform = MastersForm()
#         fotoform = MastresFoto()
#         if prostoform.is_valid():
#             prostoform.save()
#             return self.render_to_response(self.get_context_data(success=True))
#         else:
#             return self.render_to_response(
#             self.get_context_data(mastersform=mastersform, fotoform=fotoform)
#         )
# #___________________________________________________________________________________________________________

# class CompanyFormViewMasters(FormView):
#     """Класс формы для кабинета"""
#     form_class = ProstForm
#     template_name = 'flesh/base_cabinet_masters.html'
#     success_url = 'cabinet/cabinet_masters'

#     def post(self, request, *args, **kwargs):
#         prostoform = self.form_class(request.POST)
#         mastersform = MastersForm()
#         fotoform = MastresFoto()
#         if prostoform.is_valid():
#             prostoform.save()
#             return self.render_to_response(self.get_context_data(success=True))
#         else:
#             return self.render_to_response(
#             self.get_context_data(mastersform=mastersform, fotoform=fotoform, prostoform=prostoform))


# class MasterFormViewMasters(FormView):
#     """Класс формы для кабинета"""
#     form_class = MastersForm
#     template_name = 'flesh/base_cabinet_masters.html'
#     success_url = 'cabinet/cabinet_masters'

#     def post(self, request, *args, **kwargs):
#         mastersform = self.form_class(request.POST)
#         fotoform = MastresFoto()
#         prostoform = ProstForm()
#         if mastersform.is_valid():
#             mastersform.save()
#             return self.render_to_response(self.get_context_data(success=True))
#         else:
#             return self.render_to_response(
#             self.get_context_data(mastersform=mastersform,fotoform=fotoform, prostoform=prostoform)
#         )


# class MastresFotoViewMasters(FormView):
#     """Класс формы для кабинета"""
#     form_class = MastresFoto
#     template_name = 'flesh/base_cabinet_masters.html'
#     success_url = 'cabinet/cabinet_masters'

#     def post(self, request, *args, **kwargs):
#         fotoform = self.form_class(request.POST)
#         mastersform = MastersForm()
#         prostoform = ProstForm()
#         if fotoform.is_valid():
#             fotoform.save()
#             return self.render_to_response(self.get_context_data(success=True))
#         else:
#             return self.render_to_response(
#             self.get_context_data(mastersform=mastersform, fotoform=fotoform, prostoform=prostoform)
#         )


# class ProstViewMasters(FormView):
#     """Класс формы для кабинета"""
#     form_class = ProstForm
#     template_name = 'flesh/base_cabinet_masters.html'   
#     success_url = 'cabinet/cabinet_masters'

#     def post(self, request, *args, **kwargs):
#         prostoform = self.form_class(request.POST)
#         mastersform = MastersForm()
#         fotoform = MastresFoto()
#         if prostoform.is_valid():
#             prostoform.save()
#             return self.render_to_response(self.get_context_data(success=True))
#         else:
#             return self.render_to_response(
#             self.get_context_data(mastersform=mastersform, fotoform=fotoform, prostoform=prostoform)
#         )

