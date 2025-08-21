# core/views.py
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseNotAllowed
from django.contrib import messages
from .data import orders
from .models import Order, Master, Service, Review
from .forms import ServiceForm, OrderForm, ReviewModelForm, ReviewForm
from django.db.models import Q, Count, Sum


def get_services_by_master(request, master_id):
    """AJAX endpoint для получения услуг мастера"""
    master = get_object_or_404(Master, id=master_id)
    services = master.services.all()
    
    services_data = [
        {
            'id': service.id,
            'name': service.name,
            'price': float(service.price)
        }
        for service in services
    ]
    
    return JsonResponse({'services': services_data})

def review_create(request):
    if request.method == "GET":
        form = ReviewModelForm()
        return render(request, "review_class_form.html", {"form": form})
    
    elif request.method == "POST":
        form = ReviewModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("landing")
        else:
            return render(request, "review_class_form.html", {"form": form})




def landing(request):
    """Главная страница"""
    masters = Master.objects.all()[:3]
    services = Service.objects.all()[:6]
    reviews = Review.objects.select_related('master').filter(status='approved')[:5]
    
    context = {
        'masters': masters,
        'services': services,
        'reviews': reviews,
    }
    return render(request, 'landing.html', context)


def thanks(request):
    """Страница благодарности"""
    return render(request, 'thanks.html')


def orders_list(request):
    """Список заявок"""
    orders = Order.objects.select_related('master').prefetch_related('services').all().order_by('-date_created')
    context = {'orders': orders}
    return render(request, 'orders_list.html', context)


def order_detail(request, pk):
    """Детали заявки"""
    order = get_object_or_404(
        Order.objects.prefetch_related("services")
        .select_related("master")
        .annotate(total_price=Sum("services__price")),
        id=pk
    )
    context = {"order": order}
    return render(request, "order_detail.html", context)


def order_create(request):
    """Создание заявки"""
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Заявка успешно отправлена!")
            return redirect("thanks")
    else:
        form = OrderForm()
    return render(request, "order_class_form.html", {"form": form})

def create_order(request):
    """Альтернативное представление для создания заявки"""
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Заявка успешно отправлена!")
            return redirect("thanks")
    else:
        form = OrderForm()
    return render(request, "order_form.html", {"form": form})


def order_update(request, order_id):
    """
    Отвечает за маршрут 'orders/<int:order_id>/update/'
    """
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return HttpResponse("Заказ не найден", status=404)

    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, f"Заказ №{order.id} успешно обновлен.")
            return redirect("order_detail", order_id=order.id)
    else:
        form = OrderForm(instance=order)

    context = {
        "form": form,
        "operation_type": f"Обновление заказа №{order.id}",
    }
    return render(request, "order_class_form.html", context)

def create_review(request):
    """Создание отзыва"""
    if request.method == "POST":
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Отзыв успешно отправлен!")
            return redirect("thanks")
    else:
        form = ReviewForm()
    return render(request, "review_form.html", {"form": form})

def services_list(request):
    services = Service.objects.all()
    return render(request, "services_list.html", {"services": services})


def service_create(request):
    if request.method == "GET":
        # Создать пустую форму
        form = ServiceForm()
        context = {
            "operation_type": "Создание услуги",
            "form": form,
        }
        return render(request, "service_class_form.html", context=context)

    elif request.method == "POST":
        # Создаем форму и помещаем в нее данные из POST-запроса
        form = ServiceForm(request.POST)

        # Проверяем, что форма валидна
        if form.is_valid():
            # Добываем данные из формы
            name = form.cleaned_data["name"]
            description = form.cleaned_data["description"]
            price = form.cleaned_data["price"]
            duration = form.cleaned_data["duration"]
            is_popular = form.cleaned_data["is_popular"]
            image = form.cleaned_data["image"]

            # Создать объект услуги
            service = Service(
                name=name,
                description=description,
                price=price,
                duration=duration,
                is_popular=is_popular,
                image=image,
            )
            # Сохранить объект в БД
            service.save()

            # Перенаправить на страницу со списком услуг
            return redirect("services-list")
        else:
            context = {
                "operation_type": "Создание услуги",
                "form": form,
            }
            return render(request, "service_class_form.html", context=context)

    else:
        # Вернуть ошибку 405 (Метод не разрешен)
        return HttpResponseNotAllowed(["GET", "POST"])


def service_update(request, service_id):
    """
    Отвечает за маршрут 'services/<int:service_id>/update/'
    """
    try:
        service = Service.objects.get(id=service_id)
    except Service.DoesNotExist:
        # Если нет такой услуги, вернем 404
        return HttpResponse("Услуга не найдена", status=404)

    if request.method == "GET":
        # Для GET-запроса создаем форму, связанную с существующим объектом
        form = ServiceForm(instance=service)
        context = {
            "operation_type": "Обновление услуги",
            "form": form,
        }
        return render(request, "service_class_form.html", context=context)

    elif request.method == "POST":
        # Для POST-запроса создаем форму с данными из запроса и связываем с объектом
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            # Если форма валидна, сохраняем изменения
            form.save()
            messages.success(request, f"Услуга '{service.name}' успешно обновлена.")
            return redirect("services-list")
        else:
            # Если форма невалидна, снова отображаем страницу с формой и ошибками
            context = {
                "operation_type": "Обновление услуги",
                "form": form,
            }
            return render(request, "service_class_form.html", context=context)

    else:
        # Для всех других методов возвращаем ошибку
        return HttpResponseNotAllowed(["GET", "POST"])
