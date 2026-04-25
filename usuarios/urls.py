from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Usamos la vista de login nativa de Django, pero le decimos que use nuestro diseño
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    # Vista de logout nativa
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]