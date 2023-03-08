from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from embed_video.admin import AdminVideoMixin
from food.models import Product,Contact,Orders,OrderUpdate
# Register your models here.
admin.site.register(Contact)
class OrderFilter(AdminVideoMixin, admin.ModelAdmin):
    pass

class Filter(admin.ModelAdmin):
    list_display = ('update_id','order_id','update_desc')
    list_filter = ['update_desc']
admin.site.register(OrderUpdate,Filter)
class OrderFilter(AdminVideoMixin, admin.ModelAdmin):
    pass
class Filter2(admin.ModelAdmin):
    list_display = ('product_name','price','category',)
    list_filter = ['category']
admin.site.register(Product,Filter2)
class OrderFilter(AdminVideoMixin, admin.ModelAdmin):
    pass
class Filter3(admin.ModelAdmin):
    list_display = ('order_id','name','amountpaid','paymentstatus')
    list_filter = ['paymentstatus']
admin.site.register(Orders,Filter3)

