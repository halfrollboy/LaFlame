# -*- coding: utf-8 -*-
from django.views.generic import View,TemplateView
from django.shortcuts import render, redirect, render_to_response, get_object_or_404, reverse
from flesh.models import Company, Masters, Operations, OperationsDetailNas, Order #TODO зарефакторить работу с моделями 
from flesh.forms import AdministrationForm, LoginForm,Logform,LoginForm,CompanyForm
from .forms import ForingMastersCabinetForm, CompanyCabinetForm, MastersForm, MastresFoto, CreateOperations, DetailCreateOperations
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import RequestContext


class Delete_masters_form(View):
    model = Order
    template_name = 'cabinet/includes/delete_masters_form.html'

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.method =='POST':
                try:
                    Masters.objects.get(slug=request.POST['master']).delete()
                except:
                    return HttpResponse('ne ok')
                # masta = request.user.groups.all()
                # obj = get_object_or_404(Company, slug__iexact=masta[0])
                # masters= obj.masters_set.all()
                
                # context = self.get_context_data(**kwargs)
                # context['company'] = obj
                # if masters is not None:  
                #     context['masters'] = masters
            return HttpResponse('ok')



class OrderCabinet(TemplateView):
    model = Order
    template_name = 'cabinet/includes/timetable.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
             if request.method =='GET':
                return render_to_response(self.template_name)

    @csrf_protect
    def post(self, request, *args, **kwargs):
        print(request)
        return HttpResponse('ok')


class ProfileCabinet(TemplateView):
    model = Masters
    template_name = 'cabinet/includes/master_cabinet/profile_master.html'

    def get(self,request, *args, **kwargs):
        if request.user.is_authenticated:
            master = request.user.groups.all()
            #form = ForingMastersCabinetForm(request.POST, request.FILES)
            obj = get_object_or_404(self.model, slug__iexact=master[0])
            operations = obj.operations_set.all()            
            all_operations = Operations.objects.all()

            context = self.get_context_data(**kwargs)
            context['master'] = obj
            context['servises'] = operations
            context['operations'] = all_operations

            return self.render_to_response(context)

class CreteOperationMaster(View):
    def post(self, request):
        if request.method == "POST":
            
            create_operations = DetailCreateOperations(request.POST)
            if create_operations.is_valid():
                create_operations.clean()
                try:
                    obj = get_object_or_404(Masters, slug__iexact=request.POST['slug'])
                    opr = Operations.objects.filter(name_operations)
                except:
                    return redirect('administration_url')
                new_oper = create_operations.cleaned_data['name'].lower()
                
                if Operations.objects.filter(name_operations='new_oper'):
                    errors = 'ОШИБКА проверьте пожалуйста данные возможно такая услуга присутствует в базе'
                else:
                    oper = OperationsDetailNas(cash=create_operations.cleaned_data['cash'],)
                    errors = ''
            else:
                errors = 'ОШИБКА проверьте пожалуйста данные'       
            return JsonResponse({'new_oper':new_oper, 'errors':errors})
        else: 
            return redirect('administration_url')


class TimetableCabinet(TemplateView):
    model = Order
    template_name ='cabinet/includes/timetable.html'

    def get(self,request, *args, **kwargs):
        if request.user.is_authenticated:
             if request.method =='GET':
                # obj = get_object_or_404(self.model, slug__iexact=slug)
                return render_to_response(self.template_name)

    @csrf_protect
    def post(self, request, *args, **kwargs):
        return HttpResponse('ok')


#Основа под главную страницу, придётся подразбить для Ajax 
class MixinDetailCabinet(TemplateView):
    model=Company
    template_name ='cabinet/base_cabinet.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            masta = request.user.groups.all()
            obj = get_object_or_404(self.model, slug__iexact=masta[0])
            try:
                masters = Masters.objects.filter(company=obj)
            except:
                masters=None
            mastersform = MastersForm(self.request.GET or None)
            fotoform    = MastresFoto(self.request.GET or None)
            companyform = CompanyForm(self.request.GET or None)
            prob_form   = ForingMastersCabinetForm(self.request.POST or None)

            context = self.get_context_data(**kwargs)
            context['mastersform']               = mastersform
            context['fotoform']                  = fotoform
            context['companyform']               = companyform
            context['prob_form']                 = prob_form
            context[self.model.__name__.lower()] = obj
            if masters is not None:
                context['masters'] = masters
            return self.render_to_response(context)
        else:
            pass
            #return HttpResponseRedirect('notforyou') #TODO Сделать глабальную обработку ошибок 

    def post(self, request, *args, **kwargs):
        form_class = MastersForm
        template_name = 'cabinet/base_cabinet.html'
        success_url = 'cabinet/'

        mastersform = MastersForm()
        fotoform    = MastresFoto()

        masta = request.user.groups.all()
        obj = get_object_or_404(self.model, slug__iexact=masta[0])
        try: 
            masters = Masters.objects.filter(company_id=obj.id)
        except:
            masters=None
        
        if request.method=='POST' and 'createmasters' in request.POST:
            mastersform = form_class(request.POST)
            if mastersform.is_valid():
                mastersform.save(obj)
                try:
                    masters=Masters.objects.filter(company=obj)
                except:
                    masters=None
                mastersform.clean()
                return self.render_to_response(self.get_context_data(mastersform=mastersform,fotoform=fotoform,masters=masters ,company=obj ))
            else:
                mastersform.clean()
                erors_m='Не верная форма, возможно пользователь с таким номером уже существует'
                return self.render_to_response(self.get_context_data(erors_m=erors_m, mastersform=mastersform,fotoform=fotoform, masters=masters,company=obj)
            )
        if request.method=='POST' and 'e' in request.POST:
            return redirect('administration_url')

