import logging
import tkinter as tk
import tkinter.messagebox as msg
import tkinter.ttk as ttk

import ui
import ui.staff
import ui.student
from data_tables import data_handling
from processes import password_logic


class Welcome(ui.GenericPage):
    # The first page the user sees
    # The welcome landing page where they can select their login type (student/staff)

    page_name = 'Welcome'

    def __init__(self, pager_frame: ui.PagedMainFrame):
        super().__init__(pager_frame=pager_frame)

        self.message = ttk.Label(self,
                                 text='Welcome to the\n'
                                      'DofE Scheme Management Application.\n\n'
                                      'Please select your login type:',
                                 justify='center',
                                 font=ui.BOLD_CAPTION_FONT)
        self.message.grid(row=0, column=0, columnspan=2, padx=self.padx, pady=self.pady)

        # button calls the change_to_page method of the pager_frame to change view to StudentLogin
        self.student_login = ttk.Button(self,
                                        text='Student Login',
                                        command=lambda:
                                        self.pager_frame.change_to_page(StudentLogin))
        self.student_login.grid(row=1, column=0, padx=self.padx, pady=self.pady)

        # button calls the change_to_page method of the pager_frame to change view to StaffLogin
        self.staff_login = ttk.Button(self,
                                      text='Staff Login',
                                      command=lambda:
                                      self.pager_frame.change_to_page(StaffLogin))
        self.staff_login.grid(row=1, column=1, padx=self.padx, pady=self.pady)


class Login(ui.GenericPage):
    # Set by child classes.
    # Determines where the user is directed to on a successful login.
    is_student: bool

    def __init__(self, pager_frame: ui.PagedMainFrame):
        """
        The base class for the login page objects of StudentLogin and StaffLogin.
        Allows the user to return back to the landing screen
        or enter their username and password in order to access each respective system.
        """
        super().__init__(pager_frame=pager_frame)

        self.back_button = ttk.Button(self, text='Back',
                                      command=self.page_back)
        self.back_button.grid(row=0, column=0, padx=self.padx, pady=self.pady, sticky='w')

        self.user_type_label = ttk.Label(self,
                                         text=f'{"Student" if self.is_student else "Staff"} Login',
                                         font=ui.HEADING_FONT)
        self.user_type_label.grid(row=1, column=0, columnspan=2, padx=self.padx, pady=self.pady)

        if self.is_student:
            login_message = 'These will be given to you by your teacher.'
        else:
            login_message = 'Contact your system administrator to create a new account.'

        self.message = ttk.Label(
            self,
            text=f'Please enter your username and password.\nBoth are case sensitive.\n\n{login_message}',
            justify='center', font=ui.ITALIC_CAPTION_FONT
        )
        self.message.grid(row=2, column=0, columnspan=2, padx=self.padx, pady=self.pady)

        self.user_detail_frame = ttk.Frame(self)
        self.user_detail_frame.grid(row=3, column=0, columnspan=2, pady=self.pady)

        self.username_label = ttk.Label(self.user_detail_frame, text='Username:', justify='right')
        self.username_label.grid(row=0, column=0, pady=self.pady, sticky='e')

        self.username_var = tk.StringVar()
        self.username_entry = ttk.Entry(self.user_detail_frame, textvariable=self.username_var)
        self.username_entry.grid(row=0, column=1, columnspan=2, pady=self.pady, sticky='we')

        self.password_label = ttk.Label(self.user_detail_frame, text='Password:', justify='right')
        self.password_label.grid(row=1, column=0, pady=self.pady, sticky='e')

        self.password_entry = ui.PasswordEntryFrame(self.user_detail_frame)
        self.password_entry.grid(row=1, column=1, pady=self.pady, sticky='e')

        self.login_button = ttk.Button(self, text='Login', command=self.login)
        self.login_button.grid(row=4, column=1, padx=self.padx, pady=self.pady, sticky='e')

    def login(self):
        """
        Gets user's input and verifies their login details.
        Automatically advances application to appropriate page
        (for student or for staff member)
        """
        input_username = self.username_var.get()
        input_password = self.password_entry.get()

        db = self.pager_frame.master_root.db  # gets database obj from main root of application
        user_type = ('Staff', 'Student')[int(self.is_student)]
        logging.debug(f'A {user_type.lower()} user attempted to log in with username "{input_username}"')

        if user_type == 'Staff':
            # noinspection PyTypeChecker
            login_table_obj: data_handling.StaffTable = db.get_table_by_name('StaffTable')
        else:  # is Student
            # noinspection PyTypeChecker
            login_table_obj: data_handling.StudentLoginTable = db.get_table_by_name('StudentLoginTable')

        if input_username in login_table_obj.row_dict.keys():  # if username is valid, verifies pwd
            login_obj = login_table_obj.row_dict[input_username]
            if password_logic.verify_pwd_str(input_password, login_obj.password_hash):
                logging.info(f'Username "{input_username}" '
                             f'successfully logged into {user_type.lower()} application')

                if user_type == 'Staff':
                    self.pager_frame.change_to_page(
                        destination_page=ui.staff.StudentOverview,
                        staff=login_obj
                    )

                elif user_type == 'Student':
                    # noinspection PyUnresolvedReferences
                    user_id = login_obj.student_id

                    # noinspection PyTypeChecker
                    # gets Student obj specified by logged in username
                    logged_in_student: data_handling.Student = db.get_table_by_name('StudentTable').row_dict[user_id]

                    # changes page appropriately, providing StudentAwardDashboard
                    # frame with the Student obj information to update text
                    self.pager_frame.change_to_page(
                        destination_page=ui.student.StudentAwardDashboard,
                        student=logged_in_student,
                        username=input_username,
                    )

                return  # ends function so error below is not displayed

        msg.showerror('Login Failed', 'Username and/or password incorrect.\n'
                                      'Make sure you are on the correct login page')

    def page_back(self):
        """
        Returns the user back to the Welcome page after resetting the pwd visibility
        """
        self.password_entry.hide_password()
        self.pager_frame.change_to_page(Welcome)


class StudentLogin(Login):
    """
    The login page modified for students
    """
    page_name = 'Student Login'
    is_student = True


class StaffLogin(Login):
    """
    The login page modified for staff
    """
    page_name = 'Staff Login'
    is_student = False
