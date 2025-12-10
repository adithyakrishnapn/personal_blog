from django.urls import path
from .views import add_blog, home, show_blogs, view_blog, delete_blog, edit_blog, signup, login, logout


urlpatterns = [
    path('', home, name='home'),
    path('add/', add_blog, name='add_blog'),
    path('blog/<str:blog_id>/', view_blog, name='view_blog'),
    path('delete/<str:blog_id>/', delete_blog, name='delete_blog'),
    path('edit/<str:blog_id>/', edit_blog, name='edit_blog'),
    path('blogs/', show_blogs, name='show_blogs'),
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
]
