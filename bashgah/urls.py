from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('apps.main.urls',namespace='main')),
    path('accounting/', include('django.contrib.auth.urls')),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.site_header='باشگاه ولیعصر (عج)'
admin.site.index_title='به پنل مدیریت باشگاه ولیعصر خوش آمدید'

