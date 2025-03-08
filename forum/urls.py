from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from forum.views import (
    HomeView,
    
    QuestionListView,
    QuestionCreateView,
    QuestionDetailView,
    QuestionDeleteView,
    AnswerCreationView,
    CommentCreationView,
    
    QuestionVoteView,
    QuestionViewView,
    
    AnswerVoteView,
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('questions/', QuestionListView.as_view(), name='question-list'),
    path('questions/create/', QuestionCreateView.as_view(), name='question-create'),
    path('questions/detail/<int:pk>/', QuestionDetailView.as_view(), name='question-detail'),
    path('questions/delete/<int:pk>/', QuestionDeleteView.as_view(), name='question-delete'),
    path('questions/<int:pk>/answer/create', AnswerCreationView.as_view(), name='answer-create'),
    path('questions/<int:question_pk>/answer/<int:answer_pk>/comment/create', CommentCreationView.as_view(), name='comment-create'),
    
    path('question/vote', QuestionVoteView.as_view(), name='question-vote'),
    path('question/view', QuestionViewView.as_view(), name='question-view'),
    
    path('answer/vote/', AnswerVoteView.as_view(), name='answer-vote'),
    
    path('admin/', admin.site.urls),
    path('accounts/', include('users.urls')),
    
    path("__reload__/", include("django_browser_reload.urls")),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
