from django.db import models


class Order(models.Model):
    STATUS_CHOICES = (
        ("new", "Новая"),
        ("confirmed", "Подтвержденная"),
        ("completed", "Завершена"),
        ("canceled", "Отменена"),
    )

    name = models.CharField(max_length=100, verbose_name="Имя")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    comment = models.CharField(max_length=500, null=True, blank=True, verbose_name="Комментарий")
    status = models.CharField(choices=STATUS_CHOICES, default="new", max_length=20, verbose_name="Статус")
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="Дата создания")
    date_updated = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name="Дата обновления")
    master = models.ForeignKey("Master", on_delete=models.SET_NULL, null=True, verbose_name="Мастер")
    appointment_date = models.DateField(null=True, blank=True, verbose_name="Дата записи")
    services = models.ManyToManyField("Service", verbose_name="Услуги", default=None, related_name="orders")
    
    def __str__(self):
        return f"{self.name} - {self.phone}"
    
    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


from django.db import models

class Master(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    experience = models.IntegerField(default=0, verbose_name="Опыт работы (лет)")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    services = models.ManyToManyField("Service", verbose_name="Услуги", related_name="masters")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Мастер"
        verbose_name_plural = "Мастера"

class Service(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    duration = models.IntegerField(verbose_name="Длительность (мин)")
    is_popular = models.BooleanField(default=False, verbose_name="Популярная услуга")
    
    def __str__(self):
        return f"{self.name} - {self.price} ₽"
    
    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

class Review(models.Model):
    master = models.ForeignKey(Master, on_delete=models.CASCADE, related_name="reviews", verbose_name="Мастер")
    author_name = models.CharField(max_length=100, verbose_name="Имя автора")
    text = models.TextField(verbose_name="Текст отзыва")
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], verbose_name="Оценка")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    def __str__(self):
        return f"Отзыв от {self.author_name} о {self.master.name}"
    
    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
