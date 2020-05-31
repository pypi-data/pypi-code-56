from django.contrib import admin
from mpesaApp.models import mpesaDetail,payment,QueryURLS
# Register your models here.


class paymentItemAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'CheckoutRequestID',
        'amount',
        'phone',
        'created',
        'success',
        'payment_status_message'
    ]
    list_filter = ['title', 'amount', 'success']
    search_fields = ['success', 'phone', 'title']

admin.site.register(mpesaDetail)
admin.site.register(payment,paymentItemAdmin)
admin.site.register(QueryURLS)