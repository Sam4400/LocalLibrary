import datetime

from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from catalog.forms import RenewBookForm
from catalog.models import Author


# Create your views here.

from catalog.models import Book, Author, BookInstance, Genre

from django.views import generic

# Class based authentication check 'class MyView(LoginRequiredMixin, View):'
from django.contrib.auth.mixins import LoginRequiredMixin

# Function based authentication checker @login_required
#                                       def my_view(request):
from django.contrib.auth.decorators import login_required

# Function check for permissions from model @permission_required('catalog.can_edit')
#                                           def my_view(request):
from django.contrib.auth.decorators import permission_required

# Class based permission functions
#   class MyView(PermissionRequiredMixin, View):
#   permission_required = 'catalog.can_mark_returned'
#   Or multiple permissions
#   permission_required = ('catalog.can_mark_returned', 'catalog.can_edit')
from django.contrib.auth.mixins import PermissionRequiredMixin

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

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres': num_genres,
        'num_books_test': num_books_test,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


class BookListView(generic.ListView):
    model = Book
    context_object_name = 'book_list'  # your own name for the list as a template variable
    #    queryset = Book.objects.filter(title__contains='war')[:5]  # Get 5 books containing the title war
    template_name = 'book_list.html'  # Specify your own template name/location
    paginate_by = 10


class BookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Book
    template_name = 'book_detail.html'
    paginate_by = 10


class AuthorListView(generic.ListView):
    model = Author
    context_object_name = 'author_list'  # your own name for the list as a template variable
    #    queryset = Book.objects.filter(title__contains='war')[:5]  # Get 5 books containing the title war
    template_name = 'author_list.html'  # Specify your own template name/location
    paginate_by = 10


class AuthorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Author
    template_name = 'author_detail.html'
    paginate_by = 10


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


class AllLoanedBooksListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    permission_required = 'catalog.can_mark_returned'
    model = BookInstance
    template_name = 'bookinstance_list_borrowed_all.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back').order_by('borrower__last_name')


@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'book_renew_librarian.html', context)

class AuthorCreate(LoginRequiredMixin, PermissionRequiredMixin,CreateView):
    permission_required = 'author.can_add'
    model = Author
    fields = '__all__'
    initial = {'date_of_death': '05/01/2018'}
    template_name = 'author_form.html'

class AuthorUpdate(LoginRequiredMixin, PermissionRequiredMixin,UpdateView):
    permission_required = 'author.can_edit'
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    template_name = 'author_form.html'

class AuthorDelete(LoginRequiredMixin, PermissionRequiredMixin,DeleteView):
    permission_required = 'author.can_delete'
    model = Author
    success_url = reverse_lazy('authors')
    template_name = 'author_confirm_delete.html'


class AuthorEditList(LoginRequiredMixin, PermissionRequiredMixin,generic.ListView):
    permission_required = 'author.can_edit'

    model = Author
    template_name = 'edit_authors.html'
    paginate_by = 10


class BookCreate(LoginRequiredMixin, PermissionRequiredMixin,CreateView):
    permission_required = 'book.can_add_book'
    model = Book
    fields = '__all__'
    template_name = 'book_form.html'

class BookUpdate(LoginRequiredMixin, PermissionRequiredMixin,UpdateView):
    permission_required = 'book.can_edit_book'
    model = Book
    fields = '__all__'
    template_name = 'book_form.html'

class BookDelete(LoginRequiredMixin, PermissionRequiredMixin,DeleteView):
    permission_required = 'book.can_delete_book'
    model = Author
    success_url = reverse_lazy('authors')
    template_name = 'book_confirm_delete.html'


class BookEditList(LoginRequiredMixin, PermissionRequiredMixin,generic.ListView):
    permission_required = 'book.can_edit_book'

    model = Book
    template_name = 'edit_books.html'
    paginate_by = 10