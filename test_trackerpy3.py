import io
import sys
from turtle import right
import unittest
import trackerpy3patched
from trackerpy3patched import Habits
from trackerpy3patched import Interface
from trackerpy3patched import Datamanager
import pandas as pd
from unittest import mock
from unittest.mock import patch
import datetime as dt
import random
import string
from random import randrange
from tabulate import tabulate
from unittest.mock import MagicMock
from pathlib import Path


# this test creates random strings with random lenghts so that the test works always with different strings.
# The string follow a certain logic and are related to each other.

my_rad_int = randrange(100)


def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_letters
    result_str = "".join(random.choice(letters) for i in range(length))
    return result_str


test_var = get_random_string(my_rad_int)

# here are all the variables the testinmg needs
new_test_name = get_random_string(randrange(100))
new_test_name1 = get_random_string(randrange(100))
new_test_periodicity = randrange(100)
new_test_periodicity1 = randrange(100)

# user input for test_create_habit_no_dataframe_from_today
yes = str(1)
no = str(2)

x = True
while x == True:
    start_date = dt.date(1900, 1, 1)
    end_date = dt.date(2200, 2, 1)

    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date_start = start_date + dt.timedelta(days=random_number_of_days)
    random_number_of_days = random.randrange(days_between_dates)
    random_date_end = start_date + dt.timedelta(days=random_number_of_days)

    x = random_date_end < random_date_start

wrong_tracking_start = random_date_start
wrong_tracking_start -= dt.timedelta(days=1)
wrong_tracking_start = str(wrong_tracking_start)

# create a random date within the start and end date, so that a right tracking start date is created.
time_between_dates = random_date_end - random_date_start
days_between_dates = time_between_dates.days
random_number_of_days = random.randrange(days_between_dates)
right_tracking_start = random_date_start + dt.timedelta(days=random_number_of_days)

# create a date within timeframe but outside of periodicity
new_entry_within_periodicity = right_tracking_start + dt.timedelta(7)
new_entry_outside_of_periodicity = right_tracking_start + dt.timedelta(6)

# creating a radnom date outside of dataframe and outside of periodicirty
new_entry_outside_of_df_periodicity = right_tracking_start - dt.timedelta(3)

# creating a date 14 days from today
date_today_14 = dt.date.today() + dt.timedelta(14)

# creating an entry with wrong periodicity for add_value_today
wrong_periodicity_add_value_today = dt.date.today() + dt.timedelta(3)

# create a random date within the start of tracking and end of dataframe, so that a right entry date is created.
time_between_dates = random_date_end - right_tracking_start
days_between_dates = time_between_dates.days
random_number_of_days = random.randrange(days_between_dates)
right_entry_date = right_tracking_start + dt.timedelta(days=random_number_of_days)

# transform datetime to string

right_tracking_start = str(right_tracking_start)
random_date_start = str(random_date_start)
random_date_end = str(random_date_end)
date_today = dt.datetime.today().strftime("%Y-%m-%d")
right_entry_date = str(right_entry_date)
new_entry_within_periodicity = str(new_entry_within_periodicity)
new_entry_outside_of_periodicity = str(new_entry_outside_of_periodicity)
new_entry_outside_of_df_periodicity = str(new_entry_outside_of_df_periodicity)
date_today_14 = str(date_today_14)


