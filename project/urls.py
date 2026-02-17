# File: mini_insta/urls.py
# Author: Song Yu Chen (songyu@bu.edu) 11/23/2025
# Description: URL page for the project app. 
from django.urls import path
from django.conf import settings
from . import views
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    # stores urls for different views

    # views without login requirement
    path('show_accounts', AccountListView.as_view(), name="show_accounts"),
    path('show_account/<int:pk>', AccountDetailView.as_view(), name="show_account"),
    
    path('', ProductListView.as_view(), name="show_products"),
    path('product/<int:pk>/', ProductDetailView.as_view(), name="show_product"),
    
    ### prodcut creation , update, delete
    path('create_product', CreateProductView.as_view(), name="create_product"),
    path('product/<int:pk>/update/', UpdateProductView.as_view(), name="update_product"),
    path('product/<int:pk>/delete/', DeleteProductView.as_view(), name="delete_product"),
    
    ### account views
    path('my_account', MyAccountDetailView.as_view(), name='my_account'),
    path('my_products', MyProductsListView.as_view(), name='my_products'),
    path('my_favorites', MyFavoritesListView.as_view(), name='my_favorites'),
    path('my_bids', MyBidsListView.as_view(), name='my_bids'),
    path('my_orders/', MyOrdersListView.as_view(), name='my_orders'),

    
    ### favorite and unfavorite
    path('product/<int:pk>/favorite/add/', CreateFavoriteView.as_view(), name="create_favorite"),
    path('product/<int:pk>/favorite/remove/', DeleteFavoriteView.as_view(), name="delete_favorite"),

    ### create bids and accept bids
    path('product/<int:pk>/bid/', CreateBidView.as_view(), name="create_bid"),
    path('bid/<int:pk>/accept/', AcceptBidView.as_view(), name="accept_bid"),
    
    ### checkout and rating
    path("checkout/", CheckoutAcceptedBidsView.as_view(), name="checkout"),
    path("stripe/create-checkout-session/", CreateCheckoutSessionView.as_view(), name="stripe_create_session"),
    path("stripe/success/", StripeSuccessView.as_view(), name="stripe_success"),
    path("stripe/cancel/", StripeCancelView.as_view(), name="stripe_cancel"),
    path("stripe/webhook/", StripeWebhookView.as_view(), name="stripe_webhook"),

    path("product/<int:pk>/rate/", RateProductView.as_view(), name="rate_product"),


    
    ### account creation, login, logout
    path('create_account', CreateAccountView.as_view(), name='create_account'),
    path('update_account', UpdateAccountView.as_view(), name="update_account"),
    path('delete_account', DeleteAccountView.as_view(), name="delete_account"),

    path('login/', auth_views.LoginView.as_view(template_name='project/login.html'), name="login"),
    path('logout/', auth_views.LogoutView.as_view(next_page='logout_confirmation'), name="logout"),
    path('logout_confirmation/', LogoutConfirmationView.as_view(), name='logout_confirmation'),
    
]