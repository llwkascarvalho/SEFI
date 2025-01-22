from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('fila/', include('fila.urls')),
    path('historico/', include('historico.urls')),
    path('nova_solicitacao/', include('solicitacao.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('accounts/', include('django.contrib.auth.urls')),
]

# accounts/login sobrecarregado para usar o template personalizado