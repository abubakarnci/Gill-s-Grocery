from django.db import models
from django.contrib.auth.models import User


# Creating models here.

# all tables and relationship between them


class Customer(models.Model):
	# relation with user table
    user=models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name=models.CharField(max_length=200, null=True)
    email=models.CharField(max_length=200, null=True)
    profile_pic=models.ImageField(default="icon.png",null=True, blank=True)
    
    def __str__(self):
        return str(self.user)
        
  
        
class Product(models.Model):
    name=models.CharField(max_length=200, null=True)
    price=models.DecimalField(max_digits=7, decimal_places=2)
    digital=models.BooleanField(default=False, null=True, blank=False)

    #need to add image
    image=models.ImageField(null=True, blank=True)
    
    def __str__(self):
        return self.name
        
    # image url
    @property
    def imageURL(self):
        try:
            url= self.image.url
        except:
            url=''
        
        return url
  
class Comment(models.Model):
	product = models.ForeignKey(Product, related_name="comments", on_delete=models.CASCADE)
	commenter= models.CharField(max_length=200, null=True)
	commenter_body= models.TextField()
	date_added= models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return '%s - %s' % (self.product.name, self.commenter)

class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False, null=True, blank=False)
	transaction_id = models.CharField(max_length=200, null=True)

	def __str__(self):
		return str(self.id)
		
	
	@property
	def shipping(self):
	    shipping= False
	    
	    orderitems= self.orderitem_set.all()
	    
	    for i in orderitems:
	        if i.product.digital == False:
	            shipping = True
	    
	    return shipping
		
		
		
	@property
	def get_cart_total(self):
	    
	    orderitems= self.orderitem_set.all()
	    total=sum([item.get_total for item in orderitems])
	    
	    return total
	    
	@property
	def get_cart_items(self):
	    
	    orderitems= self.orderitem_set.all()
	    total=sum([item.quantity for item in orderitems])
	    return total
	    
	
		
		
class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
	quantity=models.IntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)
	
	@property
	def get_total(self):
	    total = self.product.price * self.quantity
	    return total
	
	
class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    address=models.CharField(max_length=200, null=True)
    city=models.CharField(max_length=200, null=True)
    county=models.CharField(max_length=200, null=True)
    country=models.CharField(max_length=200, null=True)
    eircode=models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
	    return self.address

    