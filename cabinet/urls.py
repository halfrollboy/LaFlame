from django.urls import path, re_path
from .views import *

app_name = 'cabinet'
urlpatterns = [
    path('cabinet/<str:slug>/', MixinDetailCabinet.as_view(), name='cabinet_main_page'),#TODO передать название компании
    path('cabinet/master/<str:slug>/',DetailCabinetMasters.as_view(),name='cabinet_masters_company_url'),
    path('information/<str:slug>/', BaseInformation.as_view(), name='base_information_new'),
    path('orders/<str:slug>/', BaseCompanyOrders.as_view(), name='base_company_orders_new'),
    path('masters/<str:slug>/', BaseCompanyMasters.as_view(), name='base_company_masters_new'),
    path('foto/<str:slug>/', BaseCompanyFoto.as_view(), name='base_company_foto_new'),
    path('description/<str:slug>/', BaseCompanyDescription.as_view(), name='base_company_description_new'),
    re_path(r'base_information/$',BaseInformation.as_view(), name='base_information'),
    re_path(r'base_company_orders/$',BaseCompanyOrders.as_view(),name='base_company_orders'),
    re_path(r'base_company_masters/$',CreateMaster.as_view(),name='base_company_masters'),
    re_path(r'base_company_foto/$',BaseCompanyFoto.as_view(), name='base_company_foto'),
    re_path(r'base_company_description/$',CreteOperation.as_view(),name='base_company_description'),
    re_path(r'orders/$', OrderCabinet.as_view(), name='orders'),
    re_path(r'profile/$', ProfileCabinet.as_view(), name='profile'),
    re_path(r'timetable/$', TimetableCabinet.as_view(), name='timetable'),
    re_path(r'delete_masters_form/$',Delete_masters_form.as_view(), name='delete_master_form'),
    re_path(r'create_operation/$', CreteOperationMaster.as_view(), name='profile'),
]
