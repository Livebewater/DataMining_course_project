import os
import django
from django.db.models import Avg
from sklearn.cluster import KMeans
import numpy as np

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "course_project.settings")
django.setup()


def fresh():
    from book_rate.models import Book, Rate
    max_score = Rate.objects.values_list("book").annotate(Avg("score")).order_by("-score__avg")
    for count, score in enumerate(max_score.all()):
        book = Book.objects.get(isbn=score[0])
        book.mean_score = score[1]
        book.save()


def k_means():
    from book_rate.models import Book
    model = KMeans(n_clusters=2)
    books = Book.objects.all()
    data = []
    authors = []
    publishers = []
    dates = np.unique(np.array(Book.objects.values_list("year_of_publication")).astype(np.int))
    # features: title, author-length, author-index, publisher-index, publish-date, mean-score

    for book in books:
        book_data = list()
        # title
        book_data.append(len(book.title))

        # author
        book_data.append(len(book.author))
        if book.author not in authors:
            authors.append(book.author)
            book_data.append(len(authors) - 1)
        else:
            book_data.append(authors.index(book.author))

        # publisher
        if book.publisher not in publishers:
            publishers.append(book.publisher)
            book_data.append(len(publishers) - 1)
        else:
            book_data.append(publishers.index(book.publisher))

            # publisher-date
        book_data.append(np.where(dates == int(book.year_of_publication))[0][0])

        # mean-score
        book_data.append(book.mean_score)
        book_data = np.array(book_data).reshape([-1, 1])
        data.append(book_data)

    data = np.concatenate(data, axis=1)
    data = np.transpose(data, [1, 0])

    KMeans()
    return data

# if __name__ == "__main__":
#     x = k_means()
#     kmeans = KMeans(n_clusters=2).fit(x)
