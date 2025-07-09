from django.contrib import admin
from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path, include, reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('quote.urls', namespace='quote')),
    path('auth/logout/',
         LogoutView.as_view(
             template_name='registration/logged_out.html',
         ),
         name='logout'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path(
        'auth/registration/',
        CreateView.as_view(
            template_name='registration/registration_form.html',
            form_class=UserCreationForm,
            success_url=reverse_lazy('quote:top-quotes'),
        ),
        name='registration',
    ),
]
