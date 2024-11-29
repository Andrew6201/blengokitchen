from django.contrib import admin
from . models import Profile,Contribution,Month,Chat,Product,Theimages,ConfirmPayment,OrderMade,AboutImages,ContactMessage
# Register your models here.

admin.site.register(Profile)
admin.site.register(Contribution)
admin.site.register(Month)
admin.site.register(Chat)
admin.site.register(Product)
admin.site.register(Theimages)
admin.site.register(ConfirmPayment)
admin.site.register(OrderMade)
admin.site.register(AboutImages)
admin.site.register(ContactMessage)
