from django.urls import path
from . import views

app_name = 'quotesapp'

urlpatterns = [
    path('', views.main, name='main'),
    path('author/', views.author, name='author'),
    path('quote/', views.quote, name='quote'),
    path('tag/', views.tag, name='tag'),
    path('detailQuote/<int:quote_id>', views.detail_quote, name='detail_quote'),
    path('detailAuthor/<int:author_id>', views.detail_author, name='detail_author'),
    path('import_data/', views.import_data, name='import_data'),
]
