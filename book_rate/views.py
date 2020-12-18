import json
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.postgres import serializers
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render
from utils.comute_score import fresh
from book_rate.models import Book, Rate, User


# Create your views here.


def index(request, flag: bool = False):
    context = {"recent_books": recent(request, flag=True), "popular_books": popular(request, flag=True)}
    if flag:
        return context
    else:
        return render(request, "book_rate/index.html", context)


def popular(request, flag: bool = False):
    if flag:
        popular_books = Book.objects.all().order_by("-mean_score")[:5]
        return popular_books
    else:
        context = {"popular_book": Book.objects.all().order_by("-mean_score")[:10]}
        return render(request, "book_rate/popular.html", context)


def recent(request, flag: bool = False):
    """
        if flag is True, means call from index
    """
    if flag:
        recent_add_books = Book.objects.order_by("-add_date")[:5]
        return recent_add_books
    else:

        recent_add_books = Book.objects.order_by("-add_date")[:10]
        context = {"recent_add": recent_add_books}
        return render(request, "book_rate/recent.html", context)


def add_rate(request, user_id):
    try:
        user = User.objects.get(user_id=user_id)
        book = Book.objects.get(isbn=request.POST["isbn"])
        rate = Rate.objects.filter(user=user, book=book)
        if len(rate) == 0:
            # 增加新评分
            new_rate = Rate.objects.create(user=user, book=book, score=int(request.POST["new_score"]))
        else:
            # 修改新评分
            rate[0].score = int(request.POST["new_score"])
            rate[0].save()
        fresh()
        context = {"status": 1}
        return HttpResponse(json.dumps(context), content_type="application/type")
    except Exception as e:
        print("add_rate:", e)
        raise Exception


def list_rate(request, user_id):
    context = {}
    user = User.objects.get(user_id=user_id)
    score = Rate.objects.filter(user=user)
    book = Book.objects.filter(isbn__in=score.values("book"))
    return render(request, "book_rate/profile.html", context)


def alter_rate(request, user_id):
    context = {}
    try:
        rate = Rate.objects.get(user=user_id, book=request.POST["isbn"])
        rate.score = request.POST["new_score"]
        rate.save()
        fresh()
        context["flag"] = 1
    except ObjectDoesNotExist as e:
        context["flag"] = 0
    return HttpResponse(json.dumps(context), content_type="application/type")


def delete_rate(request, user_id):
    context = {}
    try:
        rate = Rate.objects.get(user=user_id, book=request.POST["isbn"])
        rate.delete()
        fresh()
        context["flag"] = 1
    except ObjectDoesNotExist as e:
        context["flag"] = 0
    return HttpResponse(json.dumps(context), content_type="application/type")


def signup(request):
    return render(request, "book_rate/signup.html")


def signup_process(request):
    if request.POST:
        req = request.POST
        name = req["name"]
        location = req["location"]
        password = req["password"]
        age = req["age"]
        context = {}
        user = User.objects.filter(name=name)
        if len(user) > 0:
            if user[0].password == password:
                context["flag"] = 0
                context["user_id"] = user[0].user_id
            else:
                context["flag"] = -1
        else:
            context["flag"] = 1
            new_user = User.objects.create(name=name, location=location, password=password, age=age)
            context["user_id"] = new_user.user_id
        return HttpResponse(json.dumps(context), content_type="application/type")


def login_success(request, user_id):
    user = User.objects.get(user_id=user_id)
    context = {"flag": True, "user_id": user.user_id, "user_name": user.name}
    context2 = index(request, flag=True)
    context["recent_books"] = context2["recent_books"]
    context["popular_books"] = context2["popular_books"]
    return render(request, "book_rate/index.html", context)


def login(request):
    return render(request, "book_rate/login.html")


def login_process(request):
    context = {}
    try:
        user = User.objects.get(name=request.POST["name"])
        if user.password == request.POST["password"]:
            context["flag"] = 1
            context["user_id"] = user.user_id
        else:
            context["flag"] = 0
    except ObjectDoesNotExist as e:
        context["flag"] = -1
    return HttpResponse(json.dumps(context), content_type="application/type")


def search(request, user_id=None):
    if user_id is None:
        return render(request, "book_rate/search.html")
    else:
        return render(request, "book_rate/search.html",
                      {"flag": True, "user_name": User.objects.get(user_id=user_id).name})

    # def rate(request):
    #     return render(request, "book_rate/rate.html")


def search_return(request, user_id=None):
    # ToDo 加入读取13/10位isbn号
    # 可能有 isbn title author publisher published_date add_date
    req = request.POST
    search_id = str(req["context"])
    if "isbn_type" == req["type"]:
        res = Book.objects.filter(isbn=search_id)

    elif "pubdate_type" == req["type"]:
        res = Book.objects.filter(year_of_publication=search_id)[:20]

    elif "author_type" == req["type"]:
        res = Book.objects.filter(author=search_id)

    elif "date_type" == req["type"]:
        res = Book.objects.filter(add_date=search_id)[:20]

    else:
        res = Book.objects.filter(title=search_id)[:20]
    # ToDo 加入读取多页的问题
    # ToDo 加入时间区间搜索
    scores = []
    for book in res:
        try:
            rate = Rate.objects.get(user=User.objects.get(user_id=user_id), book=book)
            scores.append(rate.score)
        except Exception as e:
            scores.append("暂无评分")
    json_context = serializers.serialize("json", res)
    context = {"res": json_context, "user_id": user_id, "scores": scores}
    return HttpResponse(json.dumps(context), content_type="application/type")


def show_rate(request, user_id):
    user = User.objects.get(user_id=user_id)
    user_rates = Rate.objects.filter(user=user)
    context = {"name": user.name, "rates": user_rates}
    return render(request, "book_rate/my_rate.html", context=context)


def book_detail(request, book_id):
    context = {"book": Book.objects.get(isbn=book_id)}
    return render(request, "book_rate/book_detail.html", context)
