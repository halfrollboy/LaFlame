from django.urls import path, re_path, include
from django.conf.urls import url
from .views import *

urlpatterns = [
    path('',post_list, name='hello_page_url'),
    
    path('company/', CompanyList.as_view(), name='company_list_url'),
    path('company/<str:slug>/', CompanyDetail.as_view(), name='company_detail_url'),
    path('newcompany/', CreateNewCompany.as_view(),name='new_company'),
    #path('cabinet/', MixinDetailCabinet.as_view(),name='cabinet_company_url'),
    #path('cabinet/<str:slug>/',DetailCabinetMasters.as_view(),name='cabinet_masters_company_url'),
    path('company/administration',Administration.as_view(), name='administration_url'),
    path('masters_list', MastersList.as_view(), name='masters_list_url'),
    path('masters/<str:slug>/', MasterDetail.as_view(), name='maseters_detail_url'), 
    re_path(r'masters_ajax/$', masters_ajax, name='masters_ajax'),#попробую сделать аякс (рабочий аякс)
    re_path(r'logout/$', logout_user, name='logout'),
    url(r'^user/check/$',create_user),
    url(r'^login$', Administration.as_view(), name='login_page'),  
]
