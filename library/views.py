from django.shortcuts import render, redirect
from django.http import Http404, JsonResponse
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from django.utils.timezone import now
import json
from django.db.models import Q

# Create your views here.
def base(request):
    genres = Genre.objects.all()
    themes = Theme.objects.all()
    context = {'genres': genres, 'themes': themes}
    return render(request, 'library/base.html', context)

def home(request):
    genres = Genre.objects.all()
    themes = Theme.objects.all()
    books = Book.objects.all()
    trending = Book.objects.all().order_by('-rating')[:10]
    news = News.objects.all().order_by('-id')[:4]
    context = {'books': books, 'trending': trending, 'news': news, 'genres': genres, 'themes': themes}
    return render(request, 'library/home.html', context)

def lists_genre(request):
    genres = Genre.objects.all()
    themes = Theme.objects.all()
    books_by_genre = {genre: Book.objects.filter(genres=genre) for genre in genres}
    context = {'genres': genres, 'themes': themes, 'books_by_genre': books_by_genre}
    return render(request, 'library/lists_genre.html', context)

def lists_theme(request):
    genres = Genre.objects.all()
    themes = Theme.objects.all()
    books_by_theme = {theme: Book.objects.filter(themes=theme) for theme in themes}
    context = {'genres': genres, 'themes': themes, 'books_by_theme': books_by_theme}
    return render(request, 'library/lists_theme.html', context)

def lists_hot(request):
    genres = Genre.objects.all()
    themes = Theme.objects.all()
    hot = Book.objects.all().order_by('-rating')
    context = {'genres': genres, 'themes': themes, 'hot': hot}
    return render(request, 'library/lists_hot.html', context)

def history(request):
    genres = Genre.objects.all()
    themes = Theme.objects.all()
    
    if request.session.get("customer_id"):
        customer_id = request.session["customer_id"]
        borrowed_books = BorrowHistory.objects.filter(
            user_id=customer_id, 
            return_date__isnull=True
        )
        history = BorrowHistory.objects.filter(user_id=customer_id)
    else:
        borrowed_books = []
        history = []

    context = {'genres': genres, 'themes': themes, 'borrowed_books': borrowed_books, 'history': history }
    return render(request, 'library/history.html', context)

def news(request):
    genres = Genre.objects.all()
    themes = Theme.objects.all()
    news = News.objects.exclude(id=1)
    main_news = News.objects.get(id=1)
    reviews = BookReview.objects.all()
    context = {'news': news, 'main_news' : main_news, 'reviews': reviews, 'genres': genres, 'themes': themes}
    return render(request, 'library/news.html', context)

def book_detail(request, pk):
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        raise Http404("Book not found")
    
    genres_list = book.genres_list()  
    themes_list = book.themes_list() 
    genres = Genre.objects.all()
    themes = Theme.objects.all()

    context = {'book': book, 'genres_list': genres_list, 'themes_list': themes_list, 'genres': genres, 'themes': themes}    
    return render(request, 'library/book.html', context)

def review_detail(request, pk):
    try:
        review = BookReview.objects.get(pk=pk)
    except BookReview.DoesNotExist:
        raise Http404("Review not found")

    genres = Genre.objects.all()
    themes = Theme.objects.all()

    context = {'review': review, 'genres': genres, 'themes': themes}    
    return render(request, 'library/review.html', context)

def news_detail(request, pk):
    try:
        news = News.objects.get(pk=pk)
    except News.DoesNotExist:
        raise Http404("News not found")
    
    genres = Genre.objects.all()
    themes = Theme.objects.all()

    context = {'news': news, 'genres': genres, 'themes': themes}    
    return render(request, 'library/news_item.html', context)


