from django.contrib import admin
from django.urls import path, include

# the 2 following lines are for uploading images (media)

from django.conf import settings

from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('journal.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) #the static function is used to create url for the media file