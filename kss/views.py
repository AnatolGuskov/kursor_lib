from django.shortcuts import render
from django.views import generic
from ctypes  import *
import time

from .models import (Article, Author, Book, Genre, Type,
                     BookBook,
                     )



# ============== INDEX =============================
def index(request):
# =============== Visits ===================
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

# =============== Index Quantita ===================
    num_author = Author.objects.all().count()
    num_article = Article.objects.all().count()
    num_book = Book.objects.all().count()
    num_genre = Genre.objects.all().filter(image__isnull=False).count()
    num_type = Type.objects.all().count()

    # num_art_letto = 0
    # article_list = Article.objects.all()
    # for art in article_list:
    #     book_letto = BookBook.objects.all().filter(book = art.book)
    #     if book_letto: num_art_letto = num_art_letto + 1

    num_art_letto = 0
    num_book_letto = 0
    books = Book.objects.all()
    for book in books:
        letto = BookBook.objects.all().filter(book = book.id).count()
        if letto:
            num_book_letto = num_book_letto + 1
            num_art_letto = num_art_letto + book.num_art



# =============== Render INDEX =============
    return render(
        request,
        'index.html',
        context={'num_author': num_author,
                 'num_article': num_article,         'num_art_letto': num_art_letto,
                 'num_book': num_book,               'num_book_letto': num_book_letto,
                 'num_genre': num_genre,             'num_type': num_type,

                 }
    )
# ============== end INDEX =============================

# ============== BOOK_LIST =============================
def book_list(request, type):
    if type == "0":
        booklist = Book.objects.all().order_by('-data',)
        num_book = Book.objects.all().count()
    else:
        booklist = Book.objects.all().filter(group = type).order_by('-data',)
        num_book = Book.objects.all().filter(group = type).count()

    for book in booklist:
        book_content = BookBook.objects.all().filter(book = book.id)
        if book_content: book.content = "1"
        book.path = str(book.image_title)
        book.path = book.path[book.path.find("static") + 7:]
        if len(book.path) > 2:
            book.img = "1"
        else:
            book.img = "0"
        book.num_article = Article.objects.all().filter(book = book.id).count()

    typelist = Type.objects.all()
    num_type = Type.objects.all().count()

    for typ in typelist:
        typ.num_book_type = Book.objects.all().filter(group = typ.id).count()

    if type != "0":
        type_book = Type.objects.get(id = type).type
    else: type_book = "Збірок"

# -----------------------------------------------------
    return render(
        request,
        'book_list.html',
        context={'booklist': booklist, 'typelist': typelist,
                 'num_book': num_book, 'num_type': num_type, 'type_book': type_book,
                 'tytle_nome': 'Випуски',
                 'right_fon': 'img_background/Chiesa_Gievka_3.jpg',
                 'right_text': "Випуски",

                                        }
    )
# ============== END Book_list =======================

# ============== BOOK_DETAIL =============================
def book_detail(request, pk, bok):

    book_detail = Book.objects.get(id = pk)
    book_img = str(book_detail.image_title)
    book_img = book_img[book_img.find("static") + 7:]
    book_foto = str(book_detail.image_foto)
    book_foto = book_foto[book_foto.find("static") + 7:]

    # type = book.group

# ----------------------------------------
    book_articles = Article.objects.all().filter(book = pk).order_by("pagina")
    for art in book_articles:
        books = BookBook.objects.all().filter(book = art.book)
        if books:
            art.book_content = "1"
        art.id_book = book_detail.id
        if books and art.summary != "Assente":
            art.content = "1"
        else:
            art.content = "0"
        art.authore = ""
        authors = Article.objects.get(id = art.id).author.all()  # ManyToMany Tutti Authors per Article !!!!!!!!!!!!!
        for auth in authors:
            line =""
            if auth.nome != "-" and auth.padrenome != "-":
                line = line + auth.cognome + "\xa0" + auth.nome[:1] + ".\xa0" + auth.padrenome[:1] + "."  # 1 nome
            if auth.nome != "-" and auth.padrenome == "-":
                line = line + auth.cognome + "\xa0" + auth.nome[:1] + ".\xa0"  # 1 nome
            if auth.nome == "-" and auth.padrenome == "-":
                line = line + auth.cognome  # 1 nome  Валентина Дмитрівна	Редакційна колегія -. -.
            art.authore = art.authore + line + ", "

        art.authore = art.authore[:-2]
        art.author_id = authors[0].id

