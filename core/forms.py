from django import forms
from .models import Order, Service, Review, Master
from django.utils import timezone
from datetime import datetime


class ReviewModelForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['name', 'text', 'rating', 'master', 'photo']
        widgets = {
            'text': forms.Textarea(attrs={"class": "form-control"}),
            'name': forms.TextInput(attrs={"class": "form-control"}),
            'rating': forms.Select(attrs={'class': 'form-control'}),
            'master': forms.Select(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={"class": "form-control"}),
        }

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Название услуги"}
            ),
            "description": forms.Textarea(
                attrs={"placeholder": "Описание услуги", "class": "form-control"}
            ),
            "price": forms.NumberInput(attrs={"class": "form-control"}),
            "duration": forms.NumberInput(attrs={"class": "form-control"}),
            "is_popular": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "image": forms.FileInput(attrs={"class": "form-control"}),
        }
        help_texts = {
            "description": "Введите продающее описание услуги",
            "image": "Квадратное изображение не меньше 500х500",
        }


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name', 'phone', 'comment', 'master', 'services', 'appointment_date']
        widgets = {
            "name": forms.TextInput(
                attrs={"placeholder": "Ваше имя", "class": "form-control"}
            ),
            "phone": forms.TextInput(
                attrs={"placeholder": "+7 (999) 999-99-99", "class": "form-control"}
            ),
            "comment": forms.Textarea(
                attrs={"placeholder": "Комментарий к заказу", "class": "form-control", "rows": 3}
            ),
            'master': forms.Select(attrs={"class": "form-control", "id": "id_master"}),
            "services": forms.CheckboxSelectMultiple(
                attrs={"class": "form-check-input"}
            ),
            "appointment_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        master = cleaned_data.get('master')
        services = cleaned_data.get('services')
        
        if master and services:
            # Получаем услуги, которые предоставляет выбранный мастер
            master_services = master.services.all()
            
            # Проверяем, что все выбранные услуги есть у мастера
            for service in services:
                if service not in master_services:
                    raise forms.ValidationError(
                        f"Мастер {master.name} не предоставляет выбранные услуги"
                    )
        
        return cleaned_data

class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [
        (1, '1 - Ужасно'),
        (2, '2 - Плохо'),
        (3, '3 - Средне'),
        (4, '4 - Хорошо'),
        (5, '5 - Отлично'),
    ]
    
    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Оценка"
    )
    
    class Meta:
        model = Review
        fields = ['master', 'rating', 'name', 'text']
        widgets = {
            'master': forms.Select(attrs={"class": "form-control"}),
            'name': forms.TextInput(
                attrs={"placeholder": "Ваше имя", "class": "form-control"}
            ),
            'text': forms.Textarea(
                attrs={"placeholder": "Ваш отзыв", "class": "form-control", "rows": 4}
            ),
        }
        labels = {
            'master': 'Мастер',
            'name': 'Ваше имя',
            'text': 'Отзыв',
        }