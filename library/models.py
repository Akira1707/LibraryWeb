from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Customer(models.Model):
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=15)
    password = models.CharField(max_length=128)  

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Genre(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    
class Theme(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    
class Book(models.Model):
    STATUS_CHOICES = [
    ('borrowed', 'Borrowed'),
    ('available', 'Available'),
    ]

    image = models.ImageField()
    name = models.CharField(unique=True, max_length=255)
    author = models.CharField(max_length=255)
    genres = models.ManyToManyField(Genre, related_name='books')  
    themes = models.ManyToManyField(Theme, related_name='books') 
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')
    rating = models.FloatField(default=0.0, validators=[MinValueValidator(0.0),MaxValueValidator(5.0)])  
    basic_content = models.TextField(blank = True, null=True) 
    detailed_content = models.TextField(blank = True, null=True) 

    def __str__(self):
        return self.name
    
    def genres_list(self):
        return ", ".join([genre.name for genre in self.genres.all()])

    def themes_list(self):
        return ", ".join([theme.name for theme in self.themes.all()])
    
    def formatted(self, content_type='basic'):
        content = self.basic_content if content_type == 'basic' else self.detailed_content
        return content.replace('\n', '<br>') if content else ""
    
    @property 
    def ImageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class News(models.Model):
    image = models.ImageField()
    title = models.CharField(max_length=255)
    basic_content = models.TextField(blank = True, null=True) 
    detailed_content = models.TextField(blank = True, null=True) 

    def __str__(self):
        return self.title
    
    def formatted(self, content_type='basic'):
        content = self.basic_content if content_type == 'basic' else self.detailed_content
        return content.replace('\n', '<br>') if content else ""
    
    @property 
    def ImageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class BookReview(models.Model):
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True, related_name='reviews')
    reviewer_name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    image = models.ImageField(blank=True, null=True)
    basic_content = models.TextField(blank = True, null=True) 
    detailed_content = models.TextField(blank = True, null=True) 

    def __str__(self):
        return f"Review by {self.reviewer_name} on {self.book.name}"
    
    def formatted(self, content_type='basic'):
        content = self.basic_content if content_type == 'basic' else self.detailed_content
        return content.replace('\n', '<br>') if content else ""
    
    @property 
    def ImageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class BorrowHistory(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='borrow_history')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    registration_date = models.DateField()
    borrow_date = models.DateField(blank=True, null=True)
    return_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.user} borrowed {self.book}"


class BookDonation(models.Model):
    donor_user = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, related_name='donation_user')
    donor_name = models.CharField(max_length=255)
    contact = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    book_name = models.CharField(unique=True, max_length=255)
    message = models.TextField()

    def __str__(self):
        return f"{self.book_name} donated by {self.donor_name}"