# ----------------------------------------
    booklist = Book.objects.all().order_by("-data")
    num_book = Book.objects.all().count()
    for book in booklist:
        book_content = BookBook.objects.all().filter(book = book.id)
        if book_content: book.content = "1"
        book.path = str(book.image_title)
        book.path = book.path[book.path.find("static") + 7:]
        if len(book.path) > 2: book.img = "1"
        else: book.img = "0"
    tytle_nome = ""

# ----------------------------------------

    book_book = BookBook.objects.all().filter(book = pk)
    if book_book:
        book_content = "1"
    else:
        book_content = "0"

# ------------------------------------------
    return render(
        request,
        'book_detail.html',
        context={'book': book_detail, 'book_articles': book_articles,
                 'book_pk': pk,  'book_content': book_content,
                 'booklist': booklist, 'num_book': num_book,
                 'tytle_nome': tytle_nome,
                 'book_img': book_img,    'book_foto': book_foto,
                 'right_fon': 'img_background/Chiesa_Gievka_blue_3.jpg',
                 'right_text': "Збірок",
                                        }
    )
# ============== END BOOK_detail =======================

# ============== BOOK_BOOK =============================
def book_book(request, pk, pagina, bok):

    book = Book.objects.get(pk = pk)

    nome_parole = book.title.split(" ")
    book_nome = ""
    for i in range(0, len(nome_parole)):
        if (len(book_nome) + len(nome_parole[i])) < 66:
            book_nome = book_nome + " " + nome_parole[i]
        else:
            break
    if len(book.title) > 66:
        book_nome = book_nome + " ..."

    book_pseudo = book.pseudonym
    book_data = book.data.year
    book_img = str(book.image_title)
    book_img = book_img[book_img.find("static")+7:]
    book_pk = book.pk

    book_list1 = BookBook.objects.all().filter(book=pk)
    book_prefiks = book_list1[0].pagina[:pagina.find(" ")]
    for pag in book_list1:
        pag.num_pag = pag.pagina[pag.pagina.find(" ") + 0:]  # 0 pagina
        pag.num_corte = int(pag.num_pag[:4])
        pag.path = str(pag.image_pag)
        pag.path = pag.path[pag.path.find("static")+7:]

    book_list = []
    pagina = int(pagina)
    if int(pagina/2)*2 < pagina:
        pagina = pagina - 1
    for pag in book_list1:
        if pag.num_corte < pagina: pass
        else: book_list = book_list + [pag]

    book_content = (Article.objects.all().filter(book=pk).order_by("pagina") &
                    Article.objects.all().exclude(summary="Assente").order_by("pagina"))
    for page in book_content:
        if len(page.title) > 110:
            page.title = page.title[:110] + "..."
        authorslist = Article.objects.get(pk=page.pk).author.all()
        page.authors = ""
        for auth in authorslist:
            page.authors = page.authors + auth.cognome + ", "
        page.authors = page.authors[:-2]

    #-----------------------------------------------------------

    return render(
        request,
        'book_book.html',
        context={'book_list': book_list,
                 'book_nome': book_nome, 'book_pseudo': book_pseudo,
                 'book_data': book_data, 'book_img': book_img,
                 'book_pk': book_pk,
                 'book_content': book_content,

                 }
    )
# ============== END book book =======================

# ============== THEMA_LIST =============================
def thema_list(request, lett, id_nome):

# -----------------------------------------------
    articlelist = Article.objects.all().filter(genre = id_nome).order_by("-data")
    numer = len(articlelist)
# -----------------------------------------------
    if lett == "0" and id_nome == "0":
        thema_list = Genre.objects.all().exclude(thema="Особа") & Genre.objects.all().exclude(thema="Місце")
        numer = thema_list.count()

        for tem in thema_list:
            if tem.genre.find(":") > -1:
                tem.genre = "\xa0\xa0" + tem.genre[tem.genre.find(":"):]
            else:
                tem.genre = tem.genre.upper()

        right_text = "Усього тем"
        genre_text = "Тематичний покажчик"
