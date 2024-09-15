from django.shortcuts import render, redirect
from django.views import View
from portfolio.models import Portfolio
from django.core.paginator import Paginator

class PortfolioView(View):
    def get(self, request):
        books = Portfolio.objects.all().order_by('-id')
        page_size = request.GET.get('page_size', 3)
        paginator = Paginator(books, page_size)

        page_num = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_num)
        return render(
            request,
            "portfolio/list.html",
            {"page_obj": page_obj})
