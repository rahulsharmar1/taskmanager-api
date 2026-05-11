"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)


urlpatterns = [
    # Admin site
    path('admin/', admin.site.urls),
    
    # ── Authentication ────────────────────────────────────────────────────────
    # POST with {username, password} → returns {access, refresh} tokens
    path("api/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    # POST with {refresh} → returns new {access} token
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # ── Task Endpoints ────────────────────────────────────────────────────────
    path("api/", include("apps.tasks.urls")),

    # ── API Documentation ─────────────────────────────────────────────────────
    # /api/schema/           → raw OpenAPI 3.0 schema (JSON/YAML) — used by tools
    # /api/schema/swagger-ui/ → interactive Swagger UI — for human exploration
    # /api/schema/redoc/     → clean ReDoc UI — for sharing with clients/teams
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]
