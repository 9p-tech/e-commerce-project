from django.contrib import admin
from django.urls import include,path
from . import views
app_name='myapp'
urlpatterns = [
    path('hello/',views.index),
    path("lists/",views.lists,name="lists"),
    path("productid/<int:pk>/",views.ProductDetailView.as_view(),name='product_detail'),
    path("add/",views.ProductCreateView.as_view(),name="add_products"),
    path("update/<int:pk>/",views.ProductUpdateView.as_view(),name="update_products"),
    path("delete/<int:pk>/",views.ProductDeleteView.as_view(),name='delete_products'),
    path("lists/my_listings/",views.my_listings,name="my_listings"),
    path("success/", views.PaymentSuccessView.as_view(), name='success'),
    path("failed/",views.PaymentFailedView.as_view(),name='failed'),
    path("api/checkout-session/<int:id>/",views.create_check_out_session,name='api_checkout_session')

]
