from django.contrib import admin
from .models import Company, Masters, OperationsDetailNas, NewCompany

# Register your models here.
admin.site.register(Company)
admin.site.register(Masters)
admin.site.register(OperationsDetailNas)
admin.site.register(NewCompany)

# @admin.register(Company)
# class CompanyAdmin(admin.ModelAdmin):
#     list_display = {'name', 'city', 'number'}
#     search_fields = {'name', 'city','number'}
