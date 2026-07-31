import sqlite3
import datetime
from db_setup import create_table

def add_task():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    title_task = input("Enter your task: ").strip()
    task_description = input("Enter the task description (or press Enter to skip): ").strip()
    if task_description == "":
        task_description = None
    cursor.execute("INSERT INTO tasks(title, description) VALUES(?, ?)", (title_task, task_description))
    conn.commit()
    conn.close()
    print("Task has been added.\n")


def view_task():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    task_view = cursor.fetchall()
    if not task_view:
        print("Empty table")
    else:
        for i, task in enumerate(task_view, 1):
            task_id, title, description, created_at, enddate, streak, last_completed = task
            line = f"{i}. {title}"
            if description:
                line += f" Desc: {description}."
            if created_at:
                line += f" Created: {created_at}"
            if enddate:
                line += f" Due: {enddate}"
            if streak:
                line+= f" Streak: {streak}"
            if last_completed:
                line += f" {last_completed}"
            print(line)
    conn.close()


def edit_task():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("SELECT task_id, title, description FROM tasks")
    task_view = cursor.fetchall()
    task_ids = []
    if not task_view:
        print("There are no current tasks to edit.\n\n")
        return
    else:
        for task in task_view:
            task_id, title, description = task
            line = f"{task[0]}. {title}"
            if description:
                line += f" Desc: {description}."
            print(line)
            task_ids.append(task[0])
        try:
            edit_num = int(input("Enter the integer task you would like to edit\n"))
            if edit_num < 1 or edit_num not in task_ids:
                print("Task number out of range.\n")
                return
            # need to add a check to either update title or desc based on user input (below)
            edit_title = input("Enter your title edit(s) (Press enter to skip): ")
            edit_desc = input("Enter yout description edit(s) (Press enter to skip): ")
            update, values = [], []
            if edit_title != "":
                update.append("title = ?")
                values.append(edit_title)
            if edit_desc != "":
               update.append("description = ?")
               values.append(edit_desc)
            if not update:
               print("Nothing to update")
               return
            query_on = ", ".join(update)
            cursor.execute(f"UPDATE tasks set {query_on} WHERE task_id = ?", (*values, edit_num))
            conn.commit()
            print("Task has been updated\n")
        except ValueError:
            print("Please enter a valid task number!\n")
        finally:
            conn.close()


def delete_task():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    task_view = cursor.fetchall()
    task_ids = []
    if not task_view:
        print("There are no tasks to delete\n\n")
        return
    else:
        for task in task_view:
            print(f"{task[0]}. {task[1]}")
            task_ids.append(task[0])
        try:
            delete_num = int(input("Please choose a task to delete:\n"))
            if delete_num < 1 or delete_num not in task_ids:
                print("Task number out of range.\n")
                return
            cursor.execute("DELETE FROM tasks WHERE task_id = ?", (delete_num,))
            conn.commit()
            print("Task was deleted.\n")
        except ValueError:
            print("Please enter a valid task number!\n")
        finally:
            conn.close()

def complete_task():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    task_view = cursor.fetchall()
    task_ids = []
    if not task_view:
        print("Empty table")
        return
    else:
        for task in task_view:
            print(f"{task[0]}. {task[1]}")
            task_ids.append(task[0])
        try:
            complete = int(input("Enter a task # you would like to mark as complete: "))
            if complete not in task_ids:
                print("Int out of range")
                return
            cursor.execute("SELECT last_completed FROM tasks WHERE task_id = ?", (complete,))
            last_complete = cursor.fetchone()
            today = datetime.date.today()
            time = today.isoformat()
            if last_complete[0] is None:
                cursor.execute("UPDATE tasks SET streak = 1, last_completed = ? WHERE task_id = ?", (time, complete, ))
                conn.commit()
                print("Completed Streak is now 1 keep it up!")
                return
            last_date = datetime.date.fromisoformat(last_complete[0])
            days_apart = (today - last_date).days
            if days_apart == 0:
                print("Task already completed, no Streak change")
            elif days_apart == 1:
                cursor.execute("SELECT streak FROM tasks WHERE task_id = ?", (complete,))
                row = cursor.fetchone()
                streak_count = row[0] + 1
                cursor.execute("UPDATE tasks SET streak = ?, last_completed = ? WHERE task_id = ?", ( streak_count, time, complete, ))
                conn.commit()
                print(f"Task marked completed. Streak count: {streak_count}")
            else:
                cursor.execute("UPDATE tasks SET streak = 1, last_completed = ? WHERE task_id = ?", (time, complete,))
                conn.commit()
                print("Your streak was broken")
        except ValueError:
            print("Please enter a valid task number.")
        finally:
            conn.close()

create_table()

while True:
    user_options = input(
        "\nHello, what would you like to do today?\nPlease pick an option to proceed!\n"
        "'A' to add a new task\n"
        "'V' to view your current tasks\n"
        "'E' to edit a task\n"
        "'C' to mark a task complete\n"
        "'D' to delete a task\n"
        "'Q' to quit.\n"
    ).upper()

    if user_options == "A":
        add_task()
    elif user_options == "V":
        view_task()
    elif user_options == "D":
        delete_task()
    elif user_options == "E":
        edit_task()
    elif user_options == "C":
        complete_task()
    elif user_options == "Q":
        print("Thank you and see you next time!")
        exit()