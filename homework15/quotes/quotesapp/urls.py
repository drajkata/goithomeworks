from django.urls import path
from . import views

app_name = 'quotesapp'

urlpatterns = [
    path('', views.main, name='main'),
    path('author/', views.author, name='author'),
    path('quote/', views.quote, name='quote'),
    path('tag/', views.tag, name='tag'),
    path('detailQuote/<int:quote_id>', views.detailQuote, name='detailQuote'),
    path('detailAuthor/<int:author_id>', views.detailAuthor, name='detailAuthor'),
]
