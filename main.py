"""
Author: G van der Biezen
File name: main.py

The following app after logging in lets the user use a few functions.
A teacher can view a reportcard, view grades and update grades. A student
can only view his or her own reportcard. It uses a database to store a
nd read data.

Python versie: 3.10.6
IDE: IntelliJ IDEA Community Edition 2022.1.4
Last update: 13/09/2022
"""

import menu
import authentication
from get_functions import *


db = sqlite3.connect("school.db")
cursor = db.cursor()


# cosmetics/display functions
def column_string_length(rows):
    """ Checks each column for the length of the data and stores the
    max length in a list.

    :return: a list with the max length for each column."""
    len_rows = len(rows)
    len_items = len(rows[0])
    len_list = [0 for _ in range(len_items)]
    # compare the length for each line en store the max length.
    for x in range(len_rows):
        for y in range(len_items):
            item = rows[x][y]
            if len(str(item)) + 4 > len_list[y]:
                len_list[y] = len(str(item)) + 4  # +4 is tab size
    return len_list


def print_format(row, number="off", head="off"):
    """ Prints the columns from tuples in a list neatly spaced. With the
     option the add sequential numbers in the front and or displaying the
     column headers. """
    padding = column_string_length(row)
    # display a list of tuples neatly
    numbering = 0
    for items in row:
        string = ''
        numbering += 1
        if row.index(items) == 0:
            numbering = 0
            if head == "off":
                continue
        for x in items:
            i = items.index(x)
            if x is None:  # if the element is type None
                blank = '-'
                num = f"{numbering:<1}."
                string += f'{blank:<{(padding[i])}}'
            elif row.index(items) == 0:  # header
                num = f"{' ':<1} "
                string += f'{items[i]:<{(padding[i])}}'
            else:
                num = f"{numbering:<1}."
                string += f'{items[i]:<{(padding[i])}}'
        if number == "on":
            print(num, string)
        else:
            print(string)
    print()


def display_class_info():
    """ Displays info chosen by the user for all classes or a chosen class.
     Returns the data list collected and the length of the data list."""
    class_name = grade_choose_classes()  # search by class name option
    # db search
    if class_name == '':
        rows = get_t_info(select='ClassName as Class, FullName as Student',
                          table='test_student')
        print_format(rows, number="on", head="on")
    else:
        rows = get_t_info(select='ClassName as Class, FullName as Student', where='ClassName',
                          table='test_student', target=class_name)
        print_format(rows, number="on", head="on")
    return rows, len(rows)


# view grades
def grade_choose_trimester():
    """ Error handeling using conditions. Looping until the user input
    is valid.
    :return: a valid trimester code.
    """
    trim_codes = ('t1', 't2', 't3')
    valid_choice = False
    while valid_choice is not True:
        choice_trimester = input("Choose trimester. Enter T1, T2 or T3: ").lower()
        if choice_trimester not in trim_codes:
            print("Not a valid trimester. Please try again! ")
        else:
            valid_choice = True  # stop evaluation and proceed
            return choice_trimester


def grade_choose_subject():
    """ Error handeling using conditions. Looping until the user input
    is valid.
    :return: a valid subject code.
    """
    valid_choice = False
    while valid_choice is not True:
        subject = (input("Enter a subject or press Enter for all: ")).upper()
        subject_info = get_subjects()  # exam. [(1, NE, Nederlands), ...]
        subject_list = [x[1] for x in subject_info]  # get second items
        if subject != '' and subject not in subject_list:
            print("Not a valid subject. Please try again ")
        else:
            valid_choice = True  # stop evaluation and proceed
            return subject


def grade_choose_classes():
    """ Error handeling using conditions. Looping until the user input
    is valid.
    :return: a valid class name.
    """
    valid_choice = False
    while valid_choice is not True:
        classes = (input("Enter a class or press Enter for all: ")).upper()
        classes_info = get_classes()  # exam. [(221A, 1A, 13), ...]
        classes_list = [x[1] for x in classes_info]  # get second items
        if classes != '' and classes not in classes_list:
            print("Not a valid class. Please try again ")
        else:
            valid_choice = True  # stop evaluation and proceed
            return classes


def choose_student(max_len):
    """ Error handeling using conditions. Looping until the user input
    is valid. Checks if the user choice is valid after the display of a list.
    :return: a valid student choice.
    """
    valid_choice = False
    while valid_choice is not True:
        student_choice = input("Choose student: ")
        if student_choice.isdigit() is False or int(student_choice) >= max_len or int(student_choice) == 0:
            print("Not a valid choice. Please try again! ")
        else:
            valid_choice = True  # stop evaluation and proceed
            return student_choice


def grade_input_check():
    """ Error handeling using conditions. Looping until the user input
    is valid.
    :return: a valid grade format.('digit' or 'digit.digit')
    """
    valid_choice = False
    while valid_choice is not True:
        grade_input = input()
        if len(grade_input) == 1 and grade_input.isdigit() \
                and int(grade_input) >= 1:
            valid_choice = True
            return grade_input
        elif len(grade_input) == 3 and grade_input[1] == '.' \
                and (grade_input[0].isdigit() == grade_input[2].isdigit()) \
                and int(grade_input[0]) >= 1:
            valid_choice = True
            return grade_input
        else:
            print(f"{grade_input} is not a correct grade format."
                  f" Please try again: ", end='')


def view_grades_all(trimester):
    """ Gets all the grades' data for the chosen trimester and displays it. """
    row = get_t_info(table='all_grades_' + trimester + '_2022')
    print_format(row, head='on')


