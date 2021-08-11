from django import forms
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm,AuthenticationForm, PasswordChangeForm, UserCreationForm, UsernameField
from django.contrib.auth.models import User
from django.db.models.fields import TextField
from django.forms import fields, widgets
from django.forms.models import ModelForm
from .models import Customer,Confirm

#To register the User 

class CustomerRegisterationForm(UserCreationForm):
    password1=forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2=forms.CharField(label='Password confirmation',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    email=forms.CharField(required=True,widget=forms.EmailInput(attrs={'class':'form-control'}))
    class Meta:
         model=User
         #weird 
         fields=('username','email','password1','password2')

         labels={'email':'Email'}    
         widgets={'username':forms.TextInput(attrs={'class':'form-control'})}






#LOGIN using AUThentication form
class LoginForm(AuthenticationForm):
     username=UsernameField(widget=forms.TextInput(attrs={'class':'form-control'}))
     password=UsernameField(widget=forms.PasswordInput(attrs={'class':'form-control'}))



#RESET password
class RestPassword(PasswordChangeForm):
      
      old_password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
      new_password1=forms.CharField(label="New Password",widget=forms.PasswordInput(attrs={'class':'form-control'}))
      new_password2=forms.CharField(label="Confirm Password",widget=forms.PasswordInput(attrs={'class':'form-control'}))
      




#Forgot password
class SetPassword(SetPasswordForm):
      new_password1=forms.CharField(label="New Password",widget=forms.PasswordInput(attrs={'class':'form-control'}))

      new_password2=forms.CharField(label="COnfirm Password",widget=forms.PasswordInput(attrs={'class':'form-control'}))

#TO BE ADDED/To be Combine with django-mailer
class PasswordRestEmail(PasswordResetForm):
      pass



class UserProfileForm(ModelForm):

      class Meta:
            model=Customer #MISTAKENLY WROTE User
#this implies inner meta fields are ignored 
# for unless they are from automatically generated ones
# hence we define custom fields outside meta class using forms 
          
          
          
            fields=['name','address','city','zip','state']
            labels={'name':'Name','address':'Address','city':'City','zip':'Zip','state':'State'}
            widgets={'name': forms.TextInput(attrs={'class':'form-control'}),
            'address':forms.TextInput(attrs={'class':'form-control'}),
        
            'city':forms.TextInput(attrs={'class':'form-control'}),
           
            'zip':forms.NumberInput(attrs={'class':'form-control'}),
            'state':forms.Select(attrs={'class':'form-control'}),
}



class ConfirmForm(ModelForm):

      class Meta:
         model=Confirm
         fields=['otp']
         labels={'otp':'OTP:'}
         widgets={'otp': forms.TextInput(attrs={'class':'form-control'})
         }
            