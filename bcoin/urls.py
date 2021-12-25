from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from bcoin.apps.coins import views
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view

router = routers.DefaultRouter()
router.register(r"wallets", views.WalletViewSet)
router.register(r"coin_transfers", views.CoinTransferViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
    path("transactions/", views.list_transactions),
    path("transactions/<int:transaction_id>", views.view_transaction),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path(
        "openapi",
        get_schema_view(
            title="Your Project", description="API for all things …", version="1.0.0"
        ),
        name="openapi-schema",
    ),
    path(
        "swagger-ui/",
        TemplateView.as_view(
            template_name="swagger-ui.html",
            extra_context={"schema_url": "openapi-schema"},
        ),
        name="swagger-ui",
    ),
]
