# menu files
from main import *

# menu lists
teacher_menu = [["View Report Card", view_reportcard],
                ["View Grades", view_grade],
                ["Update Grades", update_grade]
                ]

student_menu = [["View Reportcard", view_my_reportcard],
                ]


# menu functions
def display_menu(options: list):
    print(f"\033[4m" + "Menu" + "\033[0m")
    for index, optie in enumerate(options):
        print(f'{index + 1}: {optie[0]}')
    print("0: Exit")
    print("-" * 20)


def menu_auth(lvl, mail):
    session_email = mail
    if lvl == 'TE':
        main = teacher_menu
    else:
        main = student_menu
    while True:
        try:
            # print("session is", session_email)
            display_menu(main)
            menu_choice = input("Choose an option: ")
            x = int(menu_choice)
            print()
            if x == 0:
                break
            elif main[x - 1][0] == "View Reportcard":  # student menu
                main[x - 1][1](session_email)
            else:
                main[x - 1][1]()  # run function
                input("Press enter to continue...")
        except (IndexError, ValueError):
            print("Not a valid option.")


if __name__ == '__main__':
    pass
    # menus(main_menu)
