from django.contrib.admin.templatetags.admin_list import pagination
from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View
from posts.models import Post, BookReview


class HomeView(View):
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
            "home.html",
            {"page_obj": page_obj, "search_query": search_query}
        )

def about_page(request):
    return render(request, "about.html")