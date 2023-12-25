############################################################################      
### ERROR HANDLING

class ContactNotFound(Exception):
    pass

def input_error(func):
    def wrapper(*args):
        try:
            return func(*args)
        except ContactNotFound as e:
            print(f"Contact not found.")
        # except Exception as e:
        #     print(f"Error caught: {e} in function {func.__name__} with values {args}")

    return wrapper

def check_value(value):
    if value is None:
        return ""
    return value

@input_error
def pretty_view_contacts(data: dict):
    if data:
        pattern_headline = "| {:^5}| {:<25}| {:<15}| {:<30}| {:<15}| {:<60}|"
        pattern_body = "| {:^5}| {:<25}| {:<15}| {:<30}| {:<15}| {:<60}|"
        print("\n{:^163}".format("-" * 163))
        print(pattern_headline.format("Id", "Name ^", "Phone", "Email", "Birthday", "Address"))
        print("{:^163}".format("-" * 163))
        for key, obj in sorted(data.items(), key=lambda x: x[1].name):
            print(pattern_body.format(
                key,
                check_value(obj.name), 
                check_value(obj.phone), 
                check_value(obj.email), 
                check_value(obj.birthday), 
                check_value(obj.address),
                ))
    else:
        raise ContactNotFound

@input_error
def pretty_view_notes(data: dict):
    if data:
        pattern_headline = "| {:^5}| {:<25}| {:<15}| {:<109}|"
        pattern_body = "| {:^5}| {:<25}| {:<15}| {:<109}|"
        print("\n{:^163}".format("-" * 163))
        print(pattern_headline.format("Id", "Name ^", "Tag", "Notes"))
        print("{:^163}".format("-" * 163))
        for key, obj in sorted(data.items(), key=lambda x: x[1].name):
            print(pattern_body.format(
                key,
                check_value(obj.name), 
                check_value(obj.tag),
                check_value(obj.notes),
                ))
    else:
        raise ContactNotFound