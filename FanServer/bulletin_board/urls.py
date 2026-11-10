from django.urls import path
from . import views

urlpatterns = [
    # Список всех объявлений
    path('', views.ArticleListView.as_view(), name='article_list'),
    
    # Создание объявления
    path('create/', views.ArticleCreateView.as_view(), name='article_create'),
    
    # Детальная страница (просмотр)
    path('<int:pk>/', views.ArticleDetailView.as_view(), name='article_detail'),
    
    # Редактирование и удаление
    path('<int:pk>/update/', views.ArticleUpdateView.as_view(), name='article_update'),
    path('<int:pk>/delete/', views.ArticleDeleteView.as_view(), name='article_delete'),
    
    # Личный кабинет (приватная страница с откликами)
    path('my-responses/', views.my_responses, name='my_responses'),
    
    # Действия с откликами
    path('response/<int:pk>/accept/', views.accept_response, name='accept_response'),
    path('response/<int:pk>/delete/', views.delete_response, name='delete_response'),
    path('subscribe/<int:category_id>/', views.toggle_subscription, name='toggle_subscription'),
]