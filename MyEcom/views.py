from django import views
from django.http import response
from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render,redirect
from django.utils.translation import templatize
from django.views import View
from django.db.models import Q
from django.views.generic.base import TemplateResponseMixin

from .models import*

from .forms import ConfirmForm, CustomerRegisterationForm, LoginForm,UserProfileForm
from django.contrib import messages
from django.contrib.auth import login,authenticate
from django.contrib.auth.views import LoginView
from django.conf import settings
from django.core.mail import send_mail
import random

import razorpay

from django.shortcuts import render

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest


# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
	auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


def homepage(request):
	
   currency = 'INR'
   payment=OrderPlaced.objects.filter(user=request.user)
   cost=0
   for pay in payment:
      cost+=pay.total_cost
   amount_original=cost
   amount_in_paisa = cost*100 # converting in paise 
   
	#Create a Razorpay Order
   razorpay_order = razorpay_client.order.create(dict(amount=amount_in_paisa,
													currency=currency))
   # order id of newly created order.
   razorpay_order_id = razorpay_order['id']
   callback_url = 'proceed/'

	# we need to pass these details to frontend.
   context = {}
   context['razorpay_order_id'] = razorpay_order_id
   context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
   context['currency'] = currency
   context['callback_url'] = callback_url
   context['razorpay_amount']=amount_original
   return render(request, 'app/payment.html', context=context)


# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def paymenthandler(request):

	# only accept POST request.
	if request.method == "POST":
		try:
		
			# get the required parameters from post request.
			payment_id = request.POST.get('razorpay_payment_id', '')
			razorpay_order_id = request.POST.get('razorpay_order_id', '')
			signature = request.POST.get('razorpay_signature', '')
			params_dict = {
				'razorpay_order_id': razorpay_order_id,
				'razorpay_payment_id': payment_id,
				'razorpay_signature': signature
			}

			# verify the payment signature.
			result = razorpay_client.utility.verify_payment_signature(
				params_dict)
			if result is None:
            
				amount = '' # Amount charged
				try:

					# capture the payemt
					razorpay_client.payment.capture(payment_id, amount)

					# render success page on successful caputure of payment
					return render(request, 'app/paymentsuccess.html',context={'context':"Congratulations your payment is successful"})
				except:

					# if there is an error while capturing payment.
					return render(request, 'app/paymentfail.html',context={'context':"there is an error while capturing payment"})
			else:

				# if signature verification fails.
				return render(request, 'app/paymentfail.html')
		except:

			#required parameters not found in POST data
			return HttpResponseBadRequest("we don't find the required parameters in POST data")
	else:
	# if other than POST request is made.
		return HttpResponseBadRequest("other than POST request is made")



class ProductView(View):
    def get(self,request):
        request.session['key']='arrived'
        watches=Product.objects.filter(category='W')
        mobiles=Product.objects.filter(category='M')
        creams=Product.objects.filter(category='C')
        electronics=Product.objects.filter(category='E')
        return render (request,'app/home.html',{'watches':watches,'creams':creams,'electronics':electronics,'mobiles':mobiles})


# def product_detail(request):
#  return render(request, 'app/productdetail.html')

class ProductDetailView(View):
    def get(self,request,pk):
        
        product_present=False
        
        if request.user.is_anonymous:     
         
           product=Product.objects.get(pk=pk)
           product_present=TempCart.objects.filter(Q(product=product.id)&Q(user=request.COOKIES['sessionid'])).exists()
       
           return render (request,'app/productdetail.html',{'product':product,'product_present':product_present})
      
        #for authenticated user
        product=Product.objects.get(pk=pk)
        product_present=Cart.objects.filter(Q(product=product.id)&Q(user=request.user)).exists()
       
      
        return render (request,'app/productdetail.html',{'product':product,'product_present':product_present})




def show_cart(request):
     
     if request.user.is_anonymous:
        product=TempCart.objects.filter(user=request.COOKIES['sessionid'])
        cart_product=[p for p in TempCart.objects.all() if p.user==request.COOKIES['sessionid']]
         
     else:
      usr=request.user
      product=Cart.objects.filter(user=usr)
      cart_product=[p for p in Cart.objects.all() if p.user==request.user]
      
     amount=0.0
     shipping_amount=70
     total_amount=0.0
   #To receive products as a list from cart placed by logged in user
   # as user is unique due to django auth
      
     for p in cart_product:
         tempamount=(p.quantity*p.product.selling_price)
         
         amount+=tempamount
         total_amount=amount+shipping_amount   
     print(product)
     print("#####################")
     return render (request,'app/cart.html',{'product':product,'total':total_amount,'amount':amount})



def plus_cart(request):
   
      product_id=request.GET.get('product_id')
      if request.user.is_authenticated:
         usr=request.user
         c = Cart.objects.get(Q(product=product_id) & Q(user=request.user))

         c.quantity+=1
         c.save()


         amount=0.0
         shipping_amount=70
         total_amount=0.0
#To receive products as a list from cart placed by logged in user
#as user is unique due to django auth
         cart_product=[p for p in Cart.objects.all() if p.user==request.user]

         for p in cart_product:
          tempamount=(p.quantity*p.product.selling_price)
        
          amount+=tempamount
          print(f"########{amount}#############")
          total_amount=amount+shipping_amount   


      else:
        c = TempCart.objects.get(Q(product=product_id) & Q(user=request.COOKIES['sessionid']))  
        usr=request.COOKIES['sessionid']
        
        c.quantity+=1
        c.save()


        amount=0.0
        shipping_amount=70
        total_amount=0.0
