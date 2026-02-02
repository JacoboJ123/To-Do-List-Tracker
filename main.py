# to do list add, view, remove
def add_task():
    add_task = input("Enter your task.\n")
    user_task.append(add_task)
    print("Task has been added.\n")


def view_task():
    if not user_task:
        print("There are no current tasks.\n\n")
    else:
        for i, task in enumerate(user_task, 1):
            print(f"{i}. {task}")


def edit_task():
    if not user_task:
        print("There are no current tasks to edit.\n\n")
        return
    else:
        for i, task in enumerate(user_task, 1):
            print(f"{i}. {task}")
        try:
            edit_num = int(input("Pick which task you would like to edit\n"))
            if edit_num < 1 or edit_num > len(user_task):
                print("Task number out of range.\n")
                return
            new_task = input("Enter your edits\n")
            user_task[edit_num - 1] = new_task
            print("Task has been updated\n")
        except ValueError:
            print("Please enter a valid task number!\n")
            return


def save_task():
    with open("tasks.txt", "w") as file:
        for i in user_task:
            file.write(i + "\n")


def load_task():
    try:
        with open("tasks.txt", "r") as file:
            user_task.clear()
            lines = file.readlines()
            for line in lines:
                user_task.append(line.strip())
    except FileNotFoundError:
        pass


def delete_task():
    if not user_task:
        print("There are no tasks to delete\n\n")
        return
    for i, task in enumerate(user_task, 1):
        print(f"{i}. {task}")
    try:
        delete_num = int(input("Please choose a task to delete\n"))
        if delete_num < 1 or delete_num > len(user_task):
            print("Task number out of range.\n")
            return
        user_task.pop(delete_num - 1)
        print("Task was deleted.\n")
    except ValueError:
        print("Please enter a valid task number!\n")
        return


user_task = []
load_task()

while True:
    user_options = input(
        "\nHello, what would you like to do today?\nPlease pick an option to proceed!\n"
        "'A' to add a new task\n"
        "'V' to view your current tasks\n"
        "'E' to edit a task\n"
        "'D' to delete a task\n"
        "'Q' to quit.\n"
    ).upper()

    if user_options == "A":
        add_task()
        save_task()
    elif user_options == "V":
        view_task()
    elif user_options == "D":
        delete_task()
        save_task()
    elif user_options == "E":
        edit_task()
        save_task()
    elif user_options == "Q":
        print("Thank you and see you next time!")
        exit()
