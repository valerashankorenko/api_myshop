from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, ProductViewSet, SubcategoryViewSet

router_v1 = DefaultRouter()
router_v1.register(r'categories', CategoryViewSet)
router_v1.register(r'subcategories', SubcategoryViewSet)
router_v1.register(r'products', ProductViewSet)

urlpatterns = [
    path('', include(router_v1.urls)),
]
