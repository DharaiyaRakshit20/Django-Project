from django.shortcuts import render
from .models import *
from django.conf import settings
from django.core.mail import send_mail
import random
from datetime import datetime,time
from django.contrib.auth.hashers import make_password,check_password
from seller_app.models import *
from django.db.models import Q
from django.db.models import F
from django.http import HttpResponse
import razorpay
# Create your views here.

def home(request):
    return render(request,"index.html")

def register(request):
    if request.method == 'POST' :
        if request.POST["conformpassword"] == request.POST["password"]:
            global user_otp, start_time
            user_otp=random.randint(100000,999999)
            start_time=datetime.now().time()
            subject = 'OTP VERIFICATION PROCESS FOR MAN FASHION'
            message = f'Thanks For Choosing us your OTP is {user_otp}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [request.POST["email"], ]
            send_mail( subject, message, email_from, recipient_list )
            global temp
            temp={
                "name":request.POST["name"],
                "email":request.POST["email"],
                "password":request.POST["password"],
                "conformpassword":request.POST["conformpassword"]
            }
            return render(request,"otp.html")
        else:
            return render(request,"sign.html",{"msg":"Password And Conform Password not match"})
    else:
        return render(request,"sign.html")

def otp(request):
    if request.method == "POST" :
        if user_otp==int(request.POST["otp"]):
            end_time=datetime.now().time()
            time_deff=datetime.combine(datetime.today(),end_time) - datetime.combine(datetime.today(),start_time)
            second_deff= time_deff.total_seconds()
            if second_deff < 30:
                Register.objects.create(
                    name=temp["name"],
                    email=temp["email"],
                    password=make_password(temp["password"]),
                    conformpassword=make_password(temp["conformpassword"])
                )
                return render(request,"index.html",{"msg":temp["name"]})
            else:
                return render(request,"otp.html",{"msg":temp["email"],"msg2":"otp veild in 30 second","recent":True,"cur_email":temp["email"]})
        else:
            return render(request,"otp.html",{"mag":"OTP NOT MATCHED"})
    else:
        return render(request,"sign.html")


def resend_email(request,em):
        global user_otp, start_time
        user_otp=random.randint(100000,999999)
        start_time=datetime.now().time()
        subject = 'OTP VERIFICATION PROCESS FOR MAN FASHION'
        message = f'Thanks For Choosing us your OTP is {user_otp}'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [request.POST["email"], ]
        send_mail( subject, message, email_from, recipient_list )
        return render(request, "otp.html",{"msg":"Otp resend Succesfulkly"})
   

def login(request):
    if request.method == "POST":
        try:
            data=Register.objects.get(email=request.POST["email"])
            if check_password(request.POST["password"],data.password):
                request.session["email"]=request.POST["email"]
                return render(request,"index.html",{"data":data})
            else:
                return render(request,"login.html",{"msg":"Password Not Match"})
        except:
            return render(request,"login.html",{"msg":"We cannot find an account  with this email address"})

    else:
        return render(request,"login.html")

def logout(reqesut):
    del reqesut.session["email"]
    return render(reqesut,"login.html",{"msg":"Logout Sucsessfully"})

def profile(request):
    if request.method == "POST":
        data=Register.objects.get(email=request.session["email"])
        try:
            profile_image=request.FILES["propic"]
        except:
            profile_image=data.propic
        if request.POST["newpassword"]:
            if check_password(request.POST["oldpassword"],data.password):
                if request.POST["newconformpassword"]==request.POST["newpassword"]:
                        data.name=request.POST["name"]
                        data.password=make_password(request.POST["newpassword"])
                        data.conformpassword=make_password(request.POST["newconformpassword"])
                        data.propic=profile_image
                        data.save()
                        return render(request,"profile.html",{"data":data,"msg":"Profile Updated Successfully.."})
                else:
                    return render(request,"profile.html",{"data":data,"msg":"New Password and Conform Password Not Match"})
            else:
                return render(request,"profile.html",{"data":data,"msg":"Old Password Is Not Match.."})
        else:
            data.name=request.POST["name"]
            data.propic=profile_image
            data.save()
            return render(request,"profile.html",{"data":data,"msg":"Profile Updated Successfully.."}) 
    else:
        data=Register.objects.get(email=request.session["email"])
        return render(request,"profile.html",{"data":data}) 
    
def shop(request):
    data=Register.objects.get(email=request.session["email"])
    all_data=Listing_Catlog.objects.all()
    return render(request,"shop.html",{"all_data":all_data,"data":data})

