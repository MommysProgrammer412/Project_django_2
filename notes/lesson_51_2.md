# Тема Django. MTV. Знакомство с Шаблонизатором и маршрутизацией. Урок 51 Ч2 - Шаблоны 🏗️

Шаблонизатор Django - это мощный инструмент для генерации HTML на сервере. Он позволяет отделить логику представления от визуального оформления, следуя принципам MTV (Model-Template-View).

## Знакомство с шаблонизатором Django 🧩

Шаблонизатор Django решает ключевую проблему смешивания Python-кода и HTML в одном файле. Вместо этого он предоставляет:

- Специальный синтаксис для вставки динамических данных
- Наследование шаблонов для повторного использования кода
- Фильтры для преобразования данных прямо в шаблоне

>[!info]
>
>#### Основные возможности шаблонизатора 🔍
>
>- Переменные: `{{ variable }}`
>- Теги: `{% tag %}`
>- Фильтры: `{{ value|filter }}`
>- Наследование: `{% extends "base.html" %}`

Шаблонизатор автоматически экранирует HTML, предотвращая XSS-атаки, но позволяет явно указать, когда содержимое безопасно с помощью фильтра `safe`.

## Места хранения шаблонов 📂

Django предоставляет гибкую систему расположения шаблонов, позволяющую организовать их наиболее удобным способом.

### Стандартные варианты и лучшие практики 🏆

По умолчанию Django ищет шаблоны в папке `templates` каждого установленного приложения, рекурсивно обходя их. Это позволяет каждому приложению иметь собственные шаблоны.

```python
# Пример структуры для приложения core
core/
    templates/
        core/
            thanks.html
```

В представлении такой шаблон будет указываться как `core/thanks.html`:

```python
def thanks(request):
    return render(request, "core/thanks.html")
```

>[!warning]
>
>#### Почему сложная структура? ⚠️
>
>Использование подпапки с именем приложения внутри `templates` предотвращает конфликты имен, когда несколько приложений имеют шаблоны с одинаковыми именами.

### Альтернативное место хранения 🗄️

Для небольших проектов можно хранить все шаблоны в корневой папке `templates`. Для этого нужно изменить настройки:

```python
# settings.py
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Добавляем корневую папку templates
        'APP_DIRS': True,
    }
]
```

`BASE_DIR` - это путь к корню проекта, а `BASE_DIR / 'templates'` создает полный путь к папке шаблонов. Например:

```python
BASE_DIR = Path(__file__).resolve().parent.parent
# Результат: C:\PY\ПРИМЕРЫ КОДА\django_consult_413
```

## Установка плагина Django для VS Code ⚙️

Для удобной работы с шаблонами Django в VS Code рекомендуется установить специальное расширение.

![django_plugin.png](./images/django_plugin.png)

Расширение Django от Baptiste Darthenay добавляет:

- Подсветку синтаксиса для `*.html` и `*.djhtml`
- Автодополнение тегов и фильтров Django
- Улучшенную навигацию по проекту

### Настройка расширения 🛠️

После установки рекомендуется добавить в настройки VS Code:

```json
 // === НАСТРОЙКИ DJANGO И WEB-РАЗРАБОТКИ ===
  "emmet.includeLanguages": {
    "django-html": "html"
  },
  "emmet.triggerExpansionOnTab": true,
  "emmet.showSuggestionsAsSnippets": true,
  "emmet.showExpandedAbbreviation": "always",
  "emmet.useInlineCompletions": true,
  "emmet.extensionsPath": [],
  "emmet.syntaxProfiles": {
    "html": {
      "filters.commentAfter": "<!-- /{[#]}/ -->",
      "attributes": {
        "class": "class",
        "id": "id",
        "for": "for"
      }
    },
    "django-html": {
      "filters.commentAfter": "{# /{[#]}/ #}"
    }
  },
  "files.associations": {
    "**/*.html": "html",
    "**/templates/*/*.html": "django-html",
    "**/templates/*/*/*.html": "django-html",
    "**/templates/*": "django-html",
    "**/requirements{/**,*}.{txt,in}": "pip-requirements"
  },
  "[django-html]": {
    "breadcrumbs.showClasses": true,
    "editor.formatOnSave": false,
    "editor.quickSuggestions": {
      "other": true,
      "comments": true,
      "strings": true
    }
  },
```

А так же

````json
  "python.analysis.packageIndexDepths": [
    {
      "name": "django",
      "depth": 10,
      "includeAllSymbols": true
    },
    {
      "name": "selenium",
      "depth": 3,
      "includeAllSymbols": true
    },
    {
      "name": "sqlalchemy",
      "depth": 3,
      "includeAllSymbols": true
    },
    {
      "name": "sqlite3",
      "depth": 3,
      "includeAllSymbols": true
    }
  ],
```

Эти настройки отключают автоформатирование (которое может сломать шаблоны) и включают подсказки во всех контекстах.

## Первый шаблон Django 🎯

Создадим простой шаблон `thanks.html` в корневой папке `templates`:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Спасибо!</title>
</head>
<body>
    <h1>Спасибо за ваш заказ!</h1>
</body>
</html>
```

Для его отображения используем функцию `render`:

```python
def thanks(request):
    return render(request, "thanks.html")
```

Функция `render` принимает два обязательных аргумента:

1. Объект запроса (`request`)
2. Путь к шаблону относительно папки `templates`

>[!info]
>
>#### Рендеринг на сервере vs клиенте 🔄
>
>Django выполняет рендеринг шаблонов на сервере, отправляя клиенту уже готовый HTML. Это отличается от современных JavaScript-фреймворков, где рендеринг часто происходит на стороне клиента.
