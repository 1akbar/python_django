from django.shortcuts import render, redirect
from .models import Product, Categories
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswrodForm
from django import forms



def update_password(request):
	if request.user.is_authenticated:
		current_user = request.user
		#did they fill out the form
		if request.method == 'POST':
			form = ChangePasswrodForm(current_user, request.POST)
			if form.is_valid():
				form.save()
				messages.success(request, "Your Password Has Been Updated, " )
				login(request, current_user)
				return redirect('update_user')
			else:
				for error in list(form.errors.values()):
					messages.error(request, error)
					return redirect('update_password')

		else:
			form = ChangePasswrodForm(current_user)
			return render(request, "update_password.html", {'form':form})

	else:
		messages.success(request, "You must be logged in")
		return redirect('home')


	return render(request, 'update_password.html', {})



def update_user(request):
	if request.user.is_authenticated:
		current_user = User.objects.get(id=request.user.id)
		user_form = UpdateUserForm(request.POST or None, instance=current_user)

		if user_form.is_valid():
			user_form.save()

			login(request, current_user)
			messages.success(request, "User has been Updated")
			return redirect('home')
		return render(request, 'update_user.html', {'user_form':user_form})
	else:
		messages.success(request, "You must be loggen in")
		return redirect('home')


def category_summary(request):
	categories = Categories.objects.all()
	return render(request, 'category_summary.html', {"categories":categories})

def category(request, foo):
	#replace hyphens with spaces
	foo = foo.replace('-', '')
	#grab the category from the url

	try:
		#look up the category
		category = Categories.objects.get(name=foo)
		products = Product.objects.filter(category=category)
		return render(request, 'category.html', {'products':products, 'category':category})
	except:
		messages.success(request, ("The Category doesn't exist"))
		return redirect('home') 

	


def product(request,pk):
	product = Product.objects.get(id=pk)
	return render(request, 'product.html', {'product':product})


def home(request):
	products = Product.objects.all()
	return render(request, 'home.html', {'products':products})


def about(request):
	return render(request, 'about.html', {})

def login_user(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, ("You have been Logged In"))
			return redirect('home')
		else:
			messages.success(request, ("Error, Try again"))
			return redirect('login')
	else:
		return render(request, 'login.html', {})


def logout_user(request):
	logout(request)
	messages.success(request, ("you have been logged out!"))
	return redirect('home')



def register_user(request):
	form = SignUpForm()
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			#log in user
			username = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, ("Registered Successfully! Welcome!"))
			return redirect('home')
		else:
			messages.success(request, ("There is a problem, Please Try Again!"))
			return redirect('register')
			

	else:

		return render(request, 'register.html', {'form':form})