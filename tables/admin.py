from django.contrib import admin
from .models import Role, Gender, Subscription, GeneralTable, HelpRequest


# Register your models here.
admin.site.register(Role)
admin.site.register(Gender)
admin.site.register(Subscription)
admin.site.register(GeneralTable)
admin.site.register(HelpRequest)
