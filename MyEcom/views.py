from django import views
from django.http import response
from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render,redirect
from django.views import View
from django.db.models import Q
from django.views.generic.base import TemplateResponseMixin

from .models import (
    Confirm,
    Customer,
    Product,
    Cart,
    OrderPlaced
)

from .forms import ConfirmForm, CustomerRegisterationForm,UserProfileForm
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
import random



def home(request):

  

   if request.user.is_authenticated:
      rnd=random.randint(1000, 9999)
            
      otp=request.session['otp']=rnd
      
      if request.method=="POST":
         fm=ConfirmForm(request.POST)
         if fm.is_valid():
            otp=fm.cleaned_data['otp']
            usr=Confirm.objects.filter(user=request.user).order_by('-id')[0]
            print(usr)
            print(usr.otp)
            print(usr.id)
            if usr.otp==otp:
               messages.success(request,f"Welcome Mr {usr.user}")
               return HttpResponseRedirect('/')
            else:
               messages.warning(request,"Plz Enter Valid Pin")
               fm=ConfirmForm()
               return render(request, 'app/email.html',{'form':fm})           
         
      else:
            
            Confirm(user=request.user,otp=otp).save()
            subject = 'Welcome to DJANGO MAIL world'
            message = f'Hi {request.user}, thank you for choosing us here is your OTP PIN {otp}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [ 'abc@gmail.com']
            send_mail( subject, message, email_from, recipient_list )
            
            
            fm=ConfirmForm()
            messages.success(request,"An OTP has been sent to your email address")
               
            return render(request, 'app/email.html',{'form':fm})   

   else:
      return HttpResponseRedirect('/login')      




class ProductView(View):
    def get(self,request):
        watches=Product.objects.filter(category='W')
        mobiles=Product.objects.filter(category='M')
        creams=Product.objects.filter(category='C')
        electronics=Product.objects.filter(category='E')
        return render (request,'app/home.html',{'watches':watches,'creams':creams,'electronics':electronics,'mobiles':mobiles})


# def product_detail(request):
#  return render(request, 'app/productdetail.html')

class ProductDetailView(View):
    def get(self,request,pk):
        product =Product.objects.get(pk=pk)
        product_present=False
        product_present=Cart.objects.filter(Q(product=product.id)&Q(user=request.user)).exists()
       
      
        return render (request,'app/productdetail.html',{'product':product,'product_present':product_present})




def show_cart(request):
     usr=request.user
     product=Cart.objects.filter(user=usr)
     amount=0.0
     shipping_amount=70
     total_amount=0.0
#To receive products as a list from cart placed by logged in user
# as user is unique due to django auth
    
     cart_product=[p for p in Cart.objects.all() if p.user==request.user]
     
     for p in cart_product:
        tempamount=(p.quantity*p.product.selling_price)
        
        amount+=tempamount
        total_amount=amount+shipping_amount   
     return render (request,'app/cart.html',{'product':product,'total':total_amount,'amount':amount})



def plus_cart(request):
   
      product_id=request.GET.get('product_id')
      c = Cart.objects.get(Q(product=product_id) & Q(user=request.user))
      c.quantity+=1
      c.save()
      usr=request.user
      amount=0.0
      shipping_amount=70
      total_amount=0.0
#To receive products as a list from cart placed by logged in user
# as user is unique due to django auth
    
      cart_product=[p for p in Cart.objects.all() if p.user==request.user]
         
      for p in cart_product:
         tempamount=(p.quantity*p.product.selling_price)
        
         amount+=tempamount
         total_amount=amount+shipping_amount   
    
      data={
         'quantity':c.quantity,
         'amount':amount,
         'total':total_amount
      }
      return JsonResponse(data)



def minus_cart(request):
   
      product_id=request.GET.get('product_id')
      c = Cart.objects.get(Q(product=product_id) & Q(user=request.user))
      c.quantity-=1
      if c.quantity==0:
         c.delete()
      else:
        c.save()
      usr=request.user
      amount=0.0
      shipping_amount=70
      total_amount=0.0
#To receive products as a list from cart placed by logged in user
# as user is unique due to django auth
    
      cart_product=[p for p in Cart.objects.all() if p.user==request.user]
         
      for p in cart_product:
         tempamount=(p.quantity*p.product.selling_price)
        
         amount+=tempamount
         total_amount=amount+shipping_amount   
    
      data={
         'quantity':c.quantity,
         'amount':amount,
         'total':total_amount
      }
      return JsonResponse(data)


def remove_cart(request):
   
      product_id=request.GET.get('product_id')
      c = Cart.objects.get(Q(product=product_id) & Q(user=request.user))
      
      c.delete()
      usr=request.user
      amount=0.0
      shipping_amount=70
      total_amount=0.0
