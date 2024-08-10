from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'), # prima pagina

    path('book/<type>/', views.book_list, name='book_list'),  # base_generic, book_list
    path('book/<pk>/<bok>', views.book_detail, name='book_detail'),  # book_list
    path('book/<pk>/<pagina>/<bok>', views.book_book, name='book-book'), # base_generic, book_list

    path('thema/<lett>/<id_nome>', views.thema_list, name='thema_list'), # base_generic, topic_list
    path('nomeindex/<lett>/<id_nome>', views.nome_list, name='nome_list'), # base_generic, topic_list
    path('cittaindex/<lett>/<id_nome>', views.citta_list, name='citta_list'), # base_generic, topic_list

    path('article/<id_article>/', views.article_detail, name='article_detail'),  # article_list
    path('article/<book>/<author>/<lettera>/', views.article_list, name='article_list'),  # base_generic, article_list

    path('author/<lettera>/<rating>/', views.author_list, name='author_list'),  # base_generic, author_list
    path('author/<pk>/', views.author_detail, name='author_detail'),  # author_list

    path('rating/', views.author_rating, name='rating'),  # author_list



]