import os
import django
import random
from datetime import datetime, timedelta

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barbershop.settings')
django.setup()

# Импортируем модели после настройки Django
from core.models import Master, Service, Order, Review
from django.contrib.auth.models import User

def create_superuser():
    """Создание суперпользователя, если его нет"""
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', '123')
        print("Суперпользователь создан: admin/123")
    else:
        # Если пользователь уже существует, обновим его пароль
        admin_user = User.objects.get(username='admin')
        admin_user.set_password('123')
        admin_user.save()
        print("Пароль суперпользователя admin обновлен на: 123")

def create_services():
    """Создание услуг"""
    services_data = [
        {
            'name': 'Мужская стрижка',
            'description': 'Классическая мужская стрижка с укладкой',
            'price': 1500.00,
            'duration': 45,
            'is_popular': True,
        },
        {
            'name': 'Стрижка машинкой',
            'description': 'Быстрая стрижка машинкой под одну длину',
            'price': 800.00,
            'duration': 20,
            'is_popular': False,
        },
        {
            'name': 'Бритье бороды',
            'description': 'Классическое бритье опасной бритвой с распариванием',
            'price': 1200.00,
            'duration': 30,
            'is_popular': True,
        },
        {
            'name': 'Стрижка бороды',
            'description': 'Моделирование и стрижка бороды',
            'price': 900.00,
            'duration': 25,
            'is_popular': True,
        },
        {
            'name': 'Детская стрижка',
            'description': 'Стрижка для мальчиков до 12 лет',
            'price': 1000.00,
            'duration': 30,
            'is_popular': False,
        },
        {
            'name': 'Укладка',
            'description': 'Укладка волос с использованием профессиональных средств',
            'price': 700.00,
            'duration': 15,
            'is_popular': False,
        },
        {
            'name': 'Комплекс (стрижка + борода)',
            'description': 'Комплексная услуга: стрижка волос и оформление бороды',
            'price': 2200.00,
            'duration': 60,
            'is_popular': True,
        },
    ]
    
    services = []
    for service_data in services_data:
        service, created = Service.objects.get_or_create(
            name=service_data['name'],
            defaults=service_data
        )
        services.append(service)
        if created:
            print(f"Создана услуга: {service.name}")
        else:
            print(f"Услуга уже существует: {service.name}")
    
    return services

def create_masters(services):
    """Создание мастеров"""
    masters_data = [
        {
            'name': 'Эльдар "Бритва" Рязанов',
            'phone': '+7 (999) 123-45-67',
            'experience': 8,
            'is_active': True,
        },
        {
            'name': 'Зоя "Ножницы" Космодемьянская',
            'phone': '+7 (999) 234-56-78',
            'experience': 5,
            'is_active': True,
        },
        {
            'name': 'Борис "Фен" Пастернак',
            'phone': '+7 (999) 345-67-89',
            'experience': 12,
            'is_active': True,
        },
        {
            'name': 'Иннокентий "Лак" Смоктуновский',
            'phone': '+7 (999) 456-78-90',
            'experience': 3,
            'is_active': True,
        },
        {
            'name': 'Раиса "Бигуди" Горбачёва',
            'phone': '+7 (999) 567-89-01',
            'experience': 7,
            'is_active': False,
        },
    ]
    
    masters = []
    for master_data in masters_data:
        master, created = Master.objects.get_or_create(
            name=master_data['name'],
            defaults=master_data
        )
        
        # Добавляем случайные услуги мастеру
        master_services = random.sample(list(services), random.randint(3, len(services)))
        master.services.set(master_services)
        
        masters.append(master)
        if created:
            print(f"Создан мастер: {master.name}")
        else:
            print(f"Мастер уже существует: {master.name}")
    
    return masters

def create_orders(masters, services):
    """Создание заказов"""
    statuses = ['new', 'confirmed', 'completed', 'canceled']
    names = ['Иван', 'Петр', 'Алексей', 'Михаил', 'Дмитрий', 'Сергей', 'Андрей', 'Николай']
    surnames = ['Иванов', 'Петров', 'Сидоров', 'Смирнов', 'Кузнецов', 'Попов', 'Васильев', 'Соколов']
    
    for i in range(20):
        # Генерируем случайные данные для заказа
        name = f"{random.choice(names)} {random.choice(surnames)}"
        phone = f"+7 (9{random.randint(10, 99)}) {random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(10, 99)}"
        status = random.choice(statuses)
        master = random.choice(masters) if random.random() > 0.2 else None
        
        # Генерируем случайную дату в пределах последних 30 дней
        days_ago = random.randint(0, 30)
        appointment_date = datetime.now().date() - timedelta(days=days_ago)
        
        # Создаем заказ
        order = Order.objects.create(
            name=name,
            phone=phone,
            comment=f"Тестовый заказ #{i+1}" if random.random() > 0.7 else "",
            status=status,
            master=master,
            appointment_date=appointment_date
        )
        
        # Добавляем случайные услуги к заказу
        order_services = random.sample(list(services), random.randint(1, 3))
        order.services.set(order_services)
        
        print(f"Создан заказ #{order.id}: {name}, статус: {status}")

def create_reviews(masters):
    """Создание отзывов"""
    review_texts = [
        "Отличный мастер! Очень доволен стрижкой.",
        "Всё понравилось, приду ещё раз.",
        "Хорошее обслуживание, но немного дороговато.",
        "Мастер знает своё дело, рекомендую!",
        "Не совсем то, что я ожидал, но в целом неплохо.",
        "Супер! Лучшая стрижка в моей жизни!",
        "Быстро и качественно. Спасибо!",
        "Приятная атмосфера и профессиональный подход.",
        "Мастер учел все мои пожелания, результат отличный.",
        "Немного не понравилось отношение, но работа выполнена хорошо."
    ]
    
    names = ["Клиент", "Посетитель", "Гость", "Александр", "Владимир", "Евгений", "Максим", "Артем"]
    
    for master in masters:
        # Генерируем от 0 до 5 отзывов для каждого мастера
        num_reviews = random.randint(0, 5)
        for i in range(num_reviews):
            name = random.choice(names)
            if random.random() > 0.3:  # 30% отзывов будут анонимными
                name = f"{name} {chr(65 + i)}"  # Добавляем букву для уникальности
            
            Review.objects.create(
                name=name,
                text=random.choice(review_texts),
                rating=random.randint(3, 5),  # В основном положительные отзывы
                master=master
            )
            
            print(f"Создан отзыв для мастера {master.name}")

if __name__ == "__main__":
    print("Начинаем заполнение базы данных...")
    create_superuser()
    services = create_services()
    masters = create_masters(services)
    create_orders(masters, services)
    create_reviews(masters)
    print("База данных успешно заполнена!")