from django.urls import path
from books import views

urlpatterns = [
    path('', views.BooksModelView.as_view(), name='index'),
    path('book/', views.BookList.as_view(), name='book_list'),
    path('author/', views.AuthorList.as_view(), name='author_list'),
    path('publisher/', views.PublisherList.as_view(), name='publisher_list'),
    path('book/<book_id>)/', views.BookDetail.as_view(), name='book_detail'),
    path('author/<author_id>)/', views.AuthorDetail.as_view(), name='author_detail'),
    path('publisher/<publisher_id>)/', views.PublisherDetail.as_view(), name='publisher_detail'),
]