#To receive products as a list from cart placed by logged in user
# as user is unique due to django auth
        cart_product=[p for p in TempCart.objects.all() if p.user==request.COOKIES['sessionid']]   
     
        for p in cart_product:
         tempamount=(p.quantity*p.product.selling_price)
        
         amount+=tempamount
         print(f"########{amount}#############")
         total_amount=amount+shipping_amount   
    


      data={
         'quantity':c.quantity,
         'amount':amount,
         'total':total_amount
      }
      return JsonResponse(data)



def minus_cart(request):
   
      product_id=request.GET.get('product_id')
      if request.user.is_authenticated:
         usr=request.user
         c = Cart.objects.get(Q(product=product_id) & Q(user=request.user))
         c.quantity-=1
         if c.quantity==0:
            c.delete()
         else:
          c.save()
         
         amount=0.0
         shipping_amount=70
         total_amount=0.0
   #To receive products as a list from cart placed by logged in user
   # as user is unique due to django auth

         cart_product=[p for p in Cart.objects.all() if p.user==request.user]
         cart_product=[p for p in TempCart.objects.all() if p.user==request.COOKIES['sessionid']]   
            
         for p in cart_product:
            tempamount=(p.quantity*p.product.selling_price)
         
            amount+=tempamount
            total_amount=amount+shipping_amount  

      else:
         c = TempCart.objects.get(Q(product=product_id) & Q(user=request.COOKIES['sessionid']))  

        
         c.quantity-=1
         if c.quantity==0:
            c.delete()
         else:
          c.save()
         
         amount=0.0
         shipping_amount=70
         total_amount=0.0
   #To receive products as a list from cart placed by logged in user
   # as user is unique due to django auth
      
   
         cart_product=[p for p in TempCart.objects.all() if p.user==request.COOKIES['sessionid']]   
            
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
      if request.user.is_authenticated:
         usr=request.user
         c = Cart.objects.get(Q(product=product_id) & Q(user=request.user))
         c.delete()

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
      else:
        c = TempCart.objects.get(Q(product=product_id) & Q(user=request.COOKIES['sessionid']))  
        print("##########{c}###########")
        usr=request.COOKIES['sessionid']
          
      
        c.delete()

        amount=0.0
        shipping_amount=70
        total_amount=0.0

        cart_product=[p for p in TempCart.objects.all() if p.user==request.COOKIES['sessionid']] 
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
         if request.user.is_anonymous :   
  
          
            
            
            prd=Product.objects.get(pk=pk)
            crt=TempCart(user=request.COOKIES['sessionid'],product=prd)
            crt.save()
            return redirect('/cart')

         
         prd=Product.objects.get(pk=pk)
         crt=Cart(user=request.user,product=prd)
         crt.save()
      
         return redirect('/cart')






def buy_now(request):
 return render(request, 'app/buynow.html')




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
        
            

    
        
class AddressView(View):
    def get(self,request):
       data=Customer.objects.filter(user=request.user)
       return render(request,'app/address.html',{'data':data,'active':'btn-primary'})


def orders(request):

 return render(request, 'app/orders.html')






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








class LoginView(View):
   
   def get(self,request):
       fm=LoginForm()
       return render(request,'app/login.html',{'fm':fm})
   
   def post(self,request):
      
      fm=LoginForm(data=request.POST) 
      if fm.is_valid():
            user = authenticate(request, username=fm.cleaned_data['username'],password=fm.cleaned_data['password'])
          
            if request.COOKIES['anonym']:
               if user is not None:  
                 Transfer_cart=TempCart.objects.filter(user=request.COOKIES['sessionid'])
                 login(request,user)
                 for p in Transfer_cart:
                   id=p.product.id
                   prd=Product.objects.get(id=id)
                   Cart(user=request.user,product=prd,quantity=p.quantity).save()    
                 
                 return HttpResponseRedirect('/profile')
            if user is not None: 
              login(request,user)
              return HttpResponseRedirect('/profile')
            



class CustomerRegistrationView(View):
   def get(self,request):

      fm=CustomerRegisterationForm()
      return render(request, 'app/customerregistration.html',{'fm':fm})

   def post(self,request):
       fm=CustomerRegisterationForm(request.POST)
       if fm.is_valid():
          fm.save()
          messages.success(request,"Congratulations your registeration is successfull!!")
         
          return HttpResponseRedirect('/login')
           

class CheckoutView(View):

   def get(self,request):
    if request.user.is_authenticated:

      usr=request.user
      ordp=Cart.objects.filter(user=usr)
      cust=Customer.objects.filter(user=request.user)
      return render(request, 'app/checkout.html',{'customer':cust,'orders':ordp})
    else:
       anonyid=request.COOKIES['sessionid']
        
       persist=HttpResponseRedirect('/registeration')
       persist.set_cookie('anonym',anonyid)
       
       return persist

   def post(self,request):
       usr=request.user

       id=request.POST['flexRadioDefault']
       customer=Customer.objects.get(id=id)
       c = Cart.objects.filter(user=request.user)
       
       for cart in c:
         id=cart.product.id
         print(id)
       
         p=Product.objects.get(id=id)
         print(p.id)
         order=OrderPlaced(user=usr,customer=customer,product=p,quantity=cart.quantity).save()
         cart.delete()
      
       return HttpResponseRedirect('/orders')
      
def orders(request):
   order=OrderPlaced.objects.filter(user=request.user)
   return render(request,'app/orders.html',{'order':order}) 

