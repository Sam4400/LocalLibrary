from django.shortcuts import render

# Create your views here.

from catalog.models import Book, Author, BookInstance, Genre

from django.views import generic


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    # Genres
    num_genres = Genre.objects.count()

    # Books that contain Test
    num_books_test = Book.objects.filter(title__contains='test').count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres': num_genres,
        'num_books_test': num_books_test
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


class BookListView(generic.ListView):
    model = Book
    context_object_name = 'book_list'  # your own name for the list as a template variable
    #    queryset = Book.objects.filter(title__contains='war')[:5]  # Get 5 books containing the title war
    template_name = 'book_list.html'  # Specify your own template name/location
    paginate_by = 10


class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'book_detail.html'
    paginate_by = 10


class AuthorListView(generic.ListView):
    model = Author
    context_object_name = 'author_list'  # your own name for the list as a template variable
    #    queryset = Book.objects.filter(title__contains='war')[:5]  # Get 5 books containing the title war
    template_name = 'author_list.html'  # Specify your own template name/location
    paginate_by = 10


class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = 'author_detail.html'
    paginate_by = 10