# -----------------------------------------------
    if lett != "0" and id_nome == "0":
        lettera = lett
        thema_list = (Genre.objects.all().exclude(thema="Особа") & Genre.objects.all().exclude(thema="Місце")
                      & Genre.objects.all().filter(genre__startswith = lettera))

        numer = thema_list.count()

        for tem in thema_list:
            if tem.genre.find(":") > -1:
                tem.genre = "\xa0\xa0" + tem.genre[tem.genre.find(":"):]
            else:
                tem.genre = tem.genre.upper()

        right_text = "Усього на літеру " + lett
        genre_text = "Тематичний покажчик (" + lett + ")"

# -----------------------------------------------
    if id_nome != "0":
        thema_list = Genre.objects.get(id = id_nome)

        right_text = "Статей"
        genre_text = thema_list.genre
# -----------------------------------------------
    for art in articlelist:
        art.pseudo = art.book
        art.authore = ""
        authors = Article.objects.get(id=art.id).author.all()  # ManyToMany Tutti Authors per Article !!!!!!
        author_set = []
        for auth in authors:
            line = ""
            if auth.nome != "-" and auth.padrenome != "-":
                line = line + auth.cognome + "\xa0" + auth.nome[:1] + ".\xa0" + auth.padrenome[:1] + "."  # 1 nome
            if auth.nome != "-" and auth.padrenome == "-":
                line = line + auth.cognome + "\xa0" + auth.nome[:1] + ".\xa0"  # 1 nome
            if auth.nome == "-" and auth.padrenome == "-":
                line = line + auth.cognome  # 1 nome  Валентина Дмитрівна	Редакційна колегія -. -.
            art.authore = art.authore + line + ", "
        art.authore = art.authore[:-2]
        art.author_id = authors[0].id

        books = BookBook.objects.all().filter(book=art.book)
        if books: art.book_content = "1"
        book = Book.objects.get(pseudonym=art.book)
        art.id_book = book.id
        if books and art.summary != "Assente":
            art.content = "1"
        else:
            art.content = "0"
# -----------------------------------------------
    letteralist = []
    lettera_set = ""
    thema_lett = Genre.objects.all().exclude(thema="Особа") & Genre.objects.all().exclude(thema="Місце")
    for art in thema_lett:
        thema_lett = []
        if lettera_set != art.thema[0]:
            lettera_set = art.thema[0]
            lettera_set_title = art.thema
            thema_lett += [lettera_set]
            thema_lett += [lettera_set_title]
            letteralist = letteralist + [thema_lett]

    # ------------------------------------------
    return render(
        request,
        'topic_list.html',
        context={'themalist': thema_list, 'numer': numer,
                 'articlelist': articlelist, 'letteralist': letteralist,
                 'right_text': right_text,
                 'genre_text': genre_text, 'genre': id_nome,
                 'alfabet': "thema_list", 'titul': "Теми статей",
                                       }
    )
# ============== END Thema_List =======================


# ============== >NOME_LIST =============================
def nome_list(request, lett, id_nome):
    articlelist = Article.objects.all().filter(genre = id_nome).order_by("-data")
    numer = len(articlelist)
# -----------------------------------------------
    if lett == "0" and id_nome == "0":
        nome_list = Genre.objects.all().filter(thema = "Особа")
        numer = Genre.objects.all().filter(thema = "Особа").count()
        for nome in nome_list:
            nome_pulito = nome.genre.split(":")
            nome.genre = nome_pulito[1]

        right_text = "Усього особ"
        genre_text = "Іменний покажчик"
# -----------------------------------------------
    if lett != "0" and id_nome == "0":
        lettera = "Особа: " + lett
        nome_list = Genre.objects.all().filter(genre__startswith = lettera)
        numer = Genre.objects.all().filter(genre__startswith = lettera).count()
        for nome in nome_list:
            nome_pulito = nome.genre.split(":")
            nome.genre = nome_pulito[1]

        right_text = "Усього на літеру " + lett
        genre_text = "Іменний покажчик (" + lett + ")"

# -----------------------------------------------
    if id_nome != "0":
        nome_list = Genre.objects.get(id = id_nome)

        right_text = "Статей"
        genre_text = nome_list.genre