@csrf_exempt
def submit_review(request):
    if request.method == "POST":
        book_name = request.POST.get('book_name')
        reviewer_name = request.POST.get('name')
        title = request.POST.get('title')
        basic_content = request.POST.get('basic_content')
        detailed_content = request.POST.get('review')
        image = request.FILES.get('image')

        try:
            book = Book.objects.get(name=book_name)  

            review = BookReview(
                book=book,
                reviewer_name=reviewer_name,
                title=title,
                basic_content=basic_content,
                detailed_content=detailed_content,
                image=image,
            )
            review.save()  

            return redirect('review_detail', pk=review.pk)

        except ObjectDoesNotExist:
            return render(request, 'library/news.html', {'error': 'Book not found'}) 
    else:
        return redirect('news')

def login(request):
    return render(request, 'library/login.html') 

def signup(request):
    return render(request, 'library/signup.html')
    
@csrf_exempt
def submit_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.objects.filter(email=email).first()
        if customer and check_password(password, customer.password):
            request.session["customer_id"] = customer.id 
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'library/login.html')

def logout(request):
    if 'customer_id' in request.session:
        del request.session['customer_id']  
    return redirect('home')

@csrf_exempt
def register(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')        
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if Customer.objects.filter(email=email).exists():
            messages.error(request,"The email is already in use. Please choose a different email.")
            return render(request, 'library/signup.html')     
        
        customer = Customer(
            first_name=first_name,
            last_name=last_name,
            email=email,
            telephone=phone,
            password= make_password(password)
        )
        customer.save()
        messages.success(request,"Registration successful! You can now log in.")
        return redirect('login')
    else:
        return render(request, 'library/signup.html')

def return_book(request):
    if request.method == "POST":
        customer_id = request.session.get("customer_id")
        data = json.loads(request.body)
        book_id = data.get("book_id")

        borrow_history = BorrowHistory.objects.filter(
            user_id=customer_id,
            book_id=book_id,
            return_date__isnull=True
        ).first()

        borrow_history.return_date = now()
        borrow_history.save()

        book = Book.objects.get(id=book_id)
        book.status = "available"
        book.save()

        return JsonResponse({'message': f"You have successfully returned book!"})
    else:
        return render(request, 'library/history.html')
    
def check_book_status(request):
    if request.method == "POST":
        data = json.loads(request.body)
        book_name = data.get("book_name").strip()
        try:
            book = Book.objects.get(name=book_name)
            book_status = book.status
            if book.status == "available":
                book_status = "Available"
            else:
                book_status = "Borrowed"
        except Book.DoesNotExist:
            book_status = "Book not found."
        return JsonResponse({'book_name': book_name, 'book_status': book_status})

def borrow_book(request):
    data = json.loads(request.body)
    book_name = data.get("book_name").strip()
    user_id = request.session.get("customer_id")  

    if not user_id:
        return JsonResponse({'message': "Please log in to borrow books."}, status=403)

    book = Book.objects.get(name=book_name)
    customer = Customer.objects.get(id = user_id)
    if book.status == "available":
        book.status = "borrowed"
        book.save()

        borrow_history = BorrowHistory(
            user= customer,
            book=book,
            registration_date= now(),
        )
        borrow_history.save()
        return JsonResponse({'message': f"You have successfully borrowed '{book.name}'!"})
    
def donate_book(request):
    data = json.loads(request.body)
    donor_name = data.get("donor_name").strip()
    contact = data.get("contact").strip()
    location = data.get("location").strip()
    book_name = data.get("book_name").strip()
    message = data.get("message").strip()
    donor_user = request.session.get("customer_id")  

    book_donation = BookDonation(
        donor_user= donor_user,
        donor_name= donor_name,
        contact= contact,
        location= location,
        book_name= book_name,
        message= message               
    )
    book_donation.save()
    return JsonResponse({'message': f"You have successfully donated!"})

def search_books(request):
    if request.method == "GET":
        query = request.GET.get("q", "").strip()
        if query:
            books = Book.objects.filter(
                Q(name__icontains=query) | Q(author__icontains=query)
            )[:10] 
            results = [{"id": book.id, "name": book.name, "author": book.author} for book in books]
            return JsonResponse(results, safe=False)
        return JsonResponse([], safe=False)  
    return JsonResponse({'error': 'Invalid method'}, status=405)