def grade_display_results(trimester, classes, subject):
    """ Error handeling using conditional expression and display the chosen data.
    :param trimester: a valid trimester code.
    :param classes: a valid class name.
    :param subject: a valid subject code.
    :return: the results.
    """
    print("Trimester:", trimester.upper())
    if classes == '' and subject == '':
        view_grades_all(trimester)
    elif classes == '':
        row = get_t_info(select=f'{subject}', table='all_grades_' + trimester + '_2022')
        print(*[x[0] for x in row if x[0] is not None], sep='\n')
    elif subject == '':
        row = get_t_info(select='*', table='all_grades_' + trimester + '_2022',
                         where='Class', target=f'{classes}')
        print_format(row, head='on')
    else:
        row = get_t_info(select=f'{subject}', table='all_grades_' + trimester + '_2022',
                         where='Class', target=f'{classes}')
        print(*[x[0] for x in row if x[0] is not None], sep='\n')


def view_grade():
    """ Main function to view grades. """
    choice_trimester = grade_choose_trimester()
    choice_class = grade_choose_classes()
    choice_subject = grade_choose_subject()
    print()
    grade_display_results(choice_trimester, choice_class, choice_subject)


# update grades
def set_grade(id_student):
    """ Sets the grade for a student. Prompting for the subject and grade.
    Loops if the user chooses to update another grade."""
    trimester = grade_choose_trimester()
    loop = "on"
    while loop == "on":
        # choose subject and grade
        subject = input("Choose a subject: ")
        subject = subject.upper()
        subject_data = get_subjects()
        subject_list = [x[1] for x in subject_data]
        if subject in subject_list:
            print(f"Enter a grade for {subject}: ", end='')
            cijfer = grade_input_check()
            # update grade
            cursor.execute(f"UPDATE grades_{trimester}_2022 SET {subject} = '{cijfer}'"
                           f" WHERE student_id = {id_student} ")
            db.commit()  # confirm the changes in the database.
            # update another subject?
            choice = input("Continue updating? Y or N: ")
            if choice == 'Y' or choice == 'y':
                print()
                continue
            else:
                print()
                loop = "off"
        else:
            print(f"{subject} is not a valid subject.")


def update_grade():
    """ Main function to update a grade. Displays the result if successful."""
    print("--------- Grading ------------- ")
    rows, max_choice = display_class_info()
    student = choose_student(max_choice)  # check choice input
    choice = rows[int(student)]
    name_student = choice[1]
    student_id = get_reg_id_fullname(name_student)  # get id number
    print(f'Name: {name_student}')
    print_report(student_id)
    set_grade(student_id)  # update grade
    print(f'Name: {name_student}')
    print_report(student_id)  # update the user with the changes made.


def view_reportcard_id():
    valid_id = False
    while valid_id is not True:
        try:
            student_id = int(input("Enter Student Id: "))
            cursor.execute(f"SELECT regID FROM student_registry")
            row = cursor.fetchall()
            stu_id_list = [x[0] for x in row]
            if student_id in stu_id_list:
                name_student = get_fullname_from_regid(student_id)
                print(f'Name: {name_student}')
                print_report(student_id)
                valid_id = True
            else:
                print("Not a valid student id.")
        except TypeError:
            print("Not a valid student id.")


def view_reportcard_class():
    """Display the reportcard for a student by choosing a class. """
    rows, max_choice = display_class_info()
    student = choose_student(max_choice)  # check choice input
    choice = rows[int(student)]
    name_student = choice[1]
    student_id = get_reg_id_fullname(name_student)  # get id number
    print()
    print(f'Name: {name_student}')
    print_report(student_id)


def view_my_reportcard(mail):
    """ Displays the reportcard for the student. When logged in the function
    uses the email to get the id and print the reportcard. """
    try:
        cursor.execute(f"SELECT regID FROM student_registry WHERE Email = '{mail}' ")
        row = cursor.fetchone()
        id_student = row[0]
        name_student = get_fullname_from_regid(id_student)
        print(f'Name: {name_student}')
        print_report(id_student)
    except TypeError:
        print("Student email not found in student registry.")


def view_reportcard():
    """ Main function to view reportcard. Gives the user two options to search
    and view a reportcard. """
    valid_choice = True
    while valid_choice:
        search_choice = input("Search by 1. Student Id  or 2. Class: ")
        if search_choice == '1':
            view_reportcard_id()
            valid_choice = False
        elif search_choice == '2':
            view_reportcard_class()
            valid_choice = False
        else:
            print("Please enter a valid option 1 or 2.")


def print_report(id_student):
    """ Display a student's reportcard by getting the grades from
      the database and printing it a viewable format."""

    trim_list = ['t1', 't2', 't3']
    grades_list = []
    # fetch the student's grades from the database
    data = cursor.execute("SELECT * FROM grades_t1_2022")
    for trim in trim_list:
        cursor.execute(f"SELECT * FROM grades_{trim}_2022 WHERE student_id = {id_student} ")
        row = cursor.fetchone()
        grades_list.append(row)
    # print data
    x = 0
    print('  \t\tT1 \t\tT2 \t\tT3')
    for column in data.description:
        if x == 0 or x == 1:
            x += 1
        else:
            print(column[0], float(grades_list[0][x]), float(grades_list[1][x]),
                  float(grades_list[2][x]), sep='\t\t', end='\n')
            x += 1
    print()


def run_main():
    """ Main function to start the app. Prompts for log in and then proceeds to
    show menu options for either teacher or student."""
    credentials = authentication.login()
    if authentication.auth_server(*credentials):
        email, _ = credentials
        lvl = authentication.auth_level(email)
        menu.menu_auth(lvl, email)


if __name__ == '__main__':
    run_main()

    # --- menu functions
    # update_grade()
    # view_grade()
    # view_reportcard()
    # view_my_reportcard("Teacher")

    cursor.close()
    db.close()
