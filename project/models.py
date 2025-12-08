from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Account(models.Model):
    '''Encapsulates the data of a project Profile'''

    username = models.TextField(max_length=20) # username should be short
    biography = models.TextField(max_length = 1000)
    profile_picture = models.ImageField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        '''Return a readable string for this account.'''

        return f"{self.username} for the user {self.user}"


class Product(models.Model):
    '''Encapsulates the data pf a project Product'''

    profile = models.ForeignKey(Account, on_delete=models.CASCADE)
    name = models.TextField(max_length=100)
    description = models.TextField(max_length=1000)
    image = models.ImageField()
    category = models.TextField(max_length=50)
    timestamp = models.DateTimeField(auto_now=True)
    expected_price = models.DecimalField(max_digits=20, decimal_places=2) # 2 decimal places for price
    satus = models.TextField(default="availabe")
    rating = models.DecimalField(max_digits=2,decimal_places=1, blank = True, null=True)

    def __str__(self):
        '''Return a readable string for this product.'''

        return f"{self.profile.username} wants to sell {self.name} for ${self.expected_price}"



class Favorite(models.Model):
    '''Encapsulates the data of a project Favorite'''

    profile = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        '''Return a readable string for the favorite.'''

        return f"{self.profile.username} favorited {self.product.name}"


class Bid(models.Model):
    '''Encapsulates the data of a project Bid'''
    profile = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    message = models.TextField()
    bid_price = models.DecimalField(max_digits=20, decimal_places=2)
    timestamp = models.DateTimeField(auto_now=True)
    status = models.TextField(default="unseen")

    def __str__(self):
        '''Return a readable string for this bid.'''

        return f"{self.profile.username} wants {self.product.name} for ${self.bid_price}"


class Order(models.Model):
    '''Encapsulates the data of a project Order'''

    profile = models.ForeignKey(Account, on_delete=models.CASCADE)
    date = models.DateField()
    total = models.DecimalField(max_digits=20, decimal_places=2)
    products = models.ManyToManyField(Product)

    def __str__(self):
        '''Return a readable string for this account.'''

        product_names = ", ".join(p.name for p in self.products.all())
        return f"{self.profile.username} bought {product_names} for ${self.total}"