# TODO Сделать разделение пользователей на профессии 
class DetailCabinetMasters(TemplateView):
    model=Company
    template_name ='cabinet/base_cabinet_masters.html'
    
    def get(self,request, slug,*args, **kwargs):
        if request.user.is_authenticated:
            if slug is not '':
                masta = request.user.groups.all()
                obj = get_object_or_404(self.model, slug__iexact=masta[0])
                mastersform = MastersForm(self.request.GET or None)
                fotoform = MastresFoto(self.request.GET or None)
                context = self.get_context_data(**kwargs)
                context['mastersform'] = mastersform
                context['fotoform']    = fotoform
                context['masters']     = get_object_or_404(Masters, slug__iexact=slug)
                context[self.model.__name__.lower()] = obj
                return self.render_to_response(context)
            else:
                return self.render_to_response(context)
        else:
            return redirect('administration_url')
    
    def post(self, request, *args, **kwargs):
        pass
        # form_class = MastersForm
        # template_name = 'flesh/base_cabinet.html'
        # success_url = 'cabinet/'

        # mastersform = MastersForm()
        # prostoform  = ProstForm()
        # fotoform    = MastresFoto()

        # masta = request.user.groups.all()
        # obj = get_object_or_404(self.model, slug__iexact=masta[0])
        # try: 
        #     masters = Masters.objects.filter(company_id=obj.id)
        # except:
        #     masters=None

class BaseInformation(TemplateView):
    model=Company
    template_name ='cabinet/includes/base_cabinet/base_cabinet_information.html'

    def get(self, request,*args, **kwargs):
        if request.user.is_authenticated:
            masta = request.user.groups.all()
            obj = get_object_or_404(self.model, slug__iexact=masta[0])
            context = self.get_context_data(**kwargs)
            context['company'] = obj
            return self.render_to_response(context)
        else:
            return redirect('administration_url')

    def post(self, request):
        pass


class BaseCompanyOrders(TemplateView):
    model=Company
    template_name ='cabinet/includes/base_cabinet/base_company_orders.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            masta = request.user.groups.all()
            obj = get_object_or_404(self.model, slug__iexact=masta[0])
            masters= obj.masters_set.all() #TODO Проверить отправляется ли пустной список
            orders = obj.order_set.all() #все заказы компании

            context = self.get_context_data(**kwargs)
            context['company'] = obj
            context['order']= orders
            if masters is not None:
                context['masters'] = masters
            return self.render_to_response(context)
        else:
            return redirect('administration_url')


class BaseCompanyMasters(TemplateView):
    model=Company
    template_name ='cabinet/includes/base_cabinet/base_company_masters.html'

    def get(self, request, slug, *args, **kwargs):
        if request.user.is_authenticated:
            masta = request.user.groups.all()
            obj = get_object_or_404(self.model, slug__iexact=masta[0])
            masters= obj.masters_set.all() #TODO Проверить отправляется ли пустной список
            mastersform= MastersForm(self.request.POST or None)

            context = self.get_context_data(**kwargs)
            context['company'] = obj
            context['mastersform'] = mastersform
            if masters is not None:
                context['masters'] = masters
            return self.render_to_response(context)
        else:
            return redirect('administration_url')


class BaseCompanyFoto(TemplateView):
    model=Company
    template_name ='cabinet/includes/base_cabinet/base_company_foto.html'

    def get(self, request):
        pass
    def post(self, request):
        pass


class BaseCompanyDescription(TemplateView):
    model=Company
    template_name ='cabinet/includes/base_cabinet/base_company_description.html'
    
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            masta = request.user.groups.all()
            companyform= CompanyCabinetForm(self.request.POST or None)
            obj = get_object_or_404(self.model, slug__iexact=masta[0])
            operations = obj.operations_set.all()            
            all_operations = Operations.objects.all()

            context = self.get_context_data(**kwargs)
            context['company'] = obj
            context['companyform'] = companyform
            context['servises'] = operations
            context['operations'] = all_operations

            return self.render_to_response(context)
        else:
            return redirect('administration_url')


class CreateMaster(View):
    def post(self,request, *args, **kwargs):
        if request.method=='POST':
            for i in request.POST['number_m']:
                if ((ord(i)<48 or ord(i)>57) and ord(i)!=43):
                    return HttpResponse('ne ok')
            obj = get_object_or_404(Company, slug__iexact=request.POST['slug'])
            masters = obj.masters_set.all()
            mastersform = MastersForm(request.POST)
            if mastersform.is_valid():
                mastersform.clean()
                mastersform.save(obj)
                mastersform = MastersForm()
                return HttpResponse('ok')
            else:
                mastersform.clean()
                erors_m='Не верная форма, возможно пользователь с таким номером уже существует'
                return HttpResponse('ne ok')    
            
        if request.method=='POST' and 'e' in request.POST:
            return HttpResponse('ne ok')


class CreteOperation(View):
    def post(self, request):
        if request.method == "POST":
            
            create_operations = CreateOperations(request.POST)
            if create_operations.is_valid():
                create_operations.clean()
                try:
                    obj = get_object_or_404(Company, slug__iexact=request.POST['slug'])
                except:
                    return redirect('administration_url')
                new_oper = create_operations.cleaned_data['name'].lower()
                new_oper = new_oper[0].upper()+new_oper[1:]
                if Operations.objects.filter(name_operations='new_oper'):
                    errors = 'ОШИБКА проверьте пожалуйста данные возможно такая услуга присутствует в базе'
                else:
                    oper = Operations(name_operations=new_oper, company=obj)
                    oper.save()
                    errors = ''
            else:
                errors = 'ОШИБКА проверьте пожалуйста данные'       
            return JsonResponse({'new_oper':new_oper, 'errors':errors})
        else: 
            return redirect('administration_url')
