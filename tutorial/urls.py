from django.contrib import admin
from django.templatetags import static
from django.urls import include, path
from rest_framework import routers

from tutorial import settings
from tutorial.quickstart import views
from .quickstart.views import CustomAuthToken, RegisterView, me, LogoutView, ResetTokenView, CardViewSet

from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register(r"users", views.UserViewSet)
router.register(r"groups", views.GroupViewSet)
router.register(r"cards", CardViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
    path("", include("tutorial.quickstart.urls")),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("api-token-auth/", CustomAuthToken.as_view(), name="api_token_auth"),
    path("api-register/", views.RegisterView.as_view(), name="api_register"),
    path('me/', me, name='me'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('reset-token/', views.ResetTokenView.as_view(), name='reset_token'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)