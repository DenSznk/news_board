
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from news_board.views import IndexView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('users.urls')),
    path('blog/', include('news_board.urls')),
    path('', IndexView.as_view(), name='index'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)