# -----------------------------------------------
    for art in articlelist:
        art.pseudo = art.book
        art.authore = ""
        authors = Article.objects.get(id=art.id).author.all()  # ManyToMany Tutti Authors per Article !!!!!!
        author_set = []
        for auth in authors:
            line = ""

            if auth.nome != "-" and auth.padrenome != "-":
                line = line + auth.cognome + "\xa0" + auth.nome[:1] + ".\xa0" + auth.padrenome[:1] + "."  # 1 nome
            if auth.nome != "-" and auth.padrenome == "-":
                line = line + auth.cognome + "\xa0" + auth.nome[:1] + ".\xa0"  # 1 nome
            if auth.nome == "-" and auth.padrenome == "-":
                line = line + auth.cognome  # 1 nome  Валентина Дмитрівна	Редакційна колегія -. -.
            art.authore = art.authore + line + ", "
        art.authore = art.authore[:-2]
        art.author_id = authors[0].id

        books = BookBook.objects.all().filter(book=art.book)
        if books: art.book_content = "1"
        book = Book.objects.get(pseudonym=art.book)
        art.id_book = book.id
        if books and art.summary != "Assente":
            art.content = "1"
        else:
            art.content = "0"
# -----------------------------------------------
    letteralist = []
    lettera_set = ""
    nome_lett = Genre.objects.all().filter(thema = "Особа")
    for art in nome_lett:
        nome_lett = []
        if lettera_set != art.genre[7:8]:
            lettera_set = art.genre[7:8]
            lettera_set_title = art.genre[7:]
            nome_lett += [lettera_set]
            nome_lett += [lettera_set_title]
            letteralist = letteralist + [nome_lett]

    # ------------------------------------------
    return render(
        request,
        'topic_list.html',
        context={'themalist': nome_list, 'numer': numer,
                 'articlelist': articlelist, 'letteralist': letteralist,
                 'right_text': right_text,
                 'genre_text': genre_text, 'genre': id_nome,
                 'alfabet': "nome_list", 'titul': "Особи статей",

                                        }
    )
# ============== END Nome_List =======================

# ============== CITTA_LIST =============================
def citta_list(request, lett, id_nome):
    articlelist = Article.objects.all().filter(genre = id_nome).order_by("-data")
    numer = len(articlelist)
# -----------------------------------------------
    if lett == "0" and id_nome == "0":
        citta_list = Genre.objects.all().filter(thema = "Місце")
        numer = citta_list.count()
        for nome in citta_list:
            nome_pulito = nome.genre.split(":")
            nome.genre = nome_pulito[1]

        right_text = "Усього назв"
        genre_text = "Географічний покажчик"
# -----------------------------------------------
    if lett != "0" and id_nome == "0":
        lettera = "Місце: " + lett
        citta_list = Genre.objects.all().filter(genre__startswith = lettera)
        numer = citta_list.count()
        for nome in citta_list:
            nome_pulito = nome.genre.split(":")
            nome.genre = nome_pulito[1]

        right_text = "Усього на літеру " + lett
        genre_text = "Географічний покажчик (" + lett + ")"

# -----------------------------------------------
    if id_nome != "0":
        citta_list = Genre.objects.get(id = id_nome)

        right_text = "Статей"
        genre_text = citta_list.genre
# -----------------------------------------------
    for art in articlelist:
        art.pseudo = art.book
        art.authore = ""
        authors = Article.objects.get(id=art.id).author.all()  # ManyToMany Tutti Authors per Article !!!!!!
        author_set = []
        for auth in authors:
            line = ""

            if auth.nome != "-" and auth.padrenome != "-":
                line = line + auth.cognome + "\xa0" + auth.nome[:1] + ".\xa0" + auth.padrenome[:1] + "."  # 1 nome
            if auth.nome != "-" and auth.padrenome == "-":
                line = line + auth.cognome + "\xa0" + auth.nome[:1] + ".\xa0"  # 1 nome
            if auth.nome == "-" and auth.padrenome == "-":
                line = line + auth.cognome  # 1 nome  Валентина Дмитрівна	Редакційна колегія -. -.
            art.authore = art.authore + line + ", "
        art.authore = art.authore[:-2]
        art.author_id = authors[0].id

        books = BookBook.objects.all().filter(book=art.book)
        if books: art.book_content = "1"
        book = Book.objects.get(pseudonym=art.book)
        art.id_book = book.id
        if books and art.summary != "Assente":
            art.content = "1"
        else:
            art.content = "0"
