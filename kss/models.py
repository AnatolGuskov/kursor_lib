from django.db import models


# GENRE   ================================      Model representing a Genre delle Storie
class Genre(models.Model):
    class Meta:
        ordering = ["genre"]

    thema = models.CharField(max_length=50, null=True)
    genre = models.CharField(max_length=100, null=True)
    image = models.ImageField(upload_to='kss/static/img_genre', default="")

    def __str__(self):
        return self.genre

# End GENRE      ==========================================================

# TYPE  ================================   Model representing a Tipi dei Libri
class Type (models.Model):
    class Meta:
        ordering = ["pseudonym"]

    type = models.CharField(max_length=50, null=True)
    pseudonym = models.CharField(max_length=50, null=True, default="")
    image = models.ImageField(upload_to='kss/static/img_tipi', null=True, blank=True, default="")

    def __str__(self):
        return self.type

# End TYPE    ==========================================================


# AUTHOR    ================================  Model representing a Catalochi
class Author(models.Model):
    class Meta:
        ordering = ["cognome", "nome"]

    cognome = models.CharField(max_length=50, null=True, default="-")
    nome = models.CharField(max_length=50, null=True, default="-")
    padrenome = models.CharField(max_length=50, null=True, default="-")
    status = models.DateField(null=True, blank=True)
    resume = models.TextField(max_length=5000, null=True)
    foto = models.ImageField(upload_to='kss/static/img_author', null=True, blank=True, default = "")
    num_art = models.IntegerField(blank=True, null=True)
    num_pag = models.IntegerField(blank=True, null=True)
    num_img = models.IntegerField(blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True)


    def __str__(self):
        return self.cognome + " " + self.nome

# End AUTHOR      ===========================================================

# BOOK    ================================   Model representing a Books
class Book(models.Model):
    class Meta:
        ordering = ["data", "pseudonym", "title", ]

    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=100)
    pseudonym = models.CharField(max_length=100)
    group = models.ManyToManyField(Type, help_text="Select a Typ for this book")
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the book")
    data = models.DateField(null=True, blank=True)
    isbn = models.CharField('ISBN', max_length=13,
                  help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    format = models.CharField(max_length=10)
    num_pag = models.IntegerField(blank=True, null=True)
    num_aut = models.IntegerField(blank=True, null=True)
    num_art = models.IntegerField(blank=True, null=True)
    num_img = models.IntegerField(blank=True, null=True)
    image_title = models.ImageField(upload_to='kss/static/img_book_title', null=True, default="")
    image_foto = models.ImageField(upload_to='kss/static/img_book_foto', null=True, default="")

    def __str__(self):
        return self.pseudonym

# End BOOK      ===========================================================

# BOOK BOOK   ======================================================
class BookBook(models.Model):
    class Meta:
        ordering = ["tytle", "pagina",]

    tytle = models.CharField(max_length=50, null=True)
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    pagina = models.CharField(max_length=20, null=True)
    status = models.CharField(max_length=20, null=True)
    image_pag = models.ImageField(upload_to='kss/static/img_book_pag', null=True, default = "")

    def __str__(self):
        return self.tytle

# End BOOK_BOOK      ===========================================================

# ARTICLE    ================================   Model representing of Articles
class Article(models.Model):
    class Meta:
        ordering = ["data", "pagina"]

    title = models.CharField(max_length=300)
    genre = models.ManyToManyField(Genre, )
    language = models.CharField(max_length=10)
    author = models.ManyToManyField('Author')
    book = models.ForeignKey('Book', on_delete = models.SET_NULL, null=True)
    pagina_book = models.CharField(max_length=1000, default="-")
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the article")
    data = models.DateField(null=True, blank=True)
    pagina = models.IntegerField(blank=True, null=True)
    num_pag = models.IntegerField(blank=True, null=True)
    num_aut = models.IntegerField(blank=True, null=True)
    num_img = models.IntegerField(blank=True, null=True)


    def __str__(self):
        return self.title

# End ARTICLE      ===========================================================



