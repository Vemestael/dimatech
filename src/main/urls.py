from rest_framework import routers

from main import views

router = routers.DefaultRouter()
router.register(r'product', views.ProductAPI)
router.register(r'customer-bill', views.CustomerBillAPI)
router.register(r'transaction', views.TransactionAPI)

urlpatterns = router.urls
