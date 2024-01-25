from .cart import Cart

#Create context processor, cart can work all pages
def cart(request):
	#Return the default data from Cart
	return {'cart': Cart(request)}