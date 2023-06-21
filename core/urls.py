from django.urls import path
from django.conf.urls.static import static
from .views import home, DownloadMedia, clean_media
from django.conf import settings

app_name = 'core'

urlpatterns = [
    path('', home, name='home'),
    path('download/', DownloadMedia, name='file_download'),
    path('clean/', clean_media, name='file_download'),
    

]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)