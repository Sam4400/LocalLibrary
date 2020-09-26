from django.contrib import admin

# Register your models here.

from .models import Author, Genre,Language,Book,BookInstance

#admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Language)
#admin.site.register(Book)
#admin.site.register(BookInstance)

class BooksInLine(admin.TabularInline):
        model = Book
        extra = 0

# Define the admin class
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')

    inlines = [BooksInLine]

    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]

# Register the admin class with the associated model
admin.site.register(Author, AuthorAdmin)

#Register the inline instance to show BookInstance information on the Book screen
class BooksInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0

# Register the Admin classes for Book using the decorator
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')

    inlines = [BooksInstanceInline]

# Register the Admin classes for BookInstance using the decorator
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book','language','status','due_back' )

    list_filter = ('status', 'due_back')

#set groupings on the record view
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back')
        }),
    )