from django.contrib.auth.forms import PasswordChangeForm
from django.urls import path
from MyEcom  import views
from .forms import LoginForm, RestPassword,SetPassword
from django.conf import settings
from django.conf.urls.static import static 
from django.contrib.auth import authenticate, views as auth_view

urlpatterns = [

    
    path('home/', views.home,name="email"),
    path('',views.ProductView.as_view(),name="home"),
    path('product-detail/<int:pk>',views.ProductDetailView.as_view(), name='product-detail'),
    path('add-to-cart/', views.AddToCartView.as_view(), name='add-to-cart'),
    path('buy/', views.buy_now, name='buy-now'),
    path('cart/', views.show_cart, name='show_cart'),
    path('pluscart/', views.plus_cart, name='plus_cart'),
    path('minuscart/', views.minus_cart, name='minus_cart'),
    path('removecart/', views.remove_cart, name='remove_cart'),




    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.AddressView.as_view(), name='address'),
    path('orders/', views.orders, name='orders'),
    path('mobiles/', views.mobiles, name='mobiles'),
    path('mobiles/<slug:data>', views.mobiles, name='mobiledata'),
   
    path('watches/', views.watches, name='watches'),
    path('watches/<slug:data>', views.watches, name='watchdata'),
     
    
    
    path('cosmetics/', views.cosmetics, name='cosmetics'),
    path('cosmetics/<slug:data>', views.cosmetics, name='cosmeticdata'),
    
    
    path('login/', auth_view.LoginView.as_view(template_name="app/login.html",authentication_form=LoginForm),name="login"),
    path('logout/', auth_view.LogoutView.as_view(),name="logout"),

    path('passwordchangedone/',auth_view.PasswordChangeDoneView.as_view(template_name="app/passwordchangedone.html"),name="passwordchangedone"),
    path('change/', auth_view.PasswordChangeView.as_view(template_name="app/changepassword.html",form_class=RestPassword,success_url="/passwordchangeddone/"),name="changepassword"),
    
    path('setpassword/', auth_view.PasswordResetConfirmView.as_view(template_name="app/setpassword.html",form_class=SetPassword,success_url="/passwordchangeddone/"),name="setpassword"),
    


    path('registeration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

#TO INCLUDE URL OF MEDIA FILES UPLOADED ON DATABASE