
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.models import User
from .models import Customer

# this is for relationship between customer and user table
# when new account will be created

@receiver(post_save, sender=User)        
def create_customer(sender, instance, created, **kwargs):
	
	if created:
		Customer.objects.create(user=instance, name=instance.username, email=instance.email)
		print('Customer created')

#post_save.connect(create_customer, sender=User)

@receiver(post_save, sender=User)        
def update_customer(sender, instance, created, **kwargs):
	if created == False:
		instance.customer.save()
		print('Customer updated')
		
#post_save.connect(update_customer, sender=User)

  