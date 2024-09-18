from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from blog.wiews import about_page, HomeView
from users.views import ProfileView

urlpatterns = [
    path("", HomeView.as_view(), name="home_page"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("about/", about_page, name="about_page"),
    path("users/", include("users.urls")),
    path("posts/", include("posts.urls")),
    path("portfolio/", include("portfolio.urls")),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

