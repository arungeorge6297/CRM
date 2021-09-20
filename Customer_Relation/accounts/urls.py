
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import  *

urlpatterns = [

    path('register/',registerPage, name="register"),
    path('login/',loginPage, name="login"),
    path('logout/',logoutUser,name="logout"),



    path('', home,name="home"),
    path('products/',product,name="products"),
    path('customer/<int:customer_id>/',customer, name="customer"),

    path('user/',userPage,name="user-page"),

    path('account/',accountSettings,name="account"),

    path('create_order/<int:customer_id>/', createOrder, name="create_order"),
    path('update_order/<int:order_id>/',updateOrder,name="update"),
    path('delete_order/<int:delete_id>/',deleteOrder,name="delete"),

    path('reset_password/',auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),
    name="reset_password"),

    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"),
    name="password_reset_done"),

    path('reset/<uid64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"),
    name="password_reset_confirm"),

    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"),
     name="password_reset_complete"),
]