from django.forms import BaseModelForm
from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse, HttpResponseNotAllowed
from django.contrib import messages
from .models import Order, Master, Service, Review
from .forms import ServiceForm, OrderForm, ReviewModelForm
from django.db.models import Q, Count, Sum, F
# Импорт миксинов для проверки прав
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
# Импорт классовых вью, View, TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)
from django.urls import reverse_lazy, reverse

class UserIsStuffPassedMixin(UserPassesTestMixin):
    """
    Миксин для проверки, является ли пользователь персоналом сайта
    """
    def test_func(self):
        """
        Метод от ответа которого будет зависеть доступ к вью
        """
        return self.request.user.is_staff

class AjaxMasterServicesView(View):
    """
    Вью для отдачи массива объектов услуг по ID мастера.
    Обслуживает AJAX запросы формы создания заказа.
    """
    def get(self, request, master_id):
        master = Master.objects.prefetch_related("services").get(id=master_id)
        services = master.services.all()
        services_data = [
            {"id": service.id, "name": service.name} for service in services
        ]
        return JsonResponse({"services": services_data})

class ReviewCreateView(CreateView):
    model = Review
    form_class = ReviewModelForm
    template_name = 'review_form.html'
    success_url = reverse_lazy('thanks')

    def form_valid(self, form):
        messages.success(self.request, 'Отзыв успешно создан!')
        return super().form_valid(form)

class LandingView(TemplateView):
    template_name = 'landing.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['masters'] = Master.objects.all()
        context['reviews'] = Review.objects.all()
        return context

class ThanksView(TemplateView):
    template_name = 'thanks.html'

    def get_context_data(self, **kwargs):
        """
        Расширение get_context_data для возможности передать в шаблон {{ title }} и {{ message }}.
        Они будут разные, в зависимости от куда пришел человек.
        Со страницы order/create/ с псевдонимом order-create
        Или со страницы review/create/ с псевдонимом review-create
        """
        context = super().get_context_data(**kwargs)
        if kwargs["source"]:
            source = kwargs["source"]
            if source == "order-create":
                context["title"] = "Спасибо за заказ!"
                context["message"] = (
                    "Ваш заказ принт. Скоро с вами свяжется наш менеджер для уточнения деталей."
                )
            elif source == "review-create":
                context["title"] = "Спасибо за отзыв!"
                context["message"] = (
                    "Ваш отзыв принят и отправлен на модерацию. После проверки он появится на сайте."
                )
            else:
                context["title"] = "Спасибо!"
                context["message"] = "Спасибо за ваше обращение!"
        return context

class OrdersListView(ListView):
    model = Order
    template_name = 'orders_list.html'
    context_object_name = 'orders'
    ordering = ['-date_created']

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q', '')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(phone__icontains=search_query) |
                Q(comment__icontains=search_query)
            )
        return queryset

class OrderDetailView(DetailView):
    model = Order
    template_name = 'order_detail.html'
    context_object_name = 'order'

    def get_queryset(self):
        """
        Лучшее место для "жадной" загрузки и аннотаций.
        Этот метод подготавливает оптимизированный QuerySet.
        """
        queryset = super().get_queryset()
        return (
            queryset.select_related("master")
            .prefetch_related("services")
            .annotate(total_price=Sum("services__price"))
        )

    def get_object(self, queryset=None):
        """
        Лучшее место для логики, специфичной для одного объекта.
        Например, для счетчика просмотров.
        """
        # Сначала получаем объект стандартным способом (он будет взят из queryset,
        # который мы определили в get_queryset)
        order = super().get_object(queryset)
        # Теперь выполняем логику с сессией и счетчиком
        session_key = f"order_{order.id}_viewed"
        if not self.request.session.get(session_key):
            self.request.session[session_key] = True
            # Атомарно увеличиваем счетчик в БД
            order.view_count = F("view_count") + 1
            order.save(update_fields=["view_count"])
            # Обновляем объект из БД, чтобы в шаблоне было актуальное значение
            order.refresh_from_db()
        return order

class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'order_form.html'
    success_url = reverse_lazy('thanks')

    def form_valid(self, form):
        messages.success(self.request, 'Заявка успешно создана!')
        return super().form_valid(form)

class OrderUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = "core.change_order"
    model = Order
    form_class = OrderForm
    template_name = "order_class_form.html"
    success_url = reverse_lazy("orders")
    success_message = "Заказ успешно обновлен!"
    pk_url_kwarg = "order_id"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        messages.success(self.request, self.success_message)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["operation_type"] = "Редактирование заказа"
        return context

class ServicesListView(LoginRequiredMixin, ListView):
    model = Service
    # queryset = Service.objects.all().order_by("-price")
    template_name = "services_list.html"
    # object_list - стандартное имя для списка объектов
    # context_object_name = "services"

class ServiceCreateView(UserIsStuffPassedMixin, CreateView):
    form_class = ServiceForm
    template_name = "service_class_form.html"
    success_url = reverse_lazy("services-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["operation_type"] = "Создание услуги"
        return context

    def form_valid(self, form):
        messages.success(self.request, "Услуга успешно создана!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, "Ошибка валидации формы! Проверьте введенные данные."
        )
        return super().form_invalid(form)

class ServiceUpdateView(UserIsStuffPassedMixin, UpdateView):
    model = Service
    form_class = ServiceForm
    template_name = "service_class_form.html"
    success_url = reverse_lazy("services-list")
    # Стандартное имя - pk, если в url другое - мы можем дать название тут
    pk_url_kwarg = "service_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["operation_type"] = "Редактирование услуги"
        return context

    def form_valid(self, form):
        messages.success(self.request, "Услуга успешно обновлена!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, "Ошибка валидации формы! Проверьте введенные данные."
        )
        return super().form_invalid(form)