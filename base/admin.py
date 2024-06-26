from django.contrib import admin
from . models import Profile,Contribution,Month,Chat,Product
# Register your models here.

admin.site.register(Profile)
admin.site.register(Contribution)
admin.site.register(Month)
admin.site.register(Chat)
admin.site.register(Product)
