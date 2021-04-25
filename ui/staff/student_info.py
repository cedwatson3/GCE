import logging
import tkinter.messagebox as msg
import tkinter.ttk as ttk

import ui
from data_tables import data_handling
from processes import shorten_string
from processes.datetime_logic import datetime_to_str


class StudentInfo(ui.GenericPage):
    page_name = "'STUDENT_NAME' - Detail"

    def __init__(self, pager_frame: ui.PagedMainFrame):
        super().__init__(pager_frame=pager_frame)

        self.back_button = ttk.Button(self, text='Back', command=self.page_back)
        self.back_button.grid(row=0, column=0, columnspan=2, padx=self.padx, pady=self.pady)

        self.student_information_frame_top = ttk.Labelframe(self, text='Student Details')
        self.student_information_frame_top.grid(row=1, column=0, padx=self.padx, pady=self.pady)
        self.student_information_frame = ttk.Frame(self.student_information_frame_top)
        self.student_information_frame.pack()

        self.award_detail_frame_top = ttk.Labelframe(self, text='Award details')
        self.award_detail_frame_top.grid(row=1, column=1, padx=self.padx, pady=self.pady)
        self.award_detail_frame = ttk.Frame(self.award_detail_frame_top)
        self.award_detail_frame.pack()

        self.action_button_frame_top = ttk.Frame(self)
        self.action_button_frame_top.grid(row=2, column=0, columnspan=2, padx=self.padx, pady=self.pady)
        self.action_button_frame = ttk.Frame(self.action_button_frame_top)
        self.action_button_frame.pack()

        self.student = None
        self.staff_origin = None

    def update_attributes(self, clicked_name: str,
                          student: data_handling.Student,
                          staff_origin: data_handling.Staff) -> None:

        self.page_name = f"'{clicked_name}' - Detail"

        self.student = student
        self.staff_origin = staff_origin

        # clear variable frames and recreate
        self.student_information_frame.destroy()
        self.award_detail_frame.destroy()
        self.action_button_frame.destroy()

        self.student_information_frame = ttk.Frame(self.student_information_frame_top)
        self.student_information_frame.pack(padx=self.padx, pady=self.pady)
        self.award_detail_frame = ttk.Frame(self.award_detail_frame_top)
        self.award_detail_frame.pack(padx=self.padx, pady=self.pady)
        self.action_button_frame = ttk.Frame(self.action_button_frame_top)
        self.action_button_frame.pack(padx=self.padx, pady=self.pady)

        # the following details are always present for a student object
        user_id_label = ttk.Label(self.student_information_frame, text='User ID:')
        user_id_label.grid(row=0, column=0, padx=self.padx, pady=self.pady, sticky='e')
        user_id_val_label = ttk.Label(self.student_information_frame, text=str(self.student.student_id))
        user_id_val_label.grid(row=0, column=1, padx=self.padx, pady=self.pady, sticky='w')

        centre_id_label = ttk.Label(self.student_information_frame, text='Centre ID:')
        centre_id_label.grid(row=1, column=0, padx=self.padx, pady=self.pady, sticky='e')
        centre_id_val_label = ttk.Label(self.student_information_frame, text=str(self.student.centre_id))
        centre_id_val_label.grid(row=1, column=1, padx=self.padx, pady=self.pady, sticky='w')

        award_level_label = ttk.Label(self.student_information_frame, text='Award Level:')
        award_level_label.grid(row=2, column=0, padx=self.padx, pady=self.pady, sticky='e')
        award_level_val_label = ttk.Label(self.student_information_frame,
                                          text=self.student.award_level.capitalize())
        award_level_val_label.grid(row=2, column=1, padx=self.padx, pady=self.pady, sticky='w')

        year_group_label = ttk.Label(self.student_information_frame, text='Year group:')
        year_group_label.grid(row=3, column=0, padx=self.padx, pady=self.pady, sticky='e')
        year_group_val_label = ttk.Label(self.student_information_frame, text=self.student.year_group)
        year_group_val_label.grid(row=3, column=1, padx=self.padx, pady=self.pady, sticky='w')

        # populate student information frame with details and buttons depending on state of student enrollment
        no_activity_details_label = ttk.Label(self.award_detail_frame, text='None', font=ui.BOLD_CAPTION_FONT)
        if not self.student.fullname:
            no_activity_details_label.pack()

        else:
            fullname_label = ttk.Label(self.student_information_frame, text='Full name:')
            fullname_label.grid(row=0, column=2, padx=self.padx, pady=self.pady, sticky='e')
            fullname_val_label = ttk.Label(self.student_information_frame, text=self.student.fullname)
            fullname_val_label.grid(row=0, column=3, padx=self.padx, pady=self.pady, sticky='w')

            gender_label = ttk.Label(self.student_information_frame, text='Gender:')
            gender_label.grid(row=1, column=2, padx=self.padx, pady=self.pady, sticky='e')
            gender_val_label = ttk.Label(self.student_information_frame, text=self.student.gender.capitalize())
            gender_val_label.grid(row=1, column=3, padx=self.padx, pady=self.pady, sticky='w')

            date_of_birth_label = ttk.Label(self.student_information_frame, text='Date of birth:')
            date_of_birth_label.grid(row=2, column=2, padx=self.padx, pady=self.pady, sticky='e')
            date_of_birth_val_label = ttk.Label(self.student_information_frame,
                                                text=datetime_to_str(self.student.date_of_birth))
            date_of_birth_val_label.grid(row=2, column=3, padx=self.padx, pady=self.pady, sticky='w')

            address_label = ttk.Label(self.student_information_frame, text='Address:')
            address_label.grid(row=3, column=2, padx=self.padx, pady=self.pady, sticky='e')
            address_val_label = ttk.Label(self.student_information_frame,
                                          text=shorten_string(self.student.address, 20))
            address_val_label.grid(row=3, column=3, padx=self.padx, pady=self.pady, sticky='w')

            phone_primary_label = ttk.Label(self.student_information_frame, text='Primary phone:')
            phone_primary_label.grid(row=4, column=2, padx=self.padx, pady=self.pady, sticky='e')
            phone_primary_val_label = ttk.Label(self.student_information_frame, text=self.student.phone_primary)
            phone_primary_val_label.grid(row=4, column=3, padx=self.padx, pady=self.pady, sticky='w')

            email_primary_label = ttk.Label(self.student_information_frame, text='Primary email:')
            email_primary_label.grid(row=5, column=2, padx=self.padx, pady=self.pady, sticky='e')
            email_primary_val_label = ttk.Label(self.student_information_frame, text=self.student.email_primary)
            email_primary_val_label.grid(row=5, column=3, padx=self.padx, pady=self.pady, sticky='w')

            phone_emergency_label = ttk.Label(self.student_information_frame, text='Emergency phone:')
            phone_emergency_label.grid(row=6, column=2, padx=self.padx, pady=self.pady, sticky='e')
            phone_emergency_val_label = ttk.Label(self.student_information_frame, text=self.student.phone_emergency)
            phone_emergency_val_label.grid(row=6, column=3, padx=self.padx, pady=self.pady, sticky='w')

            primary_lang_label = ttk.Label(self.student_information_frame, text='Primary language:')
            primary_lang_label.grid(row=7, column=2, padx=self.padx, pady=self.pady, sticky='e')
            primary_lang_val_label = ttk.Label(self.student_information_frame,
                                               text=self.student.primary_lang.capitalize())
            primary_lang_val_label.grid(row=7, column=3, padx=self.padx, pady=self.pady, sticky='w')

            date_separator = ttk.Separator(self.student_information_frame, orient='horizontal')
            date_separator.grid(row=8, column=0, columnspan=4, padx=self.padx, pady=self.pady, sticky='we')

            enrolment_date_label = ttk.Label(self.student_information_frame, text='Info submitted on:')
            enrolment_date_label.grid(row=9, column=0, columnspan=2, padx=self.padx, pady=self.pady, sticky='e')
            enrolment_date_val_label = ttk.Label(self.student_information_frame,
                                                 text=datetime_to_str(self.student.submission_date))
            enrolment_date_val_label.grid(row=9, column=2, columnspan=2, padx=self.padx, pady=self.pady, sticky='w')

            if not self.student.is_approved:
                no_activity_details_label.pack()

                approve_enrollment_button = ttk.Button(self.action_button_frame, text='Approve Enrolment',
                                                       command=self.approve_student)
                approve_enrollment_button.pack(side='left', padx=self.padx, pady=self.pady)
            else:
                # todo: delete, edit and award panels/windows
                # if no details no_activity_details_label.pack() again
                pass

    def page_back(self):
        """
        Returns the staff to the overview page
        """
        self.pager_frame.change_to_page(
            destination_page=ui.staff.StudentOverview,
            staff=self.staff_origin,
        )

    def approve_student(self):
        user_choice = msg.askyesnocancel(
            'Student Approval',
            "Are you sure you want to approve this student's submitted details?\n\n"
            "Selecting 'No' will force the student to re-enter their details. "
            "You can also select 'Cancel' to abort this choice."
        )

        if user_choice is None:
            msg.showinfo('Student Approval', 'Student details approval aborted. '
                                             'No changes made to database.')
        elif user_choice:
            self.student.is_approved = 1
            msg.showinfo('Student Approval', 'Student details approved.')

        else:
            # clearing the fullname attribute means the student has to enter all data again
            self.student.fullname = ''
            msg.showinfo('Student Approval', 'Student details rejected.')

        self.page_back()
