from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('base/', views.base, name='base'),
    path('login/', views.login, name='login'),
    path('submit_login/', views.submit_login, name='submit_login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('register/', views.register, name='register'),
    path('lists_genre/', views.lists_genre, name='lists_genre'),
    path('lists_theme/', views.lists_theme, name='lists_theme'),
    path('lists_hot/', views.lists_hot, name='lists_hot'),
    path('history/', views.history, name='history'),
    path('news/', views.news, name='news'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
    path('review/<int:pk>/', views.review_detail, name='review_detail'),
    path('news_item/<int:pk>/', views.news_detail, name='news_detail'),
    path('submit_review/', views.submit_review, name='submit_review'),
    path('check_book_status/', views.check_book_status, name='check_book_status'),
    path('borrow_book/', views.borrow_book, name='borrow_book'),
    path('return_book/', views.return_book, name='return_book'),
    path('donate_book/', views.donate_book, name='donate_book'),
    path('search-books/', views.search_books, name='search_books'),
]
