import os
import django
import time
import re
import pandas as pd
import numpy as np
import requests
import isbn
import functools

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "course_project.settings")
django.setup()


def gb_search(isbn_id):
    url = f"https://www.googleapis.com/books/v1/volumes?q=isbn%3D{isbn_id}"
    proxies = {"http": "http://127.0.0.1:12333", "https": "http://127.0.0.1:12333"}
    response = hget(url, proxies=proxies)
    if response.status_code != 200:
        raise Exception
    res = response.json()
    if "items" not in res.keys():
        return -1
    else:
        return res["items"][0]["volumeInfo"]["publishedDate"]


def db_search(isbn_id):
    url = f"https://book.feelyou.top/isbn/{isbn_id}"
    response = hget(url)
    if response.status_code != 200:
        raise Exception
    res = response.json()
    if "book_info" not in res.keys():
        return -1
    else:
        item = res["book_info"]
        if "出版年" not in item.keys():
            return -1
        return item["出版年"].split("-")[0]


def rectify(isbn_id):
    print("*" * 100)
    if len(isbn_id) == 10:
        new_isbn_id = isbn.ISBN(isbn_id).isbn13()
        print(f"{isbn_id} to {new_isbn_id}")
        isbn_id = new_isbn_id
    # patten = "<p><strong>Published:</strong>(.*)</p>"
    correct_year_db = db_search(isbn_id)
    if correct_year_db != -1:
        return correct_year_db
    correct_year_gb = gb_search(isbn_id)
    if correct_year_gb != -1:
        return correct_year_gb
    print(f"Error in {isbn_id}")


def preprocess(which, modifiable=False):
    if which == "books":
        patten = "\"(.*)\";\"(.*)\";\"(.*)\";\"(.*)\";\"(.*)\";\"(.*)\";\".*\";\".*\""
        data_headers = ["isbn", "title", "author", "year_of_publication", "publisher", "image_url"]
        file = open("../data/BX-Books.csv", encoding="ISO-8859-1").readlines()
    elif which == "users":
        patten = "\".*\";\"(.*)\";\"*(.*)\"*"
        # TODO 正则匹配存在多出一个引号的问题
        data_headers = ["Location", "Age"]
        file = open("../data/BX-Users.csv", encoding="ISO-8859-1").readlines()
    elif which == "rate":
        patten = "\"(.*)\";\"(.*)\";\"(.*)\""
        data_headers = ["user_id", "book", "score"]
        file = open("../data/BX-Book-Ratings.csv", encoding="ISO-8859-1").readlines()
    else:
        raise Exception("which param is error")
    file = file[1:]  # ignore header
    # length2 = len(file)
    length2 = 5000  # TODO 只使用部分数据
    data_dict = {}

    for ite in range(len(data_headers)):
        data_dict[data_headers[ite]] = list()
    for ite in range(length2):
        re_res = re.findall(patten, file[ite])
        if len(re_res) <= 0:
            print(f"error: index: {ite} context: {file[ite]}")
            raise Exception

        data_ite = list(re_res[0])
        if ite % 1000 == 0:
            print(f"[{ite}/{length2}] loading")
        for ite2 in range(len(data_headers)):
            if which == "users" and data_headers[ite2] == "Age":
                if data_ite[ite2] == "NULL":
                    data_ite[ite2] = -1
                else:
                    age = int(data_ite[ite2].split('"')[0])
                    if age > 119:
                        data_ite[ite2] = 119  # TODO 加了年龄上限
                    else:
                        data_ite[ite2] = age
            if which == "rate":
                if data_headers[ite2] == "score" or data_headers[ite2] == "user_id":
                    data_ite[ite2] = int(data_ite[ite2])

            data_dict[data_headers[ite2]].append(data_ite[ite2])
    data_df = pd.DataFrame(data_dict)

    if which == "books":
        print(set(data_df["year_of_publication"]))  # 存在异常值
        if modifiable:
            years = np.array(data_df["year_of_publication"]).astype(np.int)
            now_year = int(time.strftime("%Y", time.localtime()))
            abnormal_data = data_df[(years > now_year) | (years == 0)]  # |
            error_items = []
            for j in range(len(abnormal_data)):
                ab_data = abnormal_data.iloc[j]
                recent_value = ab_data[3]
                correct_year = rectify(ab_data[0])
                if correct_year is None:
                    error_items.append(j)
                    ab_data[3] = "unknown"
                    continue
                ab_data[3] = correct_year
                time.sleep(0.1)
                print(f"change {recent_value} to {ab_data[3]}")
    elif which == "users":
        print(set(data_df["Age"]))
    elif which == "rate":
        print(len(set(data_df["user_id"])), len(set(data_df["book"])))
    else:
        raise Exception("which param is error")
    return data_df


if __name__ == "__main__":
    from book_rate.models import Book, User, Rate

    book_header = ["isbn", "title", "author", "year_of_publication", "publisher", "image_url", "add_date"]
    user_header = ["location", "age", "add_date"]
    rate_header = ["user", "book", "score", "add_date"]
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 "
                      "Safari/537.36"}
    hget = functools.partial(requests.get, headers=headers)
    # data = preprocess(which="rate", modifiable=False)
    subject = "users"
    data = preprocess(which=subject, modifiable=False)
    length = len(data)
    count = 0
    for i in range(length):
        item = data.iloc[i].to_list()
        item.append(time.strftime("%Y-%m-%d", time.localtime()))

        if subject == "books":
            item_dt = dict(zip(book_header, item))
            Book.objects.create(**item_dt)

        elif subject == "users":
            item_dt = dict(zip(user_header, item))
            User.objects.create(**item_dt)

        elif subject == "rate":
            try:

                book = Book.objects.get(isbn=item[1])
                user = User.objects.get(pk=item[0])
                new_item = [user, book, item[2], item[-1]]
                item_dt = dict(zip(rate_header, new_item))
                Rate.objects.create(**item_dt)
                count += 1
                if count == 1000:
                    break
            except BaseException as e:
                print(e)
                pass
            else:
                pass
        if i % 1000 == 0:
            print(f"[{i}/{length}] loading")
    print(count)
