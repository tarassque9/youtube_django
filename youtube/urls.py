from django.urls import path
from .views import HomeView, NewVideo, LoginView, RegisterView, VideoView, CommentView, VideoFileView

urlpatterns = [
    path('index/', HomeView.as_view(), name='index'),
    path('new_video/', NewVideo.as_view(), name='newvideo'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('video/<int:id>', VideoView.as_view(), name='video'),
    path('comment/', CommentView.as_view(), name='comment'),
    path('get_video/<str:file_name>', VideoFileView.as_view())
]