from django.contrib import admin
# from .models import SampleModel

# admin.site.register(SampleModel)

from .models import Book, Review

admin.site.register(Book)
admin.site.register(Review)