#To receive products as a list from cart placed by logged in user
# as user is unique due to django auth
    
      cart_product=[p for p in Cart.objects.all() if p.user==request.user]
         
      for p in cart_product:
         tempamount=(p.quantity*p.product.selling_price)
        
         amount+=tempamount
         total_amount=amount+shipping_amount   
    
      data={
         'quantity':c.quantity,
         'amount':amount,
         'total':total_amount
      }
      return JsonResponse(data)

    





# @login_required(login_url='/accounts/login/')
#can be used  login url provide alternative to settings.LOGIn_URL
# and redirect_field_name
#IT REDIRECTS THE NONE AUTHENTICATED USER TO GIVEN URL
class AddToCartView(View):

   def get(self,request):
         pk=request.GET.get('product_id')
         prd=Product.objects.get(pk=pk)
         crt=Cart(user=request.user,product=prd)
         crt.save()
      
         return redirect('/cart')






def buy_now(request):
 return render(request, 'app/buynow.html')









# def profile(request):

#  return render(request, 'app/profile.html')


class ProfileView(View):
    def get(self,request):
       form=UserProfileForm()
       return render(request,'app/profile.html',{'form':form,'active1':'btn-primary'})
    
    def post(self,request):
            
            form=UserProfileForm(request.POST)
            if form.is_valid():
               usr=request.user
               name=form.cleaned_data['name']
               address=form.cleaned_data['address']
               city=form.cleaned_data['city']
               zip=form.cleaned_data['zip']
               state=form.cleaned_data['state']
               reg=Customer(user=usr,name=name,address=address,city=city,zip=zip,state=state)
               reg.save()
            
           
           
            else:
              return render(request,'app/profile.html',{'form':form,'active2':'btn-primary'})
            form=UserProfileForm()
            
            return render(request,'app/profile.html',{'form':form,'active2':'btn-primary'})
        
            

#def address(request):
#  return render(request, 'app/address.html')           
        
class AddressView(View):
    def get(self,request):
       data=Customer.objects.filter(user=request.user)
       return render(request,'app/address.html',{'data':data,'active':'btn-primary'})















def orders(request):

 return render(request, 'app/orders.html')





#data=None id default value for path conerter

def mobiles(request,data=None):
 if data==None:
    product =Product.objects.filter(category='M')
 elif data=='below':
    product =Product.objects.filter(category='M').filter(selling_price__lte=6000)
 elif data=='above':
    product =Product.objects.filter(category='M').filter(selling_price__gte=6000)
 return render(request, 'app/mobiles.html',{'mobiles':product})


def watches(request,data=None):
 
 if data==None:
    product =Product.objects.filter(category='W')
 elif data=='below':
    product =Product.objects.filter(category='W').filter(selling_price__lte=760)
 elif data=='above':
    product =Product.objects.filter(category='W').filter(selling_price__gte=760)
 return render(request, 'app/watches.html',{'watches':product})


def cosmetics(request,data=None):
     if data==None:
          product =Product.objects.filter(category='C')
     elif data=='below':
          product =Product.objects.filter(category='C').filter(selling_price__lte=4700)
     elif data=='above':
          product =Product.objects.filter(category='C').filter(selling_price__gte=4700)
     return render(request, 'app/cosmetics.html',{'cosmetics':product})








def login(request):
 return render(request, 'app/login.html')

# def customerregistration(request):
#  return render(request, 'app/customerregistration.html')



class CustomerRegistrationView(View):
   def get(self,request):
      fm=CustomerRegisterationForm()
      return render(request, 'app/customerregistration.html',{'fm':fm})

   def post(self,request):
       fm=CustomerRegisterationForm(request.POST)
       if fm.is_valid():
          fm.save()
          messages.success(request,"Congratulatios Your Registeration is Successfull!!")
       return HttpResponseRedirect('/login')


class CheckoutView(View):

   def get(self,request):
      usr=request.user
      ordp=Cart.objects.filter(user=usr)
      cust=Customer.objects.filter(user=request.user)
      return render(request, 'app/checkout.html',{'customer':cust,'orders':ordp,})
   def post(self,request):
       usr=request.user

       id=request.POST['flexRadioDefault']
       customer=Customer.objects.get(id=id)
       c = Cart.objects.filter(user=request.user)
       
       for cart in c:
         id=cart.product.id
         print(id)
         #Using filter will return a query set which won't be 
         #assignable to ORderPlaced
         #LOOOK FOR DIFFERNECE BETWEEN RETURN OF FILTER AND GET
         p=Product.objects.get(id=id)
         print(p.id)
         order=OrderPlaced(user=usr,customer=customer,product=p,quantity=cart.quantity).save()
         cart.delete()
      
       return HttpResponseRedirect('/orders')
      
def orders(request):
   order=OrderPlaced.objects.filter(user=request.user)
   return render(request,'app/orders.html',{'order':order}) 
       
