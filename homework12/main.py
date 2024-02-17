from variables import NUMBER_LECTURERS, NUMBER_GROUPS, NUMBER_STUDENTS, NUMBER_ASSESSMENTS_PER_STUDENT, SUBJECTS_LIST, QUERY_DICT
from fill_data_groups import create_groups
from fill_data_students import create_students
from fill_data_lecturers import create_lecturers
from fill_data_subjects import create_subjects
from fill_data_assessments import create_assessments

def fill_tables():
    create_groups(NUMBER_GROUPS)
    create_students(NUMBER_STUDENTS)
    create_lecturers(NUMBER_LECTURERS)
    create_subjects(SUBJECTS_LIST)
    create_assessments(NUMBER_ASSESSMENTS_PER_STUDENT)

if __name__ == '__main__':
    seeding = input("\nDo you want to fill tables with fake data? [Y/N] ")
    if seeding in ["Y", "y", "yes", "Yes"]:
        fill_tables()
    while(True):
        choice = input("\nEnter number of guery: ")
        if choice in QUERY_DICT.keys():
            print(f"\n{QUERY_DICT[choice][1]}\n")
            for tuple in QUERY_DICT[choice][0]():
                print(tuple)
        elif choice.lower() in ["end", "exit", "."]:
            print("\nGood bye!\n")
            break
        else:
            print("\nYou have entered an incorrect inquiry number. Enter a value from 1 to 10.")
        print("\nTo exit the program, enter 'end', 'exit' or '.'\n")