def shop_details(request,pk):
    data=Register.objects.get(email=request.session["email"])
    one_data=Listing_Catlog.objects.get(id=pk)
    return render(request,"shop-details.html",{"data":data,"one_data":one_data,"sizes":one_data.Catlog_Size.split(","),"colors":one_data.Catlog_Color.split(",")})


def shopping_cart(request,pk):
    data=Register.objects.get(email=request.session["email"])
    try:
        # product=Listing_Catlog.objects.get(id=pk)  
        exists_data=Cart.objects.get( Q(product_id=pk) & Q(buyer_id=data.id) )
        exists_data.qty+=1
        exists_data.total=exists_data.qty * exists_data.product_id.Catlog_Price
        exists_data.save()
        return cart(request,{"data":data})
    except:
        product=Listing_Catlog.objects.get(id=pk)  
        Cart.objects.create(
            product_id=product,
            buyer_id=data,
            qty=1,
            total=product.Catlog_Price   
        )
        return cart(request,{"data":data})
    
def cart(request):
    data=Register.objects.get(email=request.session["email"])
    all_cart=Cart.objects.filter(buyer_id=data.id)
    final_total=0
    for i in all_cart:
        final_total=final_total+i.total
    return render(request,"shopping-cart.html",{"all_cart":all_cart,"final_total":final_total,"data":data})


def delete_cart(request,pk):
    data=Register.objects.get(email=request.session["email"])
    cart_data=Cart.objects.get(id=pk)
    cart_data.delete()
    return cart(request,{"data":data})


def update_cart(request):
    data=Register.objects.get(email=request.session["email"])
    if request.method == "POST":
        l1=request.POST.getlist("uqty")
        all_cart=Cart.objects.all()
        for i,j in zip(all_cart,l1) :
            i.qty=j
            i.total=int(j)*i.product_id.Catlog_Price
            i.save()
        return cart(request,{"data":data})    
    else:
        return cart(request,{"data":data})    
    
def checkout(request):
    data=Register.objects.get(email=request.session["email"])
    all_cart=Cart.objects.filter(buyer_id=data.id)
    final_total=0
    for i in all_cart:
        final_total=final_total+i.total
    return render(request,"checkout.html",{"final_total":final_total,"all_cart":all_cart,"data":data})


def search(request):
    data=Register.objects.get(email=request.session["email"])
    if request.method == "POST":
        query=request.POST["search"]
        all_data=Listing_Catlog.objects.filter(Q(Catlog_Name__icontains=query) | Q(Catlog_Discription__icontains=query))
        if all_data.count()==0:
             return render(request,"shop.html",{"msg":"Product Not found"})
        else:
            return render(request,"shop.html",{"all_data": all_data,"data":data}) 
    

def checkout_details(request):
    data=Register.objects.get(email=request.session["email"])
    if request.method == "POST":
        Details.objects.create(
            firstname=request.POST["fristname"],
            lastname=request.POST["lastname"],
            country=request.POST["country"],
            address=request.POST["address"],
            city=request.POST["city"],
            state=request.POST["state"],
            postcode=request.POST["postcode"],
            phone=request.POST["phone"],
            email=request.POST["email"],
            buyer_id=data
        )
        return render(request,"checkout.html",{"msg":"Your Order Is Successfully..","data":data})
    else:
         return render(request,"checkout.html",{"data":data})
#===============Payment Razorpay===============

from django.shortcuts import render
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest


# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
	auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))



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
			if result is not None:
				amount = 20000 # Rs. 200
				try:

					# capture the payemt
					razorpay_client.payment.capture(payment_id, amount)

					# render success page on successful caputre of payment
					return HttpResponse("Payment Success")
				except:

					# if there is an error while capturing payment.
					return HttpResponse("Payment Failed")

			else:

				# if signature verification fails.
				return render(request, 'paymentfail.html')
		except:

			# if we don't find the required parameters in POST data
			return HttpResponseBadRequest()
	else:
	# if other than POST request is made.
		return HttpResponseBadRequest()

def payment_response(request):
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    response = client.utility.verify_payment_signature(request.GET)
    if response['status'] == 'success':
        # Payment is successful
        # Process the payment and update your database accordingly
        return HttpResponse("Payment Success")
    else:
        # Payment failed
        # Handle the failure or display an error message
        return HttpResponse("Payment Failed")
