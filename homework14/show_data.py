from models import Author, Quote

def show_all_authors():
    print('\n--- All authors ---')
    authors = Author.objects()
    for author in authors:
        print(f"Id: {author.id}\nFullname: {author.fullname}\nBorn date: {author.born_date}\nBorn location: {author.born_location}\nDescription: {author.description}")
        print('------------------')

def show_all_quates():
    print('\n--- All quotes ---')
    quotes = Quote.objects()
    for quote in quotes:
        tags = [tag.name for tag in quote.tags]
        author = quote.author.fullname
        print(f"Id: {quote.id}\nQuote: {quote.quote}\n Author: {author}\nTags: {tags}")
        print('------------------')

def show_quotes_of_name(value: list):
    _value = value[0]
    author_value = Author.objects(fullname=_value).first()
    if author_value:
        quotes = Quote.objects(author = author_value)
        if quotes:
            print(f"\n--- All quotes with name: {_value} ---")
            for quote in quotes:
                print(f"Quote: {quote.quote}")
            print('------------------')
        else:
            print(f"Sorry, I haven't found any quotes with name {value[0]}. Please, try again.")
            print('------------------')
    else:
        print(f"Sorry, I haven't found any quotes with name {value[0]}. Please, try again.")
        print('------------------')

def show_quotes_of_tag(value: list):
    _value = value[0]
    quotes = Quote.objects(tags__name = _value)
    if quotes:
        print(f"\n--- All quotes with tag: {_value} ---")
        for quote in quotes:
            print(f"Quote: {quote.quote} - {quote.author.fullname}")
        print('------------------')
    else:
        print(f"Sorry, I haven't found any quotes with tag {value[0]}. Please, try again.")
        print('------------------')

def show_quotes_of_tags(value: list):
    quotes = Quote.objects(tags__name__in = value)
    if quotes:
        print(f"\n--- All quotes with tags: {value} ---")
        for quote in quotes:
            print(f"Quote: {quote.quote} - {quote.author.fullname}")
        print('------------------')
    else:
        print(f"Sorry, I haven't found any quotes with tag {value}. Please, try again.")
        print('------------------')