from django.contrib import admin
from django.urls import include, path
from django.contrib.auth.views import LoginView, LogoutView
from mysite.views import main, tables, SignUp

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tables/', include('tables.urls')),
    path('reservations/', include('reservations.urls')),
    
    # Autenticación
    path('', LoginView.as_view(
        template_name='login.html',
        redirect_authenticated_user=True  # Nueva característica importante
    ), name="login"),
    
    path('signup/', SignUp.as_view(
        template_name='signup.html'
    ), name="signup"),
    
    path('main/', main, name="main"),
    path('logout/', LogoutView.as_view(
        next_page='login'  # Redirige al login después de logout
    ), name="logout")
]