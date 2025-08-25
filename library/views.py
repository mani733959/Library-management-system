from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, BorrowRecord, Member
from .forms import BookForm

def home(request):
    books = Book.objects.all()
    return render(request, "library/home.html", {"books": books})

def add_book(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = BookForm()
    return render(request, "library/add_book.html", {"form": form})

def borrow_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if book.available_copies > 0:
        member = Member.objects.get(user=request.user)
        BorrowRecord.objects.create(book=book, member=member)
        book.available_copies -= 1
        book.save()
    return redirect("home")