# -----------------------------------------------
    letteralist = []
    lettera_set = ""
    citta_lett = Genre.objects.all().filter(thema = "Місце")
    for art in citta_lett:
        citta_lett = []
        if lettera_set != art.genre[7:8]:
            lettera_set = art.genre[7:8]
            lettera_set_title = art.genre[7:]
            citta_lett += [lettera_set]
            citta_lett += [lettera_set_title]
            letteralist = letteralist + [citta_lett]

    # ------------------------------------------
    return render(
        request,
        'topic_list.html',
        context={'themalist': citta_list,  'numer': numer,
                 'articlelist': articlelist, 'letteralist': letteralist,
                 'right_text': right_text,
                 'genre_text': genre_text, 'genre': id_nome,
                 'alfabet': "citta_list",  'titul': "Міста статей",

                                        }
    )
# ============== END Citta_List =======================

# ============== ARTICLE_LIST =============================
def article_list(request, book, author, lettera):

    nome_book = ""
    articlelist = []
    num_line = 10000
    if book == "-1" and author == "0" and lettera == "0":
        articlelist = Article.objects.all().order_by('pagina_book')[:num_line]
        num_article = Article.objects.all().count()
    if book == "0" and author == "0" and lettera == "0":
        num_line = 100
        articlelist = Article.objects.all().order_by('pagina_book')[:num_line]
        num_article = Article.objects.all().count()
    if book != "0" and book != "-1" and author == "0" and lettera == "0":
        articlelist = Article.objects.all().filter(book = book)
        num_article = Article.objects.all().filter(book = book).count()
        nome_book = Book.objects.get(id=book).pseudonym
    if book == "0" and author != "0" and lettera == "0":
        articlelist = Article.objects.all().filter(author = author)
        num_article = Article.objects.all().filter(author = author).count()
    if book == "0" and author == "0" and lettera != "0":
        articlelist = Article.objects.all().filter(title__startswith=lettera).order_by('pagina_book')
        num_article = Article.objects.all().filter(title__startswith=lettera).count()
        tytle_nome = "( " + lettera + " )"

# ---------------------------------------------------------
    letteralist = []
    lettera_set = ""
    articlelett = Article.objects.all().order_by('pagina_book')
    for art in articlelett:
        article_lett = []
        if lettera_set != art.pagina_book[:1]:
            lettera_set = art.pagina_book[:1]
            lettera_set_title = art.title[:15] + " ..."
            article_lett += [lettera_set]
            article_lett += [lettera_set_title]
            letteralist = letteralist + [article_lett]

# ---------------------------------------------------------
    for art in articlelist:
        art.pseudo = art.book

        art.authore = ""
        authors = Article.objects.get(id=art.id).author.all()  # ManyToMany Tutti Authors per Article !!!!!!!!!!!!!
        for auth in authors:
            if auth.nome[0] != "-" and auth.padrenome[0] != "-":
                art.authore = art.authore + auth.cognome + "\xa0" + auth.nome[:1]  + ".\xa0"+ auth.padrenome[:1]  + "., "
            elif auth.nome[0] != "-" and auth.padrenome[0] == "-":
                art.authore = art.authore + auth.cognome + "\xa0" + auth.nome[:1]  + "., "
            else:
                art.authore = art.authore + auth.cognome  + ", "
        art.authore = art.authore[:-2]
        art.author_id = authors[0].id

        book = Book.objects.get(pseudonym=art.book)
        art.id_book = book.id
        books = BookBook.objects.all().filter(book=art.book)
        if books and art.summary != "Assente":
            art.content = "1"
        else:
            art.content = "0"


# ---------------------------------------------------------

    booklist = Book.objects.all()
    num_book = Book.objects.all().count()

    for book in booklist:
        book.num_article_book = Article.objects.all().filter(book = book.id).count()

    if lettera == "0": lettera = ""
    else: lettera = "( " + lettera + " )"
# ------------------------------------------------------------
    return render(
        request,
        'article_list.html',
        context={'articlelist': articlelist, 'booklist': booklist, 'nome_book': nome_book,
                 'num_article': num_article, 'num_book': num_book,
                 'letteralist': letteralist,
                 'tytle_nome': 'Статті', 'right_text': "Статті",
                 'right_fon': 'img_background/Chiesa_Gievka_3.jpg',
                 'right_text': "Статей",
                 'book': book, 'lettera': lettera,
                                        }
    )
