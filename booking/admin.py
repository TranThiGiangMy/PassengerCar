from django.contrib import admin
from django.contrib.auth.models import Permission
from django.db.models import Count
from django.template.response import TemplateResponse
from django.urls import path
from django.utils.html import mark_safe
from .models import User, UserType, UserInfo, Train, Routes, Tickets, Booking, Payment, Bill \
    , Tag, Comment
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib.auth.models import Group


class BookingappAdminSite(admin.AdminSite):
    site_header = "booking app"

    def get_urls(self):
        return [
                   path('train_stats/', self.train_stats)
               ] + super().get_urls()

    def train_stats(self, request):
        c = Train.objects.count()
        stats = Train.objects.annotate(train_count=Count('route_trains')).values('id', 'train_count')
        return TemplateResponse(request, 'admin/train_stats.html', {
            'c': c,
            'stats': stats
        })


admin_site = BookingappAdminSite('myapp')


# Register your models here.
class UserInfoForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = UserInfo
        fields = '__all__'


class UserInfoAdmin(admin.ModelAdmin):
    search_fields = ['id', 'name']
    list_filter = ['name', 'created_date']
    list_display = ['id', 'name', 'phone', 'created_date']
    readonly_fields = ['image_view']
    form = UserInfoForm

    def image_view(self, customer):
        if customer:
            return mark_safe(
                '<img src="/static/{url}" width="120" />' \
                    .format(url=customer.image.name)
            )


class TrainInLine(admin.StackedInline):
    model = Train
    fk_name = 'route_train'


class TrainTagInLine(admin.StackedInline):
    model = Train.tags.through


class RoutesAdmin(admin.ModelAdmin):
    search_fields = ['starting_point', 'ending_point']
    list_filter = ['starting_point', 'ending_point']
    list_display = ['id', 'starting_point', 'ending_point', 'distance']
    inlines = [TrainInLine]


class TrainAdmin(admin.ModelAdmin):
    search_fields = ['starting_date', 'ending_date']
    list_filter = ['starting_date', 'ending_date']
    list_display = ['id', 'starting_date', 'ending_date']
    inlines = [TrainTagInLine]


class TicketsAdmin(admin.ModelAdmin):
    search_fields = ['id', 'price']
    list_filter = ['price', 'created_date', 'upp_date']
    list_display = ['id', 'price', 'created_date', 'upp_date']


class BookingAdmin(admin.ModelAdmin):
    search_fields = ['ticket__price', 'number', 'train__date', 'routes_point']  # tìm kiếm
    list_filter = ['id', 'number', ]
    list_display = ['id', 'number', 'price', 'point', 'date']  # hiển thị các cột


class PaymentAdmin(admin.ModelAdmin):
    search_fields = ['id']
    list_filter = ['cash', 'banking']
    list_display = ['id', 'cash', 'banking']


class BillAdmin(admin.ModelAdmin):
    search_fields = ['id', 'total', 'created_date']
    list_filter = ['total']
    list_display = ['id', 'total', 'created_date']


class CommentAdmin(admin.ModelAdmin):
    search_fields = ['content', 'created_date', 'upded_date']
    list_filter = ['content', 'created_date', 'upded_date']
    list_display = ['content', 'created_date', 'upded_date']


admin_site.register(Group)
admin_site.register(Permission)
admin_site.register(User)
admin_site.register(UserType)
admin_site.register(UserInfo, UserInfoAdmin)
admin_site.register(Train, TrainAdmin)
admin_site.register(Routes, RoutesAdmin)
admin_site.register(Tickets, TicketsAdmin)
admin_site.register(Booking, BookingAdmin)
admin_site.register(Payment, PaymentAdmin)
admin_site.register(Bill, BillAdmin)
admin_site.register(Comment, CommentAdmin)
admin_site.register(Tag)
