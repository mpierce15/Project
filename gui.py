from tkinter import *
from errors import *
from grades import *
import csv


class Gui:
    def __init__(self, window):
        """
        Initialize the user interface and data attributes.

        :param window: The main application window.
        :type window: tkinter.Tk
        """
        self.__window = window
        self.__assignment = ''

        self.frame_assignment = Frame(self.__window)
        self.label_assignment = Label(self.frame_assignment, text='Assignment Name')
        self.input_assignment = Entry(self.frame_assignment, width=15)
        self.label_assignment.pack(side='left')
        self.input_assignment.pack(padx=20, side='left')

        self.frame_submit = Frame(self.__window)
        self.button_submit = Button(self.frame_submit, text='SUBMIT', command=self.submit)
        self.button_submit.pack()

        self.frame_name = Frame(self.__window)
        self.label_name = Label(self.frame_name, text='Student Name')
        self.input_name = Entry(self.frame_name, width=15)
        self.label_name.pack(side='left')
        self.input_name.pack(padx=20, side='left')

        self.frame_score = Frame(self.__window)
        self.label_score = Label(self.frame_score, text='Score')
        self.input_score = Entry(self.frame_score, width=15)
        self.label_score.pack(side='left')
        self.input_score.pack(padx=71, side='left')

        self.frame_back = Frame(self.__window)
        self.button_back = Button(self.frame_back, text='BACK', command=self.back)
        self.button_back.pack()

        self.frame_add = Frame(self.__window)
        self.button_add = Button(self.frame_add, text='ADD', command=self.add)
        self.button_add.pack()

        self.frame_view = Frame(self.__window)
        self.button_view = Button(self.frame_view, text="VIEW", command=self.view)
        self.button_view.pack()

        self.frame_response = Frame(self.__window)
        self.label_response = Label(self.frame_response, text='Please fill out all values')
        self.label_response.pack()

        self.entry()

    def submit(self):
        """
        Stores the valid assignment name input.
        Creates a new CSV file for the assignment and prepares UI to enter
        student data.

        :return: None
        """
        try:
            self.__assignment = self.input_assignment.get().strip()
            if self.__assignment == '':
                raise EmptyName("Please enter assignment name")
        except EmptyName as e:
            self.label_response.config(text=f'{e}')
        else:
            self.__assignment = self.input_assignment.get().strip()

            with open(f'{self.__assignment}.csv', 'w') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(['Name', 'Score', 'Grade'])

            self.frame_assignment.pack_forget()
            self.frame_submit.pack_forget()
            self.frame_response.pack_forget()
            self.label_response.config(text="Please fill out all values")

            self.frame_name.pack(anchor='w', padx=10, pady=10)
            self.frame_score.pack(anchor='w', padx=10, pady=10)
            self.frame_response.pack(pady=30)
            self.frame_back.pack(side='left', padx=20)
            self.frame_add.pack(side='left', padx=50)
            self.frame_view.pack(side='right', padx=20)
            self.input_name.focus_set()

    def entry(self):
        """
        Prepares the UI for an entry. Ensures the assignment field is cleared.
        Focus is set on assignment input.

        :return: None
        """
        self.input_assignment.delete(0, END)
        self.label_response.config(text='Please fill out all values')

        self.frame_assignment.pack(anchor='w', padx=10, pady=30)
        self.frame_submit.pack(pady=10)
        self.frame_response.pack(pady=30)
        self.frame_submit.pack()
        self.input_assignment.focus_set()

    def back(self):
        """
        Hide current UI frames and go back to the assignment entry.

        :return: None
        """
        self.frame_name.pack_forget()
        self.frame_score.pack_forget()
        self.frame_response.pack_forget()
        self.frame_back.pack_forget()
        self.frame_add.pack_forget()
        self.frame_view.pack_forget()

        self.entry()

    def add(self):
        """
        Add a student's name, score, and grade to a CSV file.

        :return: None
        """
        try:
            name = self.input_name.get().strip()
            if name == '':
                raise EmptyName('Please enter student name')
            with open(f'{self.__assignment}.csv', 'r') as csv_file:
                content = csv.reader(csv_file, delimiter=',')
                for line in content:
                    if line[0].lower() == name.lower():
                        raise DuplicateValue('That name is already in the list, please enter a new name')
            score = float(self.input_score.get().strip())
            if score < 0:
                raise NegativeValue('Please enter a positive score')
            if score > 100:
                raise OutOfRange('Maximum score is 100')
        except ValueError:
            self.label_response.config(text='Please enter correct score value')
        except EmptyName as e:
            self.label_response.config(text=f'{e}')
        except DuplicateValue as e:
            self.label_response.config(text=f'{e}')
        except NegativeValue as e:
            self.label_response.config(text=f'{e}')
        except OutOfRange as e:
            self.label_response.config(text=f'{e}')

        else:
            grade = letter_grade(score)

            with open(f'{self.__assignment}.csv', 'a') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow([name, round(score, 2), grade])

            self.input_name.delete(0, END)
            self.input_score.delete(0, END)
            self.input_name.focus_set()
            self.label_response.config(text='Please fill out all values')

    def view(self):
        """
        Opens a new window to display grade information from a CSV file.
        Calculates and displays averages and letter grades for the scores.

        :return: None
        """
        window2 = Toplevel()
        window2.title("Grade Calculator")
        window2.geometry("450x500")

        scores = []
        row_count = 0

        with open(f'{self.__assignment}.csv', 'r') as csv_file:
            content = csv.reader(csv_file, delimiter=',')
            for r, col in enumerate(content):
                for c, row in enumerate(col):
                    if row =='Name':
                        Label(window2, width=13, height=2, text=row, font='default 15 bold').grid(row=r, column=c)
                    elif row == "Score":
                        Label(window2, width=13, height=2, text=row, font='default 15 bold').grid(row=r, column=c)
                    elif row == "Grade":
                        Label(window2, width=13, height=2, text=row, font='default 15 bold').grid(row=r, column=c)
                    else:
                        Label(window2, width=13, height=2, text=row).grid(row=r, column=c)
                    row_count +=1
        with open(f'{self.__assignment}.csv', 'r') as csv_file:
            content = csv.reader(csv_file, delimiter=',')
            for line in content:
                if line[1] == 'Score':
                    pass
                else:
                    scores.append(float(line[1]))
        Label(window2, text=f'Averages:', font='default 13 bold').grid(row=row_count+1, column=0, pady=20)
        Label(window2, text=f'{avg_score(scores):.2f}', font='default 13 bold').grid(row=row_count+1, column=1, pady=20)
        Label(window2, text=f'{letter_grade(avg_score(scores))}', font='default 13 bold').grid(row=row_count+1, column=2, pady=20)

        window2.mainloop()
