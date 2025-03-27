from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Оставляем админку только здесь
    path('', include('myapp.urls')),  # Все остальные маршруты из приложения
]