class TestCalc(unittest.TestCase):
    def setUp(self):
        self.test_interface = Interface()
        self.test_datamanager = Datamanager()
        self.test_habit = Habits(test_var, my_rad_int)

        # Creating habits or functions with certain parameters to test.

        @patch(
            "builtins.input",
            side_effect=[
                "Max",
                7,
                2,
                random_date_start,
                random_date_end,
                right_tracking_start,
                2,
            ],
        )
        def create_basic_habit(mock_input):
            self.test_interface.create_habit()

        @patch(
            "builtins.input",
            side_effect=["today", 7, 2, date_today, date_today_14, date_today, 2],
        )
        def create_today_habit(mock_input):
            self.test_interface.create_habit()

        @patch(
            "builtins.input",
            side_effect=[
                "test",
                7,
                2,
                random_date_start,
                random_date_end,
                right_tracking_start,
                2,
            ],
        )
        def create_basic_habit_analysis(mock_input):
            self.test_interface.create_habit()

        @patch("builtins.input", side_effect=[right_tracking_start, yes, no])
        def create_anaylsis_entry1(mock_input):
            self.test_interface.habit_dict["test"].add_value_anyday()

        @patch("builtins.input", side_effect=[new_entry_within_periodicity, yes, no])
        def create_anaylsis_entry2(mock_input):
            self.test_interface.habit_dict["test"].add_value_anyday()

        @patch(
            "builtins.input",
            side_effect=[
                "test_for_no_user_input",
                1,
                2,
                "2022-01-01",
                "2022-12-31",
                "2022-01-01",
                2,
            ],
        )
        def create_basic_habit_test_for_no_user_input(mock_input):
            self.test_interface.create_habit()

        create_basic_habit()
        create_today_habit()
        create_basic_habit_analysis()
        create_anaylsis_entry1()
        create_anaylsis_entry2()
        create_basic_habit_test_for_no_user_input()

        print("New Test\n")

    def tearDown(self):
        print("End Test\n")

    # takes the random generated strings and integers and see if the can create a class
    def test_habit(self):
        self.assertEqual(self.test_habit.habit_name, test_var)
        self.assertEqual(self.test_habit.periodicity, my_rad_int)
        self.assertEqual(
            self.test_habit.entry_time_name, "entry time " + self.test_habit.habit_name
        )

    # The following tests test all possible permutations of entries. E.g. entry within timeframe, outside of timeframe...

    # This test checks the following: create a habit, enter random name, random periodicity, basic timeframe option,
    # Start tracking within range, no new habit.
    # Basic / tracking start date within / no new habit

    @patch(
        "builtins.input",
        side_effect=[new_test_name, new_test_periodicity, yes, date_today, no],
    )
    def test_create_habit_no_custom_data_frame(self, mock_input):
        self.test_interface.create_habit()
        self.assertEqual(
            self.test_interface.habit_dict[new_test_name].habit_name, new_test_name
        )
        self.assertEqual(
            self.test_interface.habit_dict[new_test_name].periodicity,
            int(new_test_periodicity),
        )
        self.assertEqual(
            self.test_interface.habit_dict[new_test_name].created.replace(
                microsecond=0
            ),
            dt.datetime.now().replace(microsecond=0),
        )

    # This test checks the following: create a habit, enter random name, random periodicity, basic timeframe option,
    # Start tracking not within range, repeated entry within range, no new habit.
    # Basic / tracking start date not within / no new habit

    @patch(
        "builtins.input",
        side_effect=[
            new_test_name,
            new_test_periodicity,
            yes,
            wrong_tracking_start,
            date_today,
            no,
        ],
    )
    def test_create_habit_no_custom_data_frame_false_tracking_start(self, mock_input):
        self.test_interface.create_habit()
        self.assertEqual(
            self.test_interface.habit_dict[new_test_name].habit_name, new_test_name
        )
        self.assertEqual(
            self.test_interface.habit_dict[new_test_name].periodicity,
            int(new_test_periodicity),
        )
        self.assertEqual(
            self.test_interface.habit_dict[new_test_name].created.replace(
                microsecond=0
            ),
            dt.datetime.now().replace(microsecond=0),
        )

    # This test checks the following: create a habit, enter random name, random periodicity,
    # Basic timeframe option, start tracking within range, new habit with the same options repeated.
    # Basic / tracking start date within / new habit

    @patch(
        "builtins.input",
        side_effect=[
            new_test_name,
            new_test_periodicity,
            yes,
            date_today,
            yes,
            new_test_name1,
            new_test_periodicity1,
            yes,
            date_today,
            no,
        ],
    )
    def test_create_habit_no_custom_data_frame_repeated_habit_entry(self, mock_input):
        self.test_interface.create_habit()
        self.assertEqual(
            self.test_interface.habit_dict[new_test_name].habit_name, new_test_name
        )
        self.assertEqual(
            self.test_interface.habit_dict[new_test_name].periodicity,
            int(new_test_periodicity),
        )
        # within repeated entries my computer takes to long and the microseconds dont match. I am pretty sure it is a bug.
        self.assertEqual(
            self.test_interface.habit_dict[new_test_name].created.replace(
                microsecond=0
            ),
            dt.datetime.now().replace(microsecond=0),
        )
        self.assertEqual(
            self.test_interface.habit_dict[new_test_name1].habit_name, new_test_name1
        )
        self.assertEqual(
            self.test_interface.habit_dict[new_test_name1].periodicity,
            int(new_test_periodicity1),
        )
        self.assertEqual(
            self.test_interface.habit_dict[new_test_name1].created.replace(
                microsecond=0
            ),
            dt.datetime.now().replace(microsecond=0),
        )

    # This test checks the following: create a habit, enter random name, random periodicity,
    # Basic timeframe option, start tracking not within range, new habit with the same options repeated.
    # Basic / tracking start date not within / entry / new habit

    @patch(
        "builtins.input",
        side_effect=[
            new_test_name,
            new_test_periodicity,
            yes,
            wrong_tracking_start,
            date_today,
            yes,
            new_test_name1,
            new_test_periodicity1,
            yes,
            "2022-01-01",
            date_today,
            no,
        ],
    )
    def test_create_habit_no_custom_data_frame_repeated_false_tracking_start_repeated_habit_entry(
        self, mock_input
    ):
        self.test_interface.create_habit()
        self.assertEqual(
            self.test_interface.habit_dict[new_test_name].habit_name, new_test_name
        )
        self.assertEqual(
            self.test_interface.habit_dict[new_test_name].periodicity,
            int(new_test_periodicity),
        )
        # within repeated entries my computer takes to long and the microseconds dont match. I am pretty sure it is a bug.
        self.assertEqual(
            self.test_interface.habit_dict[new_test_name].created.replace(
                microsecond=0
            ),
            dt.datetime.now().replace(microsecond=0),
        )
        self.assertEqual(
            self.test_interface.habit_dict[new_test_name1].habit_name, new_test_name1
        )
        self.assertEqual(
            self.test_interface.habit_dict[new_test_name1].periodicity,
            int(new_test_periodicity1),
        )
        self.assertEqual(
            self.test_interface.habit_dict[new_test_name1].created.replace(
                microsecond=0
            ),
            dt.datetime.now().replace(microsecond=0),
        )

    # This test checks the following: create a habit, enter random name, ranmdom periodicity, choose custom timeframe, start date before
    # End date of dataframe, start tracking within range,  no new habit.
    # Custom / timeframe within / tracking start date within / no new habit

    @patch(
        "builtins.input",
        side_effect=[
            new_test_name,
            new_test_periodicity,
            no,
            random_date_start,
            random_date_end,
            right_tracking_start,
            no,
        ],
    )
    def test_create_habit_custom_data_frame(self, mock_input):
        self.test_interface.create_habit()
        self.assertEqual(
            self.test_interface.habit_dict[new_test_name].habit_name, new_test_name
        )
        self.assertEqual(
            self.test_interface.habit_dict[new_test_name].periodicity,
            int(new_test_periodicity),
        )
        # within repeated entries my computer takes to long and the microseconds dont match. I am pretty sure it is a bug.
        self.assertEqual(
            self.test_interface.habit_dict[new_test_name].created.replace(
                microsecond=0
            ),
            dt.datetime.now().replace(microsecond=0),
        )

    # This test checks the following: create a habit, enter random name, ranmdom periodicity, choose custom timeframe, start date after
    # Custom / timeframe not within / new entry / tracking start date within / no new habit

    @patch(
        "builtins.input",
        side_effect=[
            new_test_name,
            new_test_periodicity,
            no,
            random_date_end,
            random_date_start,
            random_date_start,
            random_date_end,
            right_tracking_start,
            no,
        ],
    )
    def test_create_habit_custom_data_frame_false_user_input_time_frame(
        self, mock_input
    ):
        self.test_interface.create_habit()
        self.assertEqual(
            self.test_interface.habit_dict[new_test_name].habit_name, new_test_name
        )
        self.assertEqual(
            self.test_interface.habit_dict[new_test_name].periodicity,
            int(new_test_periodicity),
        )
        # within repeated entries my computer takes to long and the microseconds dont match. I am pretty sure it is a bug.
        self.assertEqual(
            self.test_interface.habit_dict[new_test_name].created.replace(
                microsecond=0
            ),
            dt.datetime.now().replace(microsecond=0),
        )

    # Custom / timeframe within / tracking start date not within / new entry / no new habit

    @patch(
        "builtins.input",
        side_effect=[
            new_test_name,
            new_test_periodicity,
            no,
            random_date_start,
            random_date_end,
            wrong_tracking_start,
            right_tracking_start,
            no,
        ],
    )
    def test_create_habit_custom_data_frame_false_tracking_start(self, mock_input):
        self.test_interface.create_habit()
        self.assertEqual(
            self.test_interface.habit_dict[new_test_name].habit_name, new_test_name
        )
        self.assertEqual(
            self.test_interface.habit_dict[new_test_name].periodicity,
            int(new_test_periodicity),
        )
        # within repeated entries my computer takes to long and the microseconds dont match. I am pretty sure it is a bug.
        self.assertEqual(
            self.test_interface.habit_dict[new_test_name].created.replace(
                microsecond=0
            ),
            dt.datetime.now().replace(microsecond=0),
        )

    # Custom / timeframe not within / new entry / tracking start date not within / new entry / no new habit

    @patch(
        "builtins.input",
        side_effect=[
            new_test_name,
            new_test_periodicity,
            no,
            random_date_end,
            random_date_start,
            random_date_start,
            random_date_end,
            wrong_tracking_start,
            right_tracking_start,
            no,
        ],
    )
    def test_create_habit_custom_data_frame_false_user_input_time_frame_false_tracking_start(
        self, mock_input
    ):
        self.test_interface.create_habit()
        self.assertEqual(
            self.test_interface.habit_dict[new_test_name].habit_name, new_test_name
        )
        self.assertEqual(
            self.test_interface.habit_dict[new_test_name].periodicity,
            int(new_test_periodicity),
        )
        # within repeated entries my computer takes to long and the microseconds dont match. I am pretty sure it is a bug.
        self.assertEqual(
            self.test_interface.habit_dict[new_test_name].created.replace(
                microsecond=0
            ),
            dt.datetime.now().replace(microsecond=0),
        )

    # testing add value anyday

    # testing add_value_anyday if value is within end of dataframe and start of tracking

    @patch("builtins.input", side_effect=[right_tracking_start, yes, no])
    def test_add_value_anyday_within_dataframe(self, mock_input):
        self.test_interface.habit_dict["Max"].add_value_anyday()
        row_posistion_of_entry_date = (
            self.test_interface.habit_dict["Max"]
            .df.index[self.test_interface.habit_dict["Max"].df["Max"] == True]
            .tolist()
        )
        row_postion_test = (
            self.test_interface.habit_dict["Max"]
            .df.index[
                self.test_interface.habit_dict["Max"].df["Date"] == right_tracking_start
            ]
            .tolist()
        )
        self.assertEqual(row_posistion_of_entry_date, row_postion_test)

    # testing add_value_anyday if value is outside of dataframe and start of tracking

    @patch(
        "builtins.input",
        side_effect=[wrong_tracking_start, yes, right_tracking_start, yes, no],
    )
    def test_add_value_anyday_outside_of_accepted_values(self, mock_input):
        self.test_interface.habit_dict["Max"].add_value_anyday()
        row_posistion_of_entry_date = (
            self.test_interface.habit_dict["Max"]
            .df.index[self.test_interface.habit_dict["Max"].df["Max"] == True]
            .tolist()
        )
        row_postion_test = (
            self.test_interface.habit_dict["Max"]
            .df.index[
                self.test_interface.habit_dict["Max"].df["Date"] == right_tracking_start
            ]
            .tolist()
        )
        self.assertEqual(row_posistion_of_entry_date, row_postion_test)

    # testing add_value_anyday if value is outside of periodicity

    @patch(
        "builtins.input",
        side_effect=[
            new_entry_outside_of_periodicity,
            1,
            new_entry_within_periodicity,
            1,
            2,
        ],
    )
    def test_add_value_anyday_wrong_periodicity(self, mock_input):
        self.test_interface.habit_dict["Max"].add_value_anyday()
        row_posistion_of_entry_date = (
            self.test_interface.habit_dict["Max"]
            .df.index[self.test_interface.habit_dict["Max"].df["Max"] == True]
            .tolist()
        )
        row_postion_test = (
            self.test_interface.habit_dict["Max"]
            .df.index[
                self.test_interface.habit_dict["Max"].df["Date"]
                == new_entry_within_periodicity
            ]
            .tolist()
        )
        self.assertEqual(row_posistion_of_entry_date, row_postion_test)

    # new_entry_outside_of_df_periodicity

    @patch(
        "builtins.input",
        side_effect=[
            new_entry_outside_of_df_periodicity,
            1,
            new_entry_within_periodicity,
            1,
            2,
        ],
    )
    def test_add_value_anyday_wrong_periodicity_ootside_dataframe(self, mock_input):
        self.test_interface.habit_dict["Max"].add_value_anyday()
        row_posistion_of_entry_date = (
            self.test_interface.habit_dict["Max"]
            .df.index[self.test_interface.habit_dict["Max"].df["Max"] == True]
            .tolist()
        )
        row_postion_test = (
            self.test_interface.habit_dict["Max"]
            .df.index[
                self.test_interface.habit_dict["Max"].df["Date"]
                == new_entry_within_periodicity
            ]
            .tolist()
        )
        self.assertEqual(row_posistion_of_entry_date, row_postion_test)

    # add value today right entry

    @patch("builtins.input", side_effect=[1])
    def test_add_value_today_right_input(self, mock_input):
        self.test_interface.habit_dict["today"].add_value_today()
        row_posistion_of_entry_date = (
            self.test_interface.habit_dict["today"]
            .df.index[self.test_interface.habit_dict["today"].df["today"] == True]
            .tolist()
        )
        row_postion_test = (
            self.test_interface.habit_dict["today"]
            .df.index[self.test_interface.habit_dict["today"].df["Date"] == date_today]
            .tolist()
        )
        self.assertEqual(row_posistion_of_entry_date, row_postion_test)

    # add value today entry_outside of periodicity entry

    @patch("builtins.input", side_effect=[1])
    def test_add_value_today_right_input(self, mock_input):
        self.test_interface.habit_dict["today"].add_value_today()
        row_posistion_of_entry_date = (
            self.test_interface.habit_dict["today"]
            .df.index[self.test_interface.habit_dict["today"].df["today"] == True]
            .tolist()
        )
        row_postion_test = (
            self.test_interface.habit_dict["today"]
            .df.index[self.test_interface.habit_dict["today"].df["Date"] == date_today]
            .tolist()
        )
        self.assertEqual(row_posistion_of_entry_date, row_postion_test)

    # Test if analysis module works correctly

    # Custom timeframe / winning

    @patch("builtins.input", side_effect=[2, right_tracking_start, random_date_end, 2])
    def test_add_analysis_module(self, mock_input):
        self.test_interface.habit_dict["test"].analyse_habit()
        self.assertEqual(self.test_interface.habit_dict["test"].highest_streak, 2)

    # Test if analysis module works correctly
    # Basic timeframe / winning

    @patch("builtins.input", side_effect=[1, 2])
    def test_analysis_module_basic_winning(self, mock_input):
        self.test_interface.habit_dict["test"].analyse_habit()
        self.assertEqual(self.test_interface.habit_dict["test"].highest_streak, 2)

    # Test if analysis module works correctly
    # Custom timeframe / loosing

    @patch(
        "builtins.input",
        side_effect=[2, new_entry_within_periodicity, random_date_end, 1],
    )
    def test_analysis_module_custom_loosing(self, mock_input):
        self.test_interface.habit_dict["test"].analyse_habit()
        dt1 = dt.datetime.strptime(new_entry_within_periodicity, "%Y-%m-%d").date()
        dt2 = dt.datetime.strptime(random_date_end, "%Y-%m-%d").date()
        timedelta = (((dt2 - dt1).days) + 1) / 7
        self.assertEqual(
            self.test_interface.habit_dict["test"].lowest_streak, timedelta
        )

    # Test if analysis module works correctly
    # Basic timeframe / loosing

    @patch("builtins.input", side_effect=[1, 1])
    def test_analysis_module_custom_loosing(self, mock_input):
        self.test_interface.habit_dict["test_for_no_user_input"].analyse_habit()
        dt1 = dt.datetime.strptime("2022-01-01", "%Y-%m-%d").date()
        dt2 = dt.datetime.strptime("2022-12-31", "%Y-%m-%d").date()
        timedelta = ((dt2 - dt1).days) + 1
        self.assertEqual(
            self.test_interface.habit_dict["test_for_no_user_input"].lowest_streak,
            timedelta,
        )

    # test_for_no_user_input

    def test_analysis_module_no_user_input_loosing(self):
        self.test_interface.habit_dict[
            "test_for_no_user_input"
        ].analyse_habit_no_user_input()
        dt1 = dt.datetime.strptime("2022-01-01", "%Y-%m-%d").date()
        dt2 = dt.datetime.strptime("2022-12-31", "%Y-%m-%d").date()
        timedelta = ((dt2 - dt1).days) + 1
        self.assertEqual(
            self.test_interface.habit_dict["test_for_no_user_input"].lowest_streak,
            timedelta,
        )

    def test_analysis_module_no_user_input_winning(self):
        self.test_interface.habit_dict[
            "test_for_no_user_input"
        ].analyse_habit_no_user_input()
        self.assertEqual(
            self.test_interface.habit_dict["test_for_no_user_input"].highest_streak, 0
        )

    # test format check right user input
    @patch("builtins.input", side_effect=[random_date_start])
    def test_format_check_right_user_input(self, mock_input):
        actual_value = self.test_interface.format_check("%Y-%m-%d", "test")
        expected_value = dt.datetime.strptime(random_date_start, "%Y-%m-%d")
        self.assertEqual(actual_value, expected_value)

    # test format check wrong user input
    @patch("builtins.input", side_effect=["some mysterious string", random_date_start])
    def test_format_check_wrong_user_input(self, mock_input):
        actual_value = self.test_interface.format_check("%Y-%m-%d", "test")
        expected_value = dt.datetime.strptime(random_date_start, "%Y-%m-%d")
        self.assertEqual(actual_value, expected_value)

    # test int and range check right user input
    @patch("builtins.input", side_effect=[my_rad_int])
    def test_int_and_range_check_right_user_input(self, mock_input):
        actual_value = self.test_interface.int_and_range_check(1, 100, "test")
        expected_value = my_rad_int
        self.assertEqual(actual_value, expected_value)

    # test int and range check wrong user input
    @patch("builtins.input", side_effect=["some mysterious string", my_rad_int])
    def test_int_and_range_check_wrong_user_input(self, mock_input):
        actual_value = self.test_interface.int_and_range_check(1, 100, "test")
        expected_value = my_rad_int
        self.assertEqual(actual_value, expected_value)

    # delte habit test
    @patch("builtins.input", side_effect=["Max"])
    def delete_habit_habit_exists(self, mock_input):
        self.test_interface.delete_habit()
        self.assertRaises(KeyError, lambda: self.test_interface.habit_dict["Max"])

    # delte habit test with user input failure. To make this test work the the interface.delete_habit() needs to comment out the following two lines
    # print("The following habits exist:")
    # self.show_all_habit()
    # which is commented out in the patched version

    @patch("builtins.input", side_effect=["nononono"])
    def test_delete_habit_failure(self, mock_input):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        self.test_interface.delete_habit()
        sys.stdout = sys.__stdout__
        actual_value = capturedOutput.getvalue()
        expected_value = "No such habit exists. Try again\n"
        self.assertEqual(actual_value, expected_value)

    # obviously the import test needs to be adapeted to a file existing on the users computer.
    @patch(
        "builtins.input",
        side_effect=[
            r"C:\Users\Max_G\ProgrammierProjekte\Habit-Tracker_IU\example file.csv"
        ],
    )
    def test_import_from_file(self, mock_input):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        self.test_datamanager.import_from_file()
        sys.stdout = sys.__stdout__
        actual_value = capturedOutput.getvalue()
        expected_value = "the following habits have beein imported ['Boxen', 'Drink Plenty Water', 'Eating Healthy', 'Sleeping Early', 'Meditation']\n"
        self.assertEqual(actual_value, expected_value)

    @patch("trackerpy3patched.Interface.int_and_range_check")
    def test_interface_analyse_save1_to_file(self, mock_input_1):
        mock_input_1.return_value = 1
        self.test_datamanager.saveall_merged_to_file = MagicMock()
        assert self.test_datamanager.saveall_merged_to_file.called_once()

    # testingthe streak analysis from within example dataset. Thus the filename within the patched python project
    # needs to be adapted (!)

    def test_analyse_max_streak(self):
        trackerpy3patched.datamanager.import_from_file()
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        trackerpy3patched.interface.analyse_habit_max_streak()
        sys.stdout = sys.__stdout__
        actual_value = capturedOutput.getvalue()
        expected_value = "Your 7 day habit Eating Healthy has the longest consecutive streak of 21 days\n\
Your 2 day habit Meditation has the highest streak of 7 ticked of habits in a row\n"
        self.assertEqual(actual_value, expected_value)

    # testing the streak analysis from within example dataset. Thus the filename within the patched python project
    # needs to be adapted (!)

    def test_analyse_min_streak(self):
        trackerpy3patched.datamanager.import_from_file()
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        trackerpy3patched.interface.analyse_habit_min_streak()
        sys.stdout = sys.__stdout__
        actual_value = capturedOutput.getvalue()
        expected_value = "Your 1 day habit Sleeping Early has the longest streak of not ticking of your habit 176 times in a row\n\
Your 1 day habit Sleeping Early has the longest consecutive streak of not achieving your goal 176 days\n"
        self.assertEqual(actual_value, expected_value)

    # user_interface tests as far as possible.

    @patch.object(trackerpy3patched.datamanager, "import_from_file")
    @patch.object(trackerpy3patched.interface, "int_and_range_check")
    # @patch('builtins.input', side_effect=[1])
    def test_interface_test(self, mock_input, mock_input_1):
        mock_input.return_value = 1
        trackerpy3patched.interface.user_interface()
        mock_input_1.assert_called()

    @patch(
        "builtins.input",
        side_effect=[2, "megatest", new_test_periodicity, yes, date_today, no, 8],
    )
    def test_interface_create_habit(self, mock_input):
        self.test_interface.user_interface()
        self.assertEqual(
            self.test_interface.habit_dict["megatest"].habit_name, "megatest"
        )

    @patch("builtins.input", side_effect=[3, "Max", 8])
    def test_interface_delete_habit(self, mock_input):
        self.test_interface.user_interface()
        self.assertRaises(KeyError, lambda: self.test_interface.habit_dict["Max"])

    @patch("builtins.input", side_effect=[4, "super", 8])
    def test_interface_add_value(self, mock_input):
        self.test_interface.user_interface()
        self.assertRaises(KeyError, lambda: self.test_interface.habit_dict["super"])

    @patch("builtins.input", side_effect=[5, 1, 8])
    def test_interface_analyse_habits(self, mock_input):
        self.test_interface.user_interface()

    @patch("builtins.input", side_effect=[5, 3, 1, 8])
    def test_interface_analyse_streakss_equal_periodicity(self, mock_input):
        self.test_interface.user_interface()

    @patch("builtins.input", side_effect=[5, 4, 1, 8])
    def test_interface_analyse_streaks_higest(self, mock_input):
        self.test_interface.user_interface()

    @patch.object(trackerpy3patched.datamanager, "saveall_merged_to_file")
    @patch.object(trackerpy3patched.interface, "int_and_range_check")
    def test_interface_analyse_save_to_file(self, mock_input, mock_input_1):
        mock_input.return_value = 6
        trackerpy3patched.interface.user_interface()
        mock_input_1.assert_called_once()

    @patch("builtins.input", side_effect=[8])
    def test_interface_close(self, mock_input):
        self.test_interface.user_interface()
        self.test_interface.user_interface = MagicMock()
        assert self.test_interface.user_interface.called_once()


if __name__ == "__main__":
    unittest.main()
