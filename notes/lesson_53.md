# Тема Django. Наследование шаблонов. Include. Контекстный процессор. Урок 53

## Что такое наследование шаблонов в Django? 🤔

# TODO Сделать из этих пунктов заголовки 3 уровня

- Пояснение что такое
- Пояснение что есть `{% block %}`  а так же `include`
- Пояснение что есть `{% extends %}`
- Рассказ про то что блоки можно переопределить, расширить или дать им значение по умолчанию

![templates_extends_schema.png](./images/templates_extends_schema.png)

## Простой пример наследования шаблонов в Django 📝

`base.html`

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>
        {% block title %}
        "Барбершоп "Арбуз"
        {% endblock title %}
    </title>
</head>
<body>
    {% block content %}{% endblock content %}
</body>
</html>
```

`thanks.html`

```html
{% extends "base.html" %}
{% block content %}
    <h1>Спасибо за заявку!</h1>
    <p>Мы свяжемся с вами в ближайшее время!</p>
{% endblock content %}
```

Пример на скриншоте
![first_template_exends.png](./images/first_template_exends.png)

## Простой пример `include` в Django 📝

Тег шаблона `include` позволяет включать в шаблон другой шаблон. И делает это немного по-другому, чем `extends`.

Причем мы можем включить шаблон в блок шаблона, чтобы была возможность выключить отображение блока на той или иной странице.

Как например тут:

`include_nav_menu.html`

```html
{% comment %} nav>ul>li*5>a {% endcomment %}
<nav>
    <ul>
        <li><a href="">Текст ссылки</a></li>
        <li><a href="">Текст ссылки</a></li>
        <li><a href="">Текст ссылки</a></li>
        <li><a href="">Текст ссылки</a></li>
        <li><a href="">Текст ссылки</a></li>
    </ul>
</nav>
```

`base.html`

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>
        {% block title %}
        "Барбершоп "Арбуз"
        {% endblock title %}
    </title>
</head>
<body>
    <header>
        {% block header %}
        {% include "include_nav_menu.html" %}
        {% endblock header %}
    </header>
    <main>
        {% block content %}{% endblock content %}
    </main>
    <footer>

    </footer>
    
</body>
</html>
```

- Пояснение как это работает
- Что ссылки меню и текст ссылок мы можем передавать через контекст вью
- Что мы можем выключить отображение навигационного меню определив блок в наследуемом шаблоне
