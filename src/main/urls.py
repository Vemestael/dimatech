from django.urls import include, path
from rest_framework import routers

from main import views

router = routers.DefaultRouter()
router.register(r'product', views.ProductAPI)
router.register(r'customer-bill', views.CustomerBillAPI, basename='customerbillmodel')
router.register(r'transaction', views.TransactionAPI, basename='transactionmodel')
router.register(r'purchase', views.PurchaseAPI, basename='purchasemodel')
router.register(r'auth/users', views.UserViewSet)

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('auth/', include('djoser.urls.jwt')),
    path('auth/activate/<str:uid>/<str:token>/', views.UserActivationView.as_view()),
    path('payment/webhook', views.transaction_webhook)
]
urlpatterns += router.urls
