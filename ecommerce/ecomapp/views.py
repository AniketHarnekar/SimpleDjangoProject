from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from ecomapp.models import Product,newProduct,Cart,Order
from django.db.models import Q
import razorpay 
from django.core.mail import send_mail


# Create your views here.

def product(request):
    # prod=Product.objects.all()#database to view take the data 

    prod=Product.objects.filter(is_active=True)

    #print(prod)
    
    context={}#dictionary used to display data from view to template
    context['data']=prod
    return render(request,'index.html',context)

def register(request):

    if request.method=='GET':
        return render(request,'register.html')
    else:
        name=request.POST['name']
        email=request.POST['email']
        password=request.POST['pass']
        cpassword=request.POST['cpass']
        
        '''
        print(name)
        print(email)
        print(password)
        print(cpassword)
        '''
        context={}
        
        if name=="" or email=="" or password=="" or cpassword=="":
            #print("Please fill out the all fields")
            context['errormsg']="Please fill out the all field"
        elif password != cpassword:
            # print("password and confirm password is not same")
            context['errormsg']="password and confirm password is not same"
        elif len(password) < 8:
            # print("password should be greater than 8")
            context['errormsg']="password should be greater than 8"
        else:
            u=User.objects.create(username=name,email=email)
            u.set_password(password)
            u.save()
            context['success']="User Created successfully"
            
        return render(request,'register.html',context)

    
   # return HttpResponse("Data featched")

def user_login(request):
    if request.method=="GET":
        return render(request,'login.html')
    else:
        name=request.POST['name']
        password=request.POST['password']

        # print(name)

        auth_value=authenticate(username=name,password=password)

        #print(auth_value)

        context={}
        if auth_value==None:
            context['errormsg']="Invalid Username or password"
            return render(request,'login.html',context)
        else:
            login(request,auth_value)
            return redirect('/product')


def user_logout(request):
    logout(request)
    return redirect('/product')
            

def categoryfilter(request,cid):
    # prod=Product.objects.filter(category=cid,is_active=True)# (,) and condition check 
    # prod=Product.objects.filter(category=cid).filter(is_active=True)
    # Q class to use diffrent filter

    q1=Q(category=cid)
    q2=Q(is_active=True)
    prod=Product.objects.filter(q1 & q2)

    # print(prod)

    context={}
    context['data']=prod
    return render(request,'index.html',context)

def sort(request,sid):
    context={}

    # print(type(sid))

    if(sid=='1'):
        # prod=Product.objects.order_by('-price').filter(is_active=True)
        variablePrice='-price'
    else:
        # prod=Product.objects.order_by('price').filter(is_active=True)
        variablePrice='price'
    
    prod=Product.objects.order_by(variablePrice).filter(is_active=True)
    context['data']=prod
    return render(request,'index.html',context)

def pricefilter(request):
    
    min=request.GET['min']
    max=request.GET['max']

    # print(min)
    # print(max)

    q1=Q(price__gte=min)
    q2=Q(price__lte=max)
    product_price=Product.objects.filter(q1 & q2).filter(is_active=True)
    context={}
    context['data']=product_price

    return render(request,'index.html',context)

def search(request):
    search=request.GET['search']

    # print(search)

    prod_name=Product.objects.filter(name__icontains=search).filter(is_active=True) #colname__icontains for search by name of product
    prod_details=Product.objects.filter(product_detail__icontains=search).filter(is_active=True)
    searchFiled=prod_name.union(prod_details)

    context={}
    if len(searchFiled)==0:
        context['errormsg']="Product not found"
    
    context['data']=searchFiled
    return render(request,'index.html',context)

def product_detail(request,pid):
    product_detail=Product.objects.filter(id=pid)

    # print(p)

    context={}
    context['data']=product_detail
    print('detail',product_detail)
    return render(request,'product_detail.html',context)
    
def addtocart(request,pid):
    if request.user.is_authenticated:
        # print('User logged in')

        userId=User.objects.filter(id=request.user.id)
        productId=Product.objects.filter(id=pid)

        context={}
        context['data']=productId
        # print(u)

        q1=Q(uid=userId[0])
        q2=Q(pid=productId[0])
        cart=Cart.objects.filter(q1 & q2)
        print(userId)
        print(productId)
        if len(cart)==0:
            addCart=Cart.objects.create(uid=userId[0],pid=productId[0])
            addCart.save()
            context['success']="Product Added successfully..!!"
            return render(request,'product_detail.html',context)
        else:
            context['errormsg']="Product Already exist..!!"
            return render(request,'product_detail.html',context)

        # return HttpResponse("Product added")

        
    else:
        return redirect('/login') #if user is not login then goes to login page
    
def cart(request):
    cartDisplay=Cart.objects.filter(uid=request.user.id)
    print(cartDisplay)

    context={}
    context['data']=cartDisplay

    sum=0
    for i in cartDisplay:
        sum=sum+i.pid.price*i.qty
    context['total']=sum
    context['n']=len(cartDisplay)
    return render(request,'cart.html',context)

def updateqty(request,x,cid):
    cart=Cart.objects.filter(id=cid)
    productQuantity=cart[0].qty

    if x=='1':
        productQuantity=productQuantity+1
    elif productQuantity>1:
        productQuantity=productQuantity-1
    
    cart.update(qty=productQuantity)
    return redirect('/cart')

def delete(request,cid):
    deleteCart=Cart.objects.filter(id=cid)
    deleteCart.delete()
    return redirect('/cart')

def placeorder(request):
    placeOrder=Cart.objects.filter(uid=request.user.id)


    for i in placeOrder:
        amount=i.qty*i.pid.price


        order=Order.objects.create(uid=i.uid,pid=i.pid,qty=i.qty,amt=amount)
        order.save()
        i.delete()
    return redirect('/fetchorder')

def fetchorder(request):
    order=Order.objects.filter(uid=request.user.id)
    s=0

        
    for i in order:
        s=s+i.amt
        
        

    context={'data':order,'total':s,'n':len(order)}
   
    return render(request,'placeorder.html',context)

def makepayment(request):
    order=Order.objects.filter(uid=request.user.id)
    sum=0
    for i in order:
        sum=sum+i.amt
        i.delete()

    client = razorpay.Client(auth=("rzp_test_iEzo9xa9rh15KM", "P8Pw47YHzSJJ1aIKBllRxc6z"))

    data = { "amount": sum*100, "currency": "INR", "receipt": "order_rcptid_12" }
    payment = client.order.create(data=data)
    # print(payment)
    context={}
    context['payment']=payment
    return render(request,'pay.html',context)#pass web page response so use render
    # return HttpResponse("data featched")

def paymentsuccess(request):

    sub="order Status"
    msg="Order placed successfully..!"
    frm="harnekaraniket89@gmail.com"
    
    user=User.objects.filter(id=request.user.id)
    to=user[0].email
    send_mail(
        sub,
        msg,
        frm,
        [to],
        fail_silently=False
    )

    return render(request,'paymentsuccess.html')