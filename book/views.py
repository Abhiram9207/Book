from django.shortcuts import render,redirect

# Create your views here.


from django.views.generic import View
from book.forms import BookForm,RegisterationForm,LoginForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.utils.decorators import method_decorator

from book.models import Books

def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,"invalid session")
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper

@method_decorator(signin_required,name="dispatch")
class Booklistview(View):
    def get(self,request,*args,**kwargs):
        qs=Books.objects.all()
        if "publisher" in request.GET:
            publisher=request.GET.get("publisher")
            qs=qs.filter(publisher__iexact=publisher)
        if "price_lt" in request.GET:
            amount=request.GET.get("price_lt")
            qs=qs.filter(price__lte=amount)
        return render(request,"book_list.html",{"data":qs})
    
@method_decorator(signin_required,name="dispatch")    
class BookDetailsView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Books.objects.get(id=id)
        return render(request,"books_details.html",{"data":qs})
    
@method_decorator(signin_required,name="dispatch")   
class BookDelectView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Books.objects.get(id=id).delete()
        messages.success(request,"book delected sucessfully")
        return redirect("book-all")
@method_decorator(signin_required,name="dispatch")    
class BookCreateView(View):
    def get(self,request,*args,**kwargs):
        form=BookForm()
        return render(request,"book-add.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=BookForm(request.POST,files=request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request,"book created sucessfully")
            return redirect("book-all")
        else:
            messages.error(request,"mobile created error")
            return render(request,"book-add.html",{"form":form})
@method_decorator(signin_required,name="dispatch")        
class BookUpdateView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        obj=Books.objects.get(id=id)
        form=BookForm(instance=obj)
        return render(request,"book_edit.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        obj=Books.objects.get(id=id)
        form=BookForm(request.POST,instance=obj,files=request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request,"book data updated sucessfully...")
            return redirect ("book-all")
        else:
            messages.error(request,"cant updated book data")
            return render(request,"book_edit.html",{"form":form})
        
class SignUpView(View):
    def get(self,request,*args,**kwargs):
        form=RegisterationForm()
        return render(request,"register.html",{form:"form"})
    
    def post(self,request,*args,**kwargs):
        form=RegisterationForm(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            messages.success(request,"Account created succesfully")
            return render(request,"register.html",{"form":form})
        else:
            messages.error(request,"Account creation failed")
            return render(request,"register.html",{"form":form})


class SignInView(View):
    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,"login.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            print(uname,pwd)
            user_object=authenticate(request,username=uname,password=pwd)
            if user_object:
                print("valid credentials")
                login(request,user_object)
                print(request.user)
                return redirect("book-all")
            else:
                print("invalid credentials")
            
            return render(request,"login.html",{"form":form})
        else:
            return render(request,"login.html",{"form":form})

@method_decorator(signin_required,name="dispatch")
class SignOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin")
