from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Account(models.Model):
    '''Encapsulates the data of a project Profile'''

    username = models.CharField(max_length=20) # username should be short
    biography = models.TextField(max_length = 1000)
    profile_picture = models.ImageField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        '''Return a readable string for this account.'''

        return f"{self.username} for the user {self.user}"
    
    def get_absolute_url(self):
        return reverse("my_account")


class Product(models.Model):
    '''Encapsulates the data pf a project Product'''

    profile = models.ForeignKey(Account, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=1000)
    image = models.ImageField(blank=True)
    category = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now=True)
    expected_price = models.DecimalField(max_digits=20, decimal_places=2) # 2 decimal places for price
    status = models.CharField(max_length=20, default="available")
    rating = models.DecimalField(max_digits=2,decimal_places=1, blank = True, null=True)

    def __str__(self):
        '''Return a readable string for this product.'''

        return f"{self.profile.username} wants to sell {self.name} for ${self.expected_price}"
    
    def get_absolute_url(self):
        return reverse("show_product", kwargs={"pk": self.pk})



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
    status = models.TextField(default="pending")

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

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(null=True)

    def __str__(self):
        return f"Image for {self.product.name}"
