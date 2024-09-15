from django.contrib import admin
from posts.models import Post, BookReview


class BookAdmin(admin.ModelAdmin):
    search_fields = ('title', 'description')
    list_display = ('title', 'description')

class BookReviewAdmin(admin.ModelAdmin):
    pass

admin.site.register(Post, BookAdmin)
admin.site.register(BookReview, BookReviewAdmin)
