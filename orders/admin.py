from django.contrib import admin

# Register your models here.
from .models import Order, OrderItem
from django.utils.safestring import mark_safe
from django.urls import reverse

#This displays the order items in a tabular form directly inside the parent Model (order)
#so for each order, dis play the order items
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

def order_payment(obj):
    url = obj.get_stripe_url()
    if obj.stripe_id:
        html = f'<a href="{url}" target="_blank">{obj.stripe_id}</a>'
        return mark_safe(html)
    return ''


order_payment.short_description = 'Stripe payment'



def order_pdf(obj):
    url = reverse('orders:admin_order_pdf', args=[obj.id])
    return mark_safe(f'<a href="{url}">PDF</a>')
order_pdf.short_description = 'Invoice'

import csv
import datetime
from django.http import HttpResponse


def order_detail(obj):
    url = reverse('orders:admin_order_detail', args=[obj.id])
    #escaping is converting template tags to their literal to avoid injections
    #marking safe is sotring without converting/use when the Html is from backend
    return mark_safe(f'<a href="{url}">View</a>')

def export_to_csv(modeladmin, request, queryset):

    #Gets Passed in model metadata
    opts = modeladmin.model._meta

    #sets a csv file name
    content_disposition = (
    f'attachment; filename={opts.verbose_name}.csv')
    #Tells the browser this is a csv file rather than HTML
    response = HttpResponse(content_type='text/csv')
    #Tells browser to download rather than display
    response['Content-Disposition'] = content_disposition
    #Loads the response object directly into the CSV writer (Response object is file-like in django)
    writer = csv.writer(response)
    #Excluding unsupported field types in CSV
    fields = [field for field in opts.get_fields()
    if not field.many_to_many and not field.one_to_many
    ]

    #Write a first row with header information
    writer.writerow([field.verbose_name for field in fields])
    # Write data rows
    for obj in queryset:
        data_row = []
        for field in fields:
            #get attr just get an object instance attribute, field.name makes sure the obj attr and feld attr matches
            #value = getattr(obj, email) gets the email attr from the obj dynamically
            value = getattr(obj, field.name)
            #checks if a value is of a particular type
            if isinstance(value, datetime.datetime):
                #Converting the date to more readable
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response

export_to_csv.short_description = 'Export to CSV'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    
    list_display = [
    'id',
    'first_name',
    'last_name',
    'email',
    'address',
    'postal_code',
    'city',
    'paid',
    order_payment,
    'created',
    'updated',
    order_detail,
    order_pdf,
    'coupon',
 
    ]
    list_filter = ['paid', 'created', 'updated'] 

    inlines = [OrderItemInline]
    actions = [export_to_csv]


@admin.register(OrderItem)
class OrderItemsAdmin(admin.ModelAdmin):
    list_display = [
    'price',
 
    ]



#Now this entire export starts and finishes in the request cycle, for large dataset
#The server can close the connection before the export completes, so we should try
#Assigning the task to a celeryy worker