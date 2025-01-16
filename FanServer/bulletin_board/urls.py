from django.urls import path
from .views import ArticleList, ArticleDetail, ArticleCreate, ArticleUpdate, ArticleDelete, subscriptions, ConfirmUser


urlpatterns = [
    path('', ArticleList.as_view(), name='article_list'),
    path('<int:pk>', ArticleDetail.as_view(), name='article_detail'),
    path('create/', ArticleCreate.as_view(), name='article_create'),
    path('<int:pk>/update/', ArticleUpdate.as_view(), name='article_update'),
    path('<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
    path('subscriptions/', subscriptions, name='subscriptions'),
    path('confirm/', ConfirmUser.as_view(), name='confirm_user'),
]