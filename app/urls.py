from app import settings
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static  # <-- ADICIONAR ISSO

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('educa_sorriso.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='educa_sorriso/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='educa_sorriso:home'), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
