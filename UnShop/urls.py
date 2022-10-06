from django.contrib import admin
from django.urls import path, include
from api.routers import router
from main.views import Login, Logout

urlpatterns = [
    path('', include('main.urls')),
    path('login/', Login, name='login'),
    path('logout/', Logout, name='logout'),
    path('ipa/', include(router.urls)),
    path('admin/', admin.site.urls),
]
