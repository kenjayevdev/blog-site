from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import CreateView
from posts.models import Post, BookReview
from posts.forms import BookReviewForm
from hitcount.models import HitCount
from hitcount.views import HitCountMixin
from django.contrib import messages
from django.http import HttpResponse


class BooksView(View):
    def get(self, request):
        books = Post.published.all().order_by('-id')
        search_query = request.GET.get('q', '')
        if search_query:
            books = books.filter(title__icontains=search_query)

        page_size = request.GET.get('page_size', 6)
        paginator = Paginator(books, page_size)

        page_num = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_num)

        return render(
            request,
            "posts/list.html",
            {"page_obj": page_obj, "search_query": search_query}
        )


class BookDetailView(View):
    def get(self, request, id):
        book = get_object_or_404(Post, id=id)
        review_form = BookReviewForm()

        # Hit count logic
        hit_count = HitCount.objects.get_for_object(book)
        HitCountMixin.hit_count(request, hit_count)

        return render(request, "posts/detail.html", {"book": book, "review_form": review_form})

class AddReviewView(LoginRequiredMixin, View):
    def post(self, request, id):
        book = get_object_or_404(Post, id=id)
        review_form = BookReviewForm(data=request.POST)

        if review_form.is_valid():
            BookReview.objects.create(
                book=book,
                user=request.user,
                stars_given=review_form.cleaned_data['stars_given'],
                comment=review_form.cleaned_data['comment']
            )

            return redirect(reverse("books:detail", kwargs={"id": book.id}))

        return render(request, "posts/detail.html", {"book": book, "review_form": review_form})


class EditReviewView(LoginRequiredMixin, View):
    def get(self, request, book_id, review_id):
        book = Post.objects.get(id=book_id)
        review = book.bookreview_set.get(id=review_id)
        review_form = BookReviewForm(instance=review)

        return render(request, "posts/edit_review.html", {"book": book, "review": review, "review_form": review_form})

    def post(self, request, book_id, review_id):
        book = Post.objects.get(id=book_id)
        review = book.bookreview_set.get(id=review_id)
        review_form = BookReviewForm(instance=review, data=request.POST)

        if review_form.is_valid():
            review_form.save()
            return redirect(reverse("books:detail", kwargs={"id": book.id}))

        return render(request, "posts/edit_review.html", {"book": book, "review": review, "review_form": review_form})


class ConfirmDeleteReviewView(LoginRequiredMixin, View):
    def get(self, request, book_id, review_id):
        book = Post.objects.get(id=book_id)
        review = book.bookreview_set.get(id=review_id)

        return render(request, "posts/confirm_delete_review.html", {"book": book, "review": review})


class DeleteReviewView(LoginRequiredMixin, View):
    def get(self, request, book_id, review_id):
        book = Post.objects.get(id=book_id)
        review = book.bookreview_set.get(id=review_id)

        review.delete()
        messages.success(request, "You have successfully deleted this review")

        return redirect(reverse("books:detail", kwargs={"id": book.id}))

class NewsCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = "posts/news_create.html"
    fields = ('title', 'description', 'cover_picture')


