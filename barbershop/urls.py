from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls
from core.views import LandingView, ThanksView, OrdersListView, OrderDetailView, ReviewCreateView, OrderCreateView, ServicesListView, OrderUpdateView

urlpatterns = [
    path('', LandingView.as_view(), name='landing'),
    path('thanks/', ThanksView.as_view(), name='thanks'),
    path('orders/', OrdersListView.as_view(), name='orders'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('orders/<int:order_id>/update/', OrderUpdateView.as_view(), name='order-update'),
    path('reviews/create/', ReviewCreateView.as_view(), name='create_review'),
    path('orders/create/', OrderCreateView.as_view(), name='order-create'),
    path('services/', ServicesListView.as_view(), name='services-list'),
    path('users/', include('users.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0]
    )

urlpatterns += debug_toolbar_urls()