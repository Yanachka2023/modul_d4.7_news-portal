from django.urls import path
from .views import PostList, PostDetail, multiply, PostSearch, PostCreate, PostUpdate, PostDelete # импортируем наше представление

urlpatterns = [

    path('multiply/', multiply),
    path('', PostList.as_view()),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('search/', PostSearch.as_view()),
    path('create/', PostCreate.as_view(), name = 'post_create'),
    path('<int:pk>/edit', PostUpdate.as_view(), name = 'post_edit'),
    path('<int:pk>/delete', PostDelete.as_view(), name = 'post_delete'),


]




