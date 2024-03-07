from django.shortcuts import render, redirect
from .forms import TagForm, AuthorForm, QuoteForm
from .models import Tag, Author

# Create your views here.
def main(request):
    return render(request, 'quotesapp/index.html')

def tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quotesapp:main')
        else:
            return render(request, 'quotesapp/tag.html', {'form': form})
    return render(request, 'quotesapp/tag.html', {'form': TagForm()})

def author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quotesapp:main')
        else:
            return render(request, 'quotesapp/author.html', {'form': form})
    return render(request, 'quotesapp/author.html', {'form': AuthorForm()})

def quote(request):
    tags = Tag.objects.all()
    author = Author.objects.all()
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            new_quote = form.save(commit=False)
            choice_author = Author.objects.filter(name__in=request.POST.getlist('author'))
            new_quote.author.add(choice_author)
            # for aut in choice_author.iterator():
            #     new_quote.author.add(aut)
            choice_tags = Tag.objects.filter(name__in=request.POST.getlist('tags'))
            for tag in choice_tags.iterator():
                new_quote.tags.add(tag)
            new_quote.save()

            return redirect(to='quotesapp:main')
        else:
            return render(request, 'quotesapp/quote.html', {"tags": tags, "author": author, 'form': form})
    return render(request, 'quotesapp/quote.html', {"tags": tags, "author": author, 'form': QuoteForm()})