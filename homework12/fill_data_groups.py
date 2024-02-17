from connect_db import session
from models import Group
from variables import NUMBER_GROUPS

def generate_data(numbers) -> list:
    fake_groups = []
    for i in range(numbers):
        letter = 'ABCDEFGHIJKLMNOPQRSTUWYZ'
        template_name = f"2022/2023-{letter[i]}"
        fake_groups.append(template_name)
    return fake_groups

def create_data(data) -> None:
    for fake_group in data:
        group = Group(name=fake_group)
        session.add(group)
    session.commit()

def create_groups(numbers):
    create_data(generate_data(numbers))

if __name__ == '__main__':
    create_groups(NUMBER_GROUPS)