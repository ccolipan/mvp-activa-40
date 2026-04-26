from django.urls import path
from django.contrib.auth import views as auth_views
from .import views

urlpatterns = [
    # Usamos la vista de login nativa de Django, pero le decimos que use nuestro diseño
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    # Vista de logout nativa
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # Ruta de registro
    path('registro/', views.registro_cliente, name='registro'),
    # Ruta para los coach
    path('registro/coach/', views.registro_coach, name='registro_coach'),
]