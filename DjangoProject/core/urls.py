from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from core import views

urlpatterns = [
    path('snippets/', views.SnippetList.as_view()),
    path('snippets/<int:pk>/', views.SnippetDetail.as_view()),
    path('snippets/<int:pk>/detect/', views.SnippetDetect.as_view()),
    path('snippets/detect/', views.SnippetDetect.as_view()),
    path('snippets/<int:pk>/reindent/', views.SnippetReindent.as_view()),
    path('snippets/reindent/', views.SnippetReindent.as_view()),
    path('snippets/<int:pk>/order/', views.SnippetOrderImport.as_view()),
    path('snippets/order/', views.SnippetOrderImport.as_view()),
    path('snippets/<int:pk>/pylint/', views.SnippetPylint.as_view()),
    path('snippets/pylint/', views.SnippetPylint.as_view()),
    path('snippets/<int:pk>/pyflakes/', views.SnippetPyflakes.as_view()),
    path('snippets/pyflakes/', views.SnippetPyflakes.as_view()),
    path('snippets/<int:pk>/flake8/', views.SnippetFlake8.as_view()),
    path('snippets/flake8/', views.SnippetFlake8.as_view()),
    path('snippets/<int:pk>/mypy/', views.SnippetMypy.as_view()),
    path('snippets/mypy/', views.SnippetMypy.as_view()),
    path('snippets/<int:pk>/execute/', views.SnippetExecute.as_view()),
    path('snippets/execute/', views.SnippetExecute.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
