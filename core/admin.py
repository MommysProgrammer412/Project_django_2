from typing import Any
from django.contrib import admin
from django.db.models import QuerySet, Sum, Count
from django.utils import timezone
from datetime import timedelta
from .models import Master, Order, Service, Review

# Кастомный фильтр по общей сумме заказа
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
        if self.value() == 'one_thousends':
            return queryset.filter(total_price_agg__gte=500, total_price_agg__lt=1000)
        if self.value() == 'two_thousends':
            return queryset.filter(total_price_agg__gte=1000, total_price_agg__lt=2000)
        if self.value() == 'up_two_thousends':
            return queryset.filter(total_price_agg__gte=2000)
        return queryset

# Кастомный фильтр по дате записи
class AppointmentDateFilter(admin.SimpleListFilter):
    title = 'По дате записи'
    parameter_name = 'appointment_date'

    def lookups(self, request, model_admin):
        return (
            ('today', 'Сегодня'),
            ('tomorrow', 'Завтра'),
            ('this_week', 'На этой неделе'),
        )

    def queryset(self, request, queryset):
        today = timezone.now().date()
        if self.value() == 'today':
            return queryset.filter(appointment_date=today)
        if self.value() == 'tomorrow':
            tomorrow = today + timedelta(days=1)
            return queryset.filter(appointment_date=tomorrow)
        if self.value() == 'this_week':
            start_of_week = today - timedelta(days=today.weekday())
            end_of_week = start_of_week + timedelta(days=6)
            return queryset.filter(appointment_date__range=[start_of_week, end_of_week])
        return queryset

# Инлайн для услуг в заказе
class ServiceInline(admin.TabularInline):
    model = Order.services.through
    extra = 1
    verbose_name = "Услуга"
    verbose_name_plural = "Услуги"

# Инлайн для отзывов о мастере
class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1
    verbose_name = "Отзыв"
    verbose_name_plural = "Отзывы"

# Регистрация Order с кастомным админ-классом
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 
                    'name', 
                    'phone', 
                    'master',
                    'date_created',
                    'appointment_date',
                    'status', 
                    'total_price',
                    'total_income',
                    )
    search_fields = ('name', 'phone', 'comment',)

    list_filter = ('status', 'master', TotalOrderPrice, AppointmentDateFilter)

    list_per_page = 20

    list_display_links = ('id', 'phone', 'name')

    list_editable = ('status',)

    readonly_fields = ('date_created', 'date_updated', 'total_price', 'total_income')

    actions = ('mark_completed', 'mark_canceled', 'mark_new', 'mark_confirmed')

    filter_horizontal = ('services',)
    
    inlines = [ServiceInline]

    # Исключаем services из полей, так как они будут отображаться через инлайн
    fieldsets = (
        ("Основная информация", {"fields": ("name", "phone", "status", "comment")}),
        ("Детали записи", {"fields": ("master", "appointment_date")}),
        (
            "Финансовая информация (только для чтения)",
            {
                "classes": ("collapse",),
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

# Регистрация Master с кастомным админ-классом
@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'experience', 'is_active', 'services_count')
    list_filter = ('is_active', 'services')
    search_fields = ('name',)
    filter_horizontal = ('services',)
    inlines = [ReviewInline]
    
    @admin.display(description='Количество услуг')
    def services_count(self, obj):
        return obj.services.count()

# Регистрация Service с кастомным админ-классом
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration', 'is_popular')
    list_filter = ('is_popular',)
    search_fields = ('name',)