from django.urls import reverse
from django.test import TestCase
from posts.models import Post
from users.models import CustomUser


class BooksTestCase(TestCase):
    def test_no_books(self):
        response = self.client.get(reverse("books:list"))
        self.assertContains(response, "No posts found.")

    def test_books_list(self):
        book1 = Post.objects.create(title="book1", description="Desecription1")
        book2 = Post.objects.create(title="book2", description="Desecription2")
        book3 = Post.objects.create(title="book3", description="Desecription3")

        response = self.client.get(reverse("books:list") + "?page_size=2")


        for book in [book1, book2]:
            self.assertContains(response, book.title)

        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse("books:list") + "?page=2&page_size=2")

        self.assertContains(response, book3.title)

    def test_detail_page(self):
        book = Post.objects.create(title="book1", description="Desecription1")
        response = self.client.get(reverse("books:detail", kwargs={"id": book.id}))


        self.assertContains(response, book.title)
        self.assertContains(response, book.description)

    def test_search_books(self):
        book1 = Post.objects.create(title="book1", description="Desecription1")
        book2 = Post.objects.create(title="book2", description="Desecription2")
        book3 = Post.objects.create(title="book3", description="Desecription3")

        response = self.client.get(reverse("books:list") + "?q=book1")
        self.assertContains(response, book1.title)
        self.assertNotContains(response, book2.title)
        self.assertNotContains(response, book3.title)

class BookReviewTestCase(TestCase):
    def test_add_review(self):
        book = Post.objects.create(title="book1", description="Desecription1")
        user = CustomUser.objects.create(
            username="wolf", first_name="jasur", last_name="kenjayev", email="wolf@gmail.com"
        )

        user.set_password("22121948")
        user.save()

        self.client.login(username="wolf", password="22121948")

        self.client.post(reverse("books:reviews", kwargs={"id": book.id}), data={
            "stars_given": 4,
            "comment": "hi"
        })
        book_reviews = book.bookreview_set.all()

        self.assertEqual(book_reviews.count(), 1)
        self.assertEqual(book_reviews[0].stars_given, 4)
        self.assertEqual(book_reviews[0].comment, "hi")
        self.assertEqual(book_reviews[0].book, book)
        self.assertEqual(book_reviews[0].user, user)