# ============== END Article_list =======================

# ============== ARTICLE_DETAIL =============================
def article_detail(request, id_article,):

    article = Article.objects.get(id=id_article)

    nome_parole = article.title.split(" ")
    article_nome = ""
    for i in range(0, len(nome_parole)):
        if (len(article_nome) + len(nome_parole[i]) ) < 50 :
            article_nome = article_nome + " " + nome_parole[i]
        else: break
    if len(article.title) > 50:
        article_nome = article_nome + " ..."

    book = Book.objects.get(pseudonym = article.book)
    book_img = str(book.image_title)
    book_img = book_img[book_img.find("static") + 7:]
    book_id = book.id

# -------------------------article_detail Authors---------------------
    authors_list = Article.objects.get(id=id_article).author.all()  # ManyToMany Tutti Authors per Article !!!!!!!!!!!!!
    for auth in authors_list:
        if auth.nome[0] != "-" and auth.padrenome[0] != "-":
            auth.authore = auth.cognome + "\xa0" + auth.nome[:1]  + ".\xa0"+ auth.padrenome[:1]  + "."
        elif auth.nome[0] != "-" and auth.padrenome[0] == "-":
            auth.authore = auth.cognome + "\xa0" + auth.nome[:1]  + "."
        else:
            auth.authore = auth.cognome

# -------------------------article_detail Genres---------------------
    genres_list = Article.objects.get(id=id_article).genre.all()  # ManyToMany Tutti Genres per Article !!!!!!!!!!!!!
    for gen in genres_list:
        gen.alfabet = "thema_list"
        if gen.thema == "Особа":
            gen.alfabet = "nome_list"
        if gen.thema == "Місце":
            gen.alfabet = "citta_list"

# -------------------------article_detail ArticleBook---------------------
    books = BookBook.objects.all().filter(book=book_id)
    if books and article.summary == "Assente":
        article.content = "1"
    else:
        article.content = "0"
    if books:
        book_content = "1"
    else:
        book_content = "0"
    for pag in books:
        pagina_art = pag.pagina[pag.pagina.find(" ") + 1:]
        pag.num = pagina_art
        pag.pag_corte = int(pagina_art[:3])
        pag.path = str(pag.image_pag)
        pag.path = pag.path[pag.path.find("static") + 7:]

    pag_book_prima = int(article.pagina)
    if int(pag_book_prima / 2) * 2 < pag_book_prima:
        pag_book_prima = pag_book_prima - 1
    pag_book_ultima = int(article.pagina + article.num_pag-1)
    if int(pag_book_ultima / 2) * 2 < pag_book_ultima:
        pag_book_ultima = pag_book_ultima - 1

    pagine_list = []
    for pag in books:
        if pag.pag_corte < pag_book_prima or pag.pag_corte > pag_book_ultima:
            pass
        else:
            pagine_list = pagine_list + [pag]

# ------------------------------------------------------------
    return render(
        request,
        'article_detail.html',
        context={'article': article, 'pagine_list': pagine_list,
                 'article_nome': article_nome,
                 'authors_list': authors_list, 'genres_list': genres_list,
                 'tytle_nome': 'Стаття', 'right_text': "Стаття",
                 'book_content': book_content, 'book_pk': book_id,
                 'book_img': book_img,
                 'nome_parole': nome_parole,
                                        }
    )
# ============== END Article_detail =======================

# ============== AUTHOR_LIST =============================
def author_list(request, lettera, rating):

    if lettera == "0":
        authorlist = Author.objects.all()
        num_author = Author.objects.all().count()
        authorlettera = authorlist
        tytle_nome = ""

    if lettera == "100":
        authorlist = Author.objects.all()[:100]
        num_author = Author.objects.all().count()
        authorlettera = Author.objects.all()
        tytle_nome = ""

    if lettera != "0" and lettera != "100":
        authorlist = Author.objects.all().filter(cognome__startswith = lettera)
        num_author = Author.objects.all().filter(cognome__startswith = lettera).count()
        authorlettera = authorlist
        tytle_nome = "( " + lettera + " )"

