from typing import Any
from django.contrib import admin
from django.db.models import QuerySet, Sum
from .models import Master, Order, Service, Review

admin.site.register(Master)
# admin.site.register(Order)
admin.site.register(Service)

class TotalOrderPrice(admin.SimpleListFilter):
    title = 'По общей сумме заказа'
    parameter_name = 'total_order_price'

    def lookups(self, request, model_admin):
        'Возвращают варианты фильтра'
        return(
            ('five_hundreds', 'До 500'),
            ('one_thousends', 'До 1000'),
            ('two_thousends', 'До 2000'),
            ('up_two_thousends', 'Свыше 2 тысяч'),
        )
    def queryset(self, request, queryset):
        queryset = queryset.annotate(total_price_agg=Sum('services__price'))
        if self.value() == 'five_hundreds':
            return queryset.filter(total_price_agg__lt=500)
        if self.value() == 'one_thousends':  # Исправлено
            return queryset.filter(total_price_agg__gte=500, total_price_agg__lt=1000)
        if self.value() == 'two_thousends':  # Исправлено
            return queryset.filter(total_price_agg__gte=1000, total_price_agg__lt=2000)
        if self.value() == 'up_two_thousends':  # Исправлено
            return queryset.filter(total_price_agg__gte=2000)
        return queryset

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('name', 
                    'phone', 
                    'master',
                    'date_created',
                    'appointment_date',
                    'status', 
                    'total_price',
                    'total_income',
                    )
    search_fields = ('name', 'phone', 'comment',)

    list_filter = ('status', 'master', TotalOrderPrice)

    list_per_page = 5

    list_display_links = ('phone', 'name')

    list_editable = ('status',)

    readonly_fields = ('date_created', 'date_updated', 'total_price', 'total_income')

    actions = ('mark_completed', 'mark_canceled', 'mark_new', 'mark_confirmed')

    filter_horizontal = ('services',)

    # Группируем поля на странице редактирования
    fieldsets = (
        ("Основная информация", {"fields": ("name", "phone", "status", "comment")}),
        ("Детали записи", {"fields": ("master", "appointment_date", "services")}),
        (
            "Финансовая информация (только для чтения)",
            {
                "classes": ("collapse",),  # Делаем блок сворачиваемым
                "fields": ("total_price", "total_income"),
            },
        ),
        (
            "Служебная информация (только для чтения)",
            {"classes": ("collapse",), "fields": ("date_created", "date_updated")},
        ),
    )

    @admin.action(description='Отметить как завершенные')
    def mark_completed(self, request, queryset):
        queryset.update(status='completed')

    @admin.action(description='Отметить как отмененные')
    def mark_canceled(self, request, queryset):
        queryset.update(status='canceled')

    @admin.action(description='Отметить как новые')
    def mark_new(self, request, queryset):
        queryset.update(status='new')
    
    @admin.action(description='Отметить как подтвержденные')
    def mark_confirmed(self, request, queryset):
        queryset.update(status='confirmed')

    @admin.display(description='Общая стоимость')
    def total_price(self, obj):
        return sum([service.price for service in obj.services.all()])
    
    @admin.display(description='Выручка по номеру')
    def total_income(self, obj):
        orders = Order.objects.filter(phone=obj.phone, status='completed').prefetch_related('services')
        return sum([service.price for order in orders for service in order.services.all()])
    
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['master', 'rating', 'status', 'created_at']
    list_filter = ['master', 'rating','status']
    search_fields = ['master__name', 'comment']
    readonly_fields = ['created_at', 'rating']
    list_editable = ['status']
    list_per_page = 10
    actions = ['check_published']
    @admin.action(description='Опубликовать отзыв')
    def check_published(self, request, queryset):
        queryset.update(status='published')