#1.Question
# The behaviour of the signal that prints before and after the it triggred shows
# that the signal handler run synchronously

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
import time

@receiver(post_save, sender=User)
def user_post_save(sender, instance, **kwargs):
    print("Signal handler started")
    time.sleep(3)
    print("Signal handler finished")

# Triggering the signal
print("Before creating user")
user = User.objects.create(username='testuser', password='password')
print("After creating user")


# 2.Queston
    # Yes, Django signals typically run in the same thread as the 
    # caller unless explicitly configured to use threading or asynchronous behavior.

# Creating a Django signal and connect it to a handler:
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
import threading


@receiver(post_save, sender=User)
def user_post_save(sender, instance, **kwargs):
    print(f"Signal handler running in thread: {threading.current_thread().name}")


# Create a Django signal and connect it to a handler:
if __name__ == "__main__":
    print(f"Main thread: {threading.current_thread().name}")
    user = User.objects.create(username='testuser', password='password')

# The main thread prints the thread name, which is typically "MainThread".
# When the signal post_save is triggered after the User model is saved, it also prints the thread name.



# 3.Question
    # By default, Django signals do run in the same database transaction as the caller. 
    # If the caller is inside a transaction, the signal handlers will be executed within that transaction.

from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def user_post_save(sender, instance, **kwargs):
    print("Signal triggered: Inside transaction block")
    # Deliberately raise an error to rollback
    raise Exception("Error in signal handler!")

# Triggering the Signal
try:
    with transaction.atomic():
        user = User.objects.create(username='testuser', password='password')
        print("User created: Inside transaction block")
except Exception as e:
    print(f"Transaction rolled back due to: {e}")

# The signal is connected to the post_save of the User model.
# Inside a transaction block (transaction.atomic()), the User object is saved, which triggers the signal.
# The signal handler deliberately raises an exception.
# If the signal runs inside the same transaction, the exception in the signal handler should cause 
# the entire transaction to roll back, preventing the User object from being saved in the database.


#The Class Rectangle
class Rectangle:
    def __init__(self, length, width):
        self.length = length
        self.width = width

    def __iter__(self):
        # length
        yield {'length': self.length}
        # width
        yield {'width': self.width}


rect = Rectangle(10, 5)

for dimension in rect:
    print(dimension)