#-----------------------------------------------
    for auth in authorlist:
        if auth.nome == "-" and auth.padrenome == "-":
            auth.nomepadre = ""  # 1 nome
        if auth.nome != "-" and auth.padrenome == "-":
            auth.nomepadre = auth.nome  # 1 nome
        if auth.nome != "-" and auth.padrenome != "-":
            auth.nomepadre = auth.nome + "\xa0" + auth.padrenome




    letteralist = []
    lettera_set = ""
    for auth in authorlettera:
        auth_lett = []
        if lettera_set != auth.cognome[:1]:
            lettera_set = auth.cognome[:1]
            lettera_set_cognome = auth.cognome + " ..."
            auth_lett += [lettera_set]
            auth_lett += [lettera_set_cognome]
            letteralist = letteralist + [auth_lett]


    for auth in authorlist:
        auth.num_article = Article.objects.all().filter(author=auth.id).count()

# ------------------------------------------
    return render(
        request,
        'author_list.html',
        context={'authorlist': authorlist, 'letteralist': letteralist,
                 'num_author': num_author,
                 'tytle_nome': tytle_nome,
                 'right_fon': 'img_background/Chiesa_Gievka_3.jpg',
                 'right_text': "Авторів",

                                        }
    )
# ============== END Author_list =======================

# ============== AUTHOR_DETAIL =============================
def author_detail(request, pk):

    author = Author.objects.get(pk = pk)
    foto_img = str(author.foto)
    foto_img = foto_img[foto_img.find("static") + 7:]
# ----------------------------------------
    author_articles = Article.objects.all().filter(author = pk).order_by("-data")
    for art in author_articles:
        books = BookBook.objects.all().filter(book = art.book)
        if books and art.summary != "Assente":
            art.content = "1"
        book = Book.objects.get(pseudonym = art.book)
        art.id_book = book.id
# ----------------------------------------
    authorlist = Author.objects.all()
    num_author = Author.objects.all().count()
    tytle_nome = ""

    letteralist = []
    lettera_set = ""
    for auth in authorlist:
        auth_lett = []
        if lettera_set != auth.cognome[:1]:
            lettera_set = auth.cognome[:1]
            lettera_set_cognome = auth.cognome + " ..."
            auth_lett += [lettera_set]
            auth_lett += [lettera_set_cognome]
            letteralist = letteralist + [auth_lett]


# ------------------------------------------
    return render(
        request,
        'author_detail.html',
        context={'author': author, 'author_articles': author_articles,
                 'foto': foto_img,
                 'letteralist': letteralist,
                 'num_author': num_author,
                 'tytle_nome': tytle_nome,
                 'right_fon': 'img_background/Chiesa_Gievka_3.jpg',
                 'right_text': "Авторів",

                                        }
    )
# ============== END Author_detail =======================

# ============== AUTHOR_RATING =============================
def author_rating(request,):

    # authorlist = Author.objects.all().exclude(cognome = "Редакційна колегія")
    # num_author = Author.objects.all().count()
    #
    # for auth in authorlist:
    #     article_author = Article.objects.all().filter(author = auth.id).count()
    #     auth.num_art = article_author       # 1 articles
    #     auth.save(update_fields=["num_art"])

    authorlist = Author.objects.all().exclude(cognome="Редакційна колегія").filter(num_art__gt = 2)

    # for auth in authorlist:
    #     num_pagine = 0
    #     num_images = 0
    #     article_author = Article.objects.all().filter(author = auth.id)
    #     for art in article_author:
    #         num_pagine += art.num_pag/art.num_aut
    #         num_images += art.num_img/art.num_aut
    #     auth.num_pag = int(num_pagine)        # 2 pagine
    #     auth.save(update_fields=["num_pag"])
    #     auth.num_img = int(num_images)        # 3 images
    #     auth.save(update_fields=["num_img"])
    #     auth.posto = int(0)

    authorlist = authorlist.order_by('-num_art', '-num_pag', '-num_img', )

    rating = []
    num_author = 0
    for auth in authorlist:
        if auth.num_art != 0 and auth.num_art != 1:
            num_author += 1
            auth.rating = num_author
            auth.save(update_fields=["rating"])
            rating = rating + [auth]



    return render(
        request,
        'rating.html',
        context={'rating': rating, 'authorlist': authorlist,
                 'num_author': num_author,
                 'right_fon': 'img_background/Chiesa_Gievka_3.jpg',
                 'right_text': "Авторів",

                                        }
    )
# ============== END Author_rating =======================



