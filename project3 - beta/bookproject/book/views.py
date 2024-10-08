from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .models import Book, Review
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Avg

from django.core.paginator import Paginator
from .consts import ITEMS_PER_PAGE

class ListBookView(LoginRequiredMixin, ListView):                   #database使う時はListViewを使う
    template_name = 'book/book_list.html'
    model = Book                                #model = Book でBookモデルを使うことを指定している
    paginate_by = ITEMS_PER_PAGE
    
    
class DetailBookView(LoginRequiredMixin, DetailView):             #database使う時はDetailViewを使うがどのデータを使うか指定しないといけない     
    template_name = 'book/book_detail.html'
    model = Book
   

class CreateBookView(LoginRequiredMixin, CreateView):           #CreateViewはブラウザからデータベース使う時
    template_name = 'book/book_create.html'
    model = Book
    fields = ['title', 'text', 'category', 'thumbnail']  #fieldsはcreateで使うデータの種類を指定しないといけない
    success_url = reverse_lazy('list-book')  #reverse_lazyは成功したらどこに行くか指定する
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    
class DeleteBookView(LoginRequiredMixin, DeleteView):           #DeleteViewはデータベースからデータを消す時
    template_name = 'book/book_confirm_delete.html'
    model = Book
    success_url = reverse_lazy('list-book')  #成功したらどこに行くか指定する
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        
        if obj.user != self.request.user:
            raise PermissionDenied
        
        return obj
    
    
class UpdateBookView(LoginRequiredMixin, UpdateView):           #UpdateViewはデータベースのデータを更新する時
    model = Book
    template_name = 'book/book_update.html'
    fields = ['title', 'text', 'category', 'thumbnail']  
    # success_url = reverse_lazy('list-book')  #成功したらどこに行くか指定する
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not obj.user == self.request.user:
            raise PermissionDenied
        
        return obj
    
    def get_success_url(self):
        return reverse('detail-book', kwargs={'pk': self.object.id})
    
    
    
def index_view(request):                #functionバージョン
    object_list = Book.objects.order_by('-id')  #Bookモデルのデータを最新で並べ替える
    ranking_list = Book.objects.annotate(avg_rating=Avg('review__rate')).order_by('-avg_rating')[:3]
    
    paginator = Paginator(ranking_list, ITEMS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # query = request.GET('number')
    # print(query)
    
    return render(request, 'book/index.html', {'object_list': object_list, 'ranking_list': ranking_list, 'page_obj':page_obj})  #index.htmlを表示する

    

class CreateReviewView(LoginRequiredMixin, CreateView):           #CreateViewはブラウザからデータベース使う時
    model = Review
    fields = ['book','title', 'text', 'rate',]  #fieldsはcreateで使うデータの種類を指定しないといけない
    template_name = 'book/review_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book'] = Book.objects.get(pk=self.kwargs['book_id'])
        return context
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('detail-book', kwargs={'pk': self.object.book.id})  #成功したらどこに行くか指定する