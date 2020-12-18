from django.contrib import admin
from book_rate.models import Book, User, Rate


# Register your models here.


class RelationAdmin(admin.ModelAdmin):
    raw_id_fields = ['user', 'book']


admin.site.register(Book)
admin.site.register(User)
admin.site.register(Rate, RelationAdmin)
