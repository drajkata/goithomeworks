from django.shortcuts import render, redirect, get_object_or_404
from .forms import TagForm, AuthorForm, QuoteForm
from .models import Tag, Author, Quote
from django.contrib import messages

# Create your views here.
def main(request):
    quote = Quote.objects.all()
    return render(request, 'quotesapp/index.html', {"quote" : quote})

def detailQuote(request, quote_id):
    quote = get_object_or_404(Quote, pk=quote_id)
    return render(request, 'quotesapp/detailQuote.html', {"quote" : quote})

def detailAuthor(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    return render(request, 'quotesapp/detailAuthor.html', {"author" : author})

def tag(request):
    if request.user.is_authenticated == False:
        messages.error(request, 'You don\'t have permission to manage tags.')
        return redirect(to='quotesapp:main')

    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quotesapp:main')
        else:
            return render(request, 'quotesapp/tag.html', {'form': form})
    return render(request, 'quotesapp/tag.html', {'form': TagForm()})

def author(request):
    if request.user.is_authenticated == False:
            messages.error(request, 'You don\'t have permission to manage authors.')
            return redirect(to='quotesapp:main')

    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quotesapp:main')
        else:
            return render(request, 'quotesapp/author.html', {'form': form})
    return render(request, 'quotesapp/author.html', {'form': AuthorForm()})

def quote(request):
    if request.user.is_authenticated == False:
        messages.error(request, 'You don\'t have permission to manage quotes.')
        return redirect(to='quotesapp:main')

    tags = Tag.objects.all()
    author = Author.objects.all()
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            new_quote = form.save(commit=False)
            new_quote.author = Author.objects.get(fullname=request.POST["author"])
            new_quote.save()
            choice_tags = Tag.objects.filter(name__in=request.POST.getlist('tags'))
            for tag in choice_tags.iterator():
                new_quote.tags.add(tag)
            return redirect(to='quotesapp:main')
        else:
            return render(request, 'quotesapp/quote.html', {"tags": tags, "author": author, 'form': form})
    return render(request, 'quotesapp/quote.html', {"tags": tags, "author": author, 'form': QuoteForm()})