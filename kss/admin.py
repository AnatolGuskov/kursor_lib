from django.contrib import admin

from .models import (Genre, Type, Author, Book, Article,
                     BookBook)

from import_export.admin import ImportExportActionModelAdmin
from import_export import resources
from import_export import fields
from import_export.widgets import ForeignKeyWidget


#========================== GENRE ==============================
class GenreResource(resources.ModelResource):

   class Meta:
       model = Genre

class GenreAdmin(ImportExportActionModelAdmin):
    resourse_class = GenreResource
    list_display = ('id', 'thema', 'genre', 'image', )
    list_filter = ('thema',)

admin.site.register(Genre, GenreAdmin)

#========================= Genre ===================================
#========================= TYPE ===================================
class TypeResource(resources.ModelResource):

    class Meta:
        model = Type

class TypeAdmin(ImportExportActionModelAdmin):
    resourse_class = TypeResource
    list_display = ('id', 'type',  'pseudonym', 'image',)

admin.site.register(Type, TypeAdmin)


#========================= Type ===================================
#========================= AUTHOR ===================================
class AuthorResource(resources.ModelResource):

    class Meta:
        model = Author

class AuthorAdmin(ImportExportActionModelAdmin):
    resourse_class = AuthorResource
    list_display = ('id', 'cognome', 'nome', 'padrenome', 'rating', 'status',)

admin.site.register(Author, AuthorAdmin)


#========================= Author ===================================
# ======================== BOOK =======================================
class BookResource(resources.ModelResource):

   class Meta:
       model = Book

class BookAdmin(ImportExportActionModelAdmin):
    resourse_class = BookResource
    list_display = ('id', 'pseudonym', 'data', 'image_title', 'num_pag', 'num_aut', 'num_art', 'num_img',)
    list_filter = ('group', )

admin.site.register(Book, BookAdmin)

#========================= Book ===================================
#========================= BOOK BOOK ===================================
class BookBookResource(resources.ModelResource):

    class Meta:
        model = BookBook

class BookBookAdmin(ImportExportActionModelAdmin):
    resourse_class = BookBookResource
    list_display = ('id', 'tytle', 'book', 'pagina', 'status', 'image_pag',)
    list_filter = ('tytle',)

admin.site.register(BookBook, BookBookAdmin)


#========================= Book book ===================================
# ======================== ARTICLE =======================================
class ArticleResource(resources.ModelResource):

   class Meta:
       model = Article

class ArticleAdmin(ImportExportActionModelAdmin):
    resourse_class = ArticleResource
    list_display = ('id', 'title', 'data', 'book', 'pagina', 'num_pag', 'num_aut', 'num_img',)
    list_filter = ('book', 'author',)

admin.site.register(Article, ArticleAdmin)

#========================= Article ===================================
