from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User
from django.db.models import Exists, OuterRef
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from .forms import ArticleForm, UserResponseForm
from .models import Article, Category, Subscription
from datetime import datetime
from .filters import ArticleFilter

class ArticleList(ListView):
    model = Article
    ordering = 'article_time'
    template_name = 'articles.html'
    context_object_name = 'articles'
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = ArticleFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['filterset'] = self.filterset
        return context


class ArticleDetail(LoginRequiredMixin, DetailView):
    model = Article
    template_name = 'article.html'
    context_object_name = 'article'

    def post(self, request, *args, **kwargs):
        article = self.get_object()
        if self.request.method == 'POST':
            form = UserResponseForm(self.request.POST)
            if form.is_valid():
                userresponse = form.save(commit=False)
                userresponse.author = self.request.user
                userresponse.article_id = article.id
                userresponse.save()
                return redirect('article_detail', article.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = UserResponseForm()
        return context


class ArticleCreate(LoginRequiredMixin, CreateView):
    raise_exception = True
    permission_required = ('articles.add_article',)
    form_class = ArticleForm
    model = Article
    template_name = 'article_create.html'


    def form_valid(self, form):
        article = form.save(commit=False)
        article.author = self.request.user
        article.save()
        return super().form_valid(form)


class ArticleUpdate(LoginRequiredMixin, UpdateView):
    form_class = ArticleForm
    model = Article
    template_name = 'article_edit.html'
    context_object_name = 'article'


class ArticleDelete(LoginRequiredMixin, DeleteView):
    model = Article
    template_name = 'article_delete.html'
    success_url = reverse_lazy('article_list')


# настройка рассылки
@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscription.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscription.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscription.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('name')
    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )

class ConfirmUser(UpdateView):
    model = User
    context_object_name = 'confirm_user'

    def post(self, request, *args, **kwargs):
        if 'code' in request.POST:
            user = User.objects.filter(code=request.POST['code'])
            if user.exists():
                user.update(is_active=True)
                user.update(code=None)
            else:
                return render(self.request, 'users/invalid_code.html')
            return redirect('account_login')


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'articles.html'
