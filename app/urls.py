from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'app'
urlpatterns = [
    path('', views.index, name='index'),
    path('shops', views.shops_list, name='shops_list'),
    path('shops/<str:category>/', views.photos_category, name='photos_category'),
   # path('shops/<str:category>/', views.shops_detail, name='shops_detail'),
    path('posts', views.posts_list, name='posts_list'),
    path('mypage', views.mypage, name='mypage'),
    path('mypage/edit', views.mypage_edit, name='mypage_edit'),
    path('users/<int:pk>/', views.users_detail, name='users_detail'),
    path('photos/new/', views.photos_new, name='photos_new'),
    path('photos/<int:pk>/', views.photos_detail, name='photos_detail'),
    path('photos/<int:pk>/delete/', views.photos_delete, name='photos_delete'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_change/', views.PasswordChange.as_view(), name='password_change'),
    path('password_change/done/', views.PasswordChangeDone.as_view(), name='password_change_done'),
    #path(r'^(?P<photo_id>[0-9]+)/like/$', views.like, name='like'),
]