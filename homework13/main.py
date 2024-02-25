import connect_me
from models import Author, Quote, Tag
from seeds import seed_mongo_db

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

COMMAND_SEARCH_DICT = {
    "name" : show_quotes_of_name,
    "tag" : show_quotes_of_tag,
    "tags" : show_quotes_of_tags,
}

COMMAND_GENERAL_DICT = {
    "show all authors" : show_all_authors,
    "show all quotes" : show_all_quates,
    "exit" : exit,
    "." : exit,
}

def main():
    choice = input("Do you want to fill mongo database with data? ")
    if choice in ["y", "Y", "Yes", "yes"]:
        seed_mongo_db() 
    while True:
        print("\nEnter your command to search quotes. You can use command like 'name', 'tag', 'tags' or exit to close the program. Please enter your query using this template: 'command:value'.")
        user_input = input("Enter your query here: ")
        value = ""
        input_splitted = []
        input_splitted = user_input.split(":")
        command = input_splitted[0]
        if command in COMMAND_SEARCH_DICT.keys():
            if len(input_splitted) > 1:
                value = input_splitted[1]
                if len(value) == 0:
                    print("You have not provided any value. Please, try again.")
                    print('------------------')
                    continue
                value_list = value.split(",")
                values = []
                for val in value_list:
                    values.append(val.strip())
                COMMAND_SEARCH_DICT[command](values)
            else:
                print("You have not provided any value. Please, try again.")
                print('------------------')
        elif command in COMMAND_GENERAL_DICT.keys():
            COMMAND_GENERAL_DICT[command]()
        else:
            print("Sorry, I don't understand your command. Please, try again.")
            print('------------------')


if __name__ == '__main__':
    main()