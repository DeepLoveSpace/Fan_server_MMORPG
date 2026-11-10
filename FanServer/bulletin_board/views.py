from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Article, UserResponse, Category
from .forms import ArticleForm, ResponseForm
from .models import Subscription
from django.contrib.auth.decorators import login_required

# 1. Главная страница (список всех объявлений)
class ArticleListView(ListView):
    model = Article
    template_name = 'bulletin_board/article_list.html'
    context_object_name = 'articles'
    paginate_by = 5 # по 5 объявлений на страницу

    def get_queryset(self):
        queryset = Article.objects.all().order_by('-article_time')
        # Фильтрация по категории (если выбрана в меню)
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category__name=category)
        return queryset

# 2. Страница одного объявления (с формой отклика)
class ArticleDetailView(DetailView):
    model = Article
    template_name = 'bulletin_board/article_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем форму для отклика в контекст
        context['form'] = ResponseForm()
        # Добавляем отклики к этому объявлению
        context['responses'] = self.object.responses.all().order_by('-created_at')
        return context

    def post(self, request, *args, **kwargs):
        # Обработка отправки формы отклика
        self.object = self.get_object()
        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.article = self.object
            response.author = request.user
            response.save()
            return redirect('article_detail', pk=self.object.pk)
        return self.render_to_response(self.get_context_data(form=form))

# 3. Создание объявления (только для авторизованных)
class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'bulletin_board/article_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# 4. Редактирование объявления (только автор)
class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'bulletin_board/article_form.html'

    def test_func(self):
        # Проверяем, что текущий юзер - автор
        return self.get_object().author == self.request.user

# 5. Удаление объявления (только автор)
class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    success_url = reverse_lazy('article_list')
    template_name = 'bulletin_board/article_confirm_delete.html'

    def test_func(self):
        return self.get_object().author == self.request.user

# 6. Личный кабинет (приватная страница с откликами)
def my_responses(request):
    # Берем все отклики на объявления текущего пользователя
    responses = UserResponse.objects.filter(article__author=request.user).select_related('article', 'author')
    
    # Фильтр по конкретному объявлению (как в ТЗ)
    article_id = request.GET.get('article')
    if article_id:
        responses = responses.filter(article_id=article_id)
        
    # Все объявления юзера для выпадающего списка в фильтре
    user_articles = Article.objects.filter(author=request.user)

    return render(request, 'bulletin_board/my_responses.html', {
        'responses': responses,
        'user_articles': user_articles,
        'selected_article': article_id
    })

# 7. Принять отклик
def accept_response(request, pk):
    response = get_object_or_404(UserResponse, pk=pk)
    # Проверяем права: только автор объявления может принять отклик
    if request.user == response.article.author:
        response.status = True
        response.save()
    return redirect('my_responses')

# 8. Удалить отклик
def delete_response(request, pk):
    response = get_object_or_404(UserResponse, pk=pk)
    if request.user == response.article.author:
        response.delete()
    return redirect('my_responses')

@login_required
def toggle_subscription(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    sub, created = Subscription.objects.get_or_create(user=request.user, category=category)
    if not created:
        sub.delete() # Если уже подписан - отписываем
    return redirect('article_list')