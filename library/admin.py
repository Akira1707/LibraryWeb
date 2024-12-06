from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Customer)
admin.site.register(Genre)
admin.site.register(Theme)
admin.site.register(Book)
admin.site.register(News)
admin.site.register(BookReview)
admin.site.register(BorrowHistory)
admin.site.register(BookDonation)
