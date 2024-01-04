from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static
from django.urls import path, include
from django.conf import settings
from android.views import (
    AndroidRequestHandlerAPIView,
    fully_fetched_data,
    fetch_criminals,
    generate_token,
    fetch_camera,
)

router = DefaultRouter()
router.register(r"mud", AndroidRequestHandlerAPIView)

urlpatterns = [
    path("api/clients/", fully_fetched_data),
    path("api/criminals/", fetch_criminals),
    path("api/", include(router.urls)),
    path("api/camera/", fetch_camera),
    path("auth/token/", generate_token)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)