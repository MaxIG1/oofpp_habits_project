
from turtle import right
import unittest
from trackerpy3 import Seven_day_habit
from trackerpy3 import Interface
import pandas as pd
from unittest import mock
from unittest.mock import patch
import datetime as dt
import random
import string
from random import randrange


#this test creates random strings with random lenghts so that the test works always with different strings

my_rad_int = randrange(100)




def get_random_string(length):
    # choose from all lowercase letter
        letters = string.ascii_letters
        result_str = ''.join(random.choice(letters) for i in range(length))
        return result_str

test_var = get_random_string(my_rad_int)


# here are all the variables the testinmg needs
new_test_name = get_random_string(randrange(100)) 
new_test_name1 = get_random_string(randrange(100)) 
new_test_periodicity = randrange(100)
new_test_periodicity1 = randrange(100)

#user input for test_create_habit_no_dataframe_from_today
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


#create a random date within the start and end date, so that a right tracking start date is created.
time_between_dates = random_date_end - random_date_start
days_between_dates = time_between_dates.days
random_number_of_days = random.randrange(days_between_dates)
right_tracking_start = random_date_start + dt.timedelta(days=random_number_of_days)


#create a date within timeframe but outside of periodicity
new_entry_within_periodicity = right_tracking_start + dt.timedelta(7)
new_entry_outside_of_periodicity = right_tracking_start + dt.timedelta(6)

#creating a radnom date outside of dataframe and outside of periodicirty
new_entry_outside_of_df_periodicity = right_tracking_start - dt.timedelta(3)

#creating a date 14 days from today 
date_today_14 = dt.date.today() + dt.timedelta(14)

#creating an entry with wrong periodicity for add_value_today
wrong_periodicity_add_value_today = dt.date.today() + dt.timedelta(3)




#create a random date within the start of tracking and end of dataframe, so that a right entry date is created.
time_between_dates = random_date_end - right_tracking_start
days_between_dates = time_between_dates.days
random_number_of_days = random.randrange(days_between_dates)
right_entry_date = right_tracking_start + dt.timedelta(days=random_number_of_days)

#transform datetime to string

right_tracking_start = str(right_tracking_start)
random_date_start = str(random_date_start)
random_date_end = str(random_date_end)
date_today = dt.datetime.today().strftime('%Y-%m-%d')
right_entry_date = str(right_entry_date)
new_entry_within_periodicity = str(new_entry_within_periodicity)
new_entry_outside_of_periodicity = str(new_entry_outside_of_periodicity)
new_entry_outside_of_df_periodicity  = str(new_entry_outside_of_df_periodicity)
date_today_14 = str(date_today_14)


class TestCalc(unittest.TestCase):

    

    def setUp(self):
        self.test_interface = Interface()
        self.test_habit = Seven_day_habit(test_var, my_rad_int)
        @patch('builtins.input', side_effect=["Max", 7, 2, random_date_start, random_date_end, right_tracking_start, 2])
        def create_basic_habit(mock_input):
            self.test_interface.create_habit()
        @patch('builtins.input', side_effect=["today", 7, 2, date_today, date_today_14, date_today, 2])
        def create_today_habit(mock_input):
            self.test_interface.create_habit()
        @patch('builtins.input', side_effect=["test", 7, 2, random_date_start, random_date_end, right_tracking_start, 2])
        def create_basic_habit_analysis(mock_input):
            self.test_interface.create_habit()

        @patch('builtins.input', side_effect=[right_tracking_start, yes, no])
        def create_anaylsis_entry1(mock_input):
            self.test_interface.habit_dict["test"].add_value_anyday()
        @patch('builtins.input', side_effect=[new_entry_within_periodicity , yes, no])
        def create_anaylsis_entry2(mock_input):
            self.test_interface.habit_dict["test"].add_value_anyday()

        @patch('builtins.input', side_effect=["test_for_no_user_input", 1, 2, "2022-01-01", "2022-12-31", "2022-01-01", 2])
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
        
# takes the random genereated strings and integes and see if the can create a class
    def test_habit(self):
        self.assertEqual(self.test_habit.habit_name, test_var)
        self.assertEqual(self.test_habit.periodicity, my_rad_int)
        self.assertEqual(self.test_habit.entry_time_name, "entry time " + self.test_habit.habit_name)

    # this testchecks the follwoing: create a habit, enter random name, random periodicity, basic timeframe option,
    # start tracking within range, no new habit.
    # Basic / tracking Start date within / no new habit

    @patch('builtins.input', side_effect=[new_test_name, new_test_periodicity, yes, date_today, no])
    def test_create_habit_no_custom_data_frame(self, mock_input):
        self.test_interface.create_habit()
        self.assertEqual(self.test_interface.habit_dict[new_test_name].habit_name, new_test_name)
        self.assertEqual(self.test_interface.habit_dict[new_test_name].periodicity, int(new_test_periodicity))
        self.assertEqual(self.test_interface.habit_dict[new_test_name].created.replace(microsecond=0), dt.datetime.now().replace(microsecond=0))


    # this testchecks the follwoing: create a habit, enter random name, random periodicity, basic timeframe option,
    # start tracking not within range, repeated entry within range, no new habit.
    # Basic / tracking Start date not within / no new habit

    @patch('builtins.input', side_effect=[new_test_name, new_test_periodicity, yes, wrong_tracking_start, date_today, no])
    def test_create_habit_no_custom_data_frame_false_tracking_start(self, mock_input):
        self.test_interface.create_habit()
        self.assertEqual(self.test_interface.habit_dict[new_test_name].habit_name, new_test_name)
        self.assertEqual(self.test_interface.habit_dict[new_test_name].periodicity, int(new_test_periodicity))
        self.assertEqual(self.test_interface.habit_dict[new_test_name].created.replace(microsecond=0), dt.datetime.now().replace(microsecond=0))

    # this testchecks the follwoing: create a habit, enter random name, random periodicity, 
    # basic timeframe option, start tracking within range, new habit with the same options repeated.
    # Basic / tracking Start date within / new new habit

    @patch('builtins.input', side_effect=[new_test_name, new_test_periodicity, yes, date_today, yes, new_test_name1, new_test_periodicity1, yes, date_today, no])
    def test_create_habit_no_custom_data_frame_repeated_habit_entry(self, mock_input):
        self.test_interface.create_habit()
        self.assertEqual(self.test_interface.habit_dict[new_test_name].habit_name, new_test_name)
        self.assertEqual(self.test_interface.habit_dict[new_test_name].periodicity, int(new_test_periodicity))
        # within repeated entries my computer takes to long and the microseconds dont match. I am pretty sure it is a bug.
        self.assertEqual(self.test_interface.habit_dict[new_test_name].created.replace(microsecond=0), dt.datetime.now().replace(microsecond=0))
        self.assertEqual(self.test_interface.habit_dict[new_test_name1].habit_name, new_test_name1)
        self.assertEqual(self.test_interface.habit_dict[new_test_name1].periodicity, int(new_test_periodicity1))
        self.assertEqual(self.test_interface.habit_dict[new_test_name1].created.replace(microsecond=0), dt.datetime.now().replace(microsecond=0))

    # this testchecks the follwoing: create a habit, enter random name, random periodicity, 
    # basic timeframe option, start tracking not within range, new habit with the same options repeated.
    # Basic / tracking Start date not within / entry / new habit

    @patch('builtins.input', side_effect=[new_test_name, new_test_periodicity, yes, wrong_tracking_start, date_today, yes, new_test_name1, new_test_periodicity1, yes, "2022-01-01", date_today, no])
    def test_create_habit_no_custom_data_frame_repeated_false_tracking_start_repeated_habit_entry(self, mock_input):
        self.test_interface.create_habit()
        self.assertEqual(self.test_interface.habit_dict[new_test_name].habit_name, new_test_name)
        self.assertEqual(self.test_interface.habit_dict[new_test_name].periodicity, int(new_test_periodicity))
        # within repeated entries my computer takes to long and the microseconds dont match. I am pretty sure it is a bug.
        self.assertEqual(self.test_interface.habit_dict[new_test_name].created.replace(microsecond=0), dt.datetime.now().replace(microsecond=0))
        self.assertEqual(self.test_interface.habit_dict[new_test_name1].habit_name, new_test_name1)
        self.assertEqual(self.test_interface.habit_dict[new_test_name1].periodicity, int(new_test_periodicity1))
        self.assertEqual(self.test_interface.habit_dict[new_test_name1].created.replace(microsecond=0), dt.datetime.now().replace(microsecond=0))

    # this test checks the follwoing: create a habit, enter random name, ranmdom periodicity, choose custom timeframe, start date before
    # end date of dataframe, start tracking within range,  no new habit.
    # Custom / Time frame within / Tracking Start date within / no new habit

    @patch('builtins.input', side_effect=[new_test_name, new_test_periodicity, no, random_date_start, random_date_end, right_tracking_start, no])
    def test_create_habit_custom_data_frame(self, mock_input):
        self.test_interface.create_habit()
        self.assertEqual(self.test_interface.habit_dict[new_test_name].habit_name, new_test_name)
        self.assertEqual(self.test_interface.habit_dict[new_test_name].periodicity, int(new_test_periodicity))
        # within repeated entries my computer takes to long and the microseconds dont match. I am pretty sure it is a bug.
        self.assertEqual(self.test_interface.habit_dict[new_test_name].created.replace(microsecond=0), dt.datetime.now().replace(microsecond=0))


    # this test checks the follwoing: create a habit, enter random name, ranmdom periodicity, choose custom timeframe, start date after
    # Custom / Time frame not within / new Entry / Tracking Start date within / no new habit
  
    @patch('builtins.input', side_effect=[new_test_name, new_test_periodicity, no, random_date_end, random_date_start, random_date_start, random_date_end, right_tracking_start, no])
    def test_create_habit_custom_data_frame_false_user_input_time_frame(self, mock_input):
        self.test_interface.create_habit()
        self.assertEqual(self.test_interface.habit_dict[new_test_name].habit_name, new_test_name)
        self.assertEqual(self.test_interface.habit_dict[new_test_name].periodicity, int(new_test_periodicity))
        # within repeated entries my computer takes to long and the microseconds dont match. I am pretty sure it is a bug.
        self.assertEqual(self.test_interface.habit_dict[new_test_name].created.replace(microsecond=0), dt.datetime.now().replace(microsecond=0))

    # Custom / Time frame within / Tracking Start date not within / new entry / no new habit

    @patch('builtins.input', side_effect=[new_test_name, new_test_periodicity, no, random_date_start, random_date_end, wrong_tracking_start, right_tracking_start, no])
    def test_create_habit_custom_data_frame_false_tracking_start(self, mock_input):
        self.test_interface.create_habit()
        self.assertEqual(self.test_interface.habit_dict[new_test_name].habit_name, new_test_name)
        self.assertEqual(self.test_interface.habit_dict[new_test_name].periodicity, int(new_test_periodicity))
        # within repeated entries my computer takes to long and the microseconds dont match. I am pretty sure it is a bug.
        self.assertEqual(self.test_interface.habit_dict[new_test_name].created.replace(microsecond=0), dt.datetime.now().replace(microsecond=0))


    #Custom / Time frame not within / new Entry / Tracking Start date not within / new entry / no new habit

    @patch('builtins.input', side_effect=[new_test_name, new_test_periodicity, no, random_date_end, random_date_start, random_date_start, random_date_end, wrong_tracking_start, right_tracking_start, no])
    def test_create_habit_custom_data_frame_false_user_input_time_frame_false_tracking_start(self, mock_input):
        self.test_interface.create_habit()
        self.assertEqual(self.test_interface.habit_dict[new_test_name].habit_name, new_test_name)
        self.assertEqual(self.test_interface.habit_dict[new_test_name].periodicity, int(new_test_periodicity))
        # within repeated entries my computer takes to long and the microseconds dont match. I am pretty sure it is a bug.
        self.assertEqual(self.test_interface.habit_dict[new_test_name].created.replace(microsecond=0), dt.datetime.now().replace(microsecond=0))


    #testing add value anyday
    
    #testing add_value_anyday if value is within end of dataframe and start of tracking

    @patch('builtins.input', side_effect=[right_tracking_start, yes, no])
    def test_add_value_anyday_within_dataframe(self, mock_input):
        self.test_interface.habit_dict["Max"].add_value_anyday()
        row_posistion_of_entry_date = self.test_interface.habit_dict["Max"].df.index[self.test_interface.habit_dict["Max"].df["Max"] == True].tolist()
        row_postion_test = self.test_interface.habit_dict["Max"].df.index[self.test_interface.habit_dict["Max"].df["Date"] == right_tracking_start].tolist()  
        self.assertEqual(row_posistion_of_entry_date, row_postion_test)    

    #testing add_value_anyday if value is outside of dataframe and start of tracking 

    @patch('builtins.input', side_effect=[wrong_tracking_start, yes, right_tracking_start, yes, no])
    def test_add_value_anyday_outside_of_accepted_values(self, mock_input):
        self.test_interface.habit_dict["Max"].add_value_anyday()
        row_posistion_of_entry_date = self.test_interface.habit_dict["Max"].df.index[self.test_interface.habit_dict["Max"].df["Max"] == True].tolist()
        row_postion_test = self.test_interface.habit_dict["Max"].df.index[self.test_interface.habit_dict["Max"].df["Date"] == right_tracking_start].tolist()  
        self.assertEqual(row_posistion_of_entry_date, row_postion_test)     

    #testing add_value_anyday if value is of periodicity 
 
    @patch('builtins.input', side_effect=[new_entry_outside_of_periodicity, 1, new_entry_within_periodicity, 1, 2])
    def test_add_value_anyday_wrong_periodicity(self, mock_input):
        self.test_interface.habit_dict["Max"].add_value_anyday()
        row_posistion_of_entry_date = self.test_interface.habit_dict["Max"].df.index[self.test_interface.habit_dict["Max"].df["Max"] == True].tolist()
        row_postion_test = self.test_interface.habit_dict["Max"].df.index[self.test_interface.habit_dict["Max"].df["Date"] == new_entry_within_periodicity].tolist()  
        self.assertEqual(row_posistion_of_entry_date, row_postion_test)   


    #new_entry_outside_of_df_periodicity

    @patch('builtins.input', side_effect=[new_entry_outside_of_df_periodicity, 1, new_entry_within_periodicity, 1, 2])
    def test_add_value_anyday_wrong_periodicity_ooutside_dataframe(self, mock_input):
        self.test_interface.habit_dict["Max"].add_value_anyday()
        row_posistion_of_entry_date = self.test_interface.habit_dict["Max"].df.index[self.test_interface.habit_dict["Max"].df["Max"] == True].tolist()
        row_postion_test = self.test_interface.habit_dict["Max"].df.index[self.test_interface.habit_dict["Max"].df["Date"] == new_entry_within_periodicity].tolist()  
        self.assertEqual(row_posistion_of_entry_date, row_postion_test) 

# add value today right entry

    @patch('builtins.input', side_effect=[1])
    def test_add_value_today_right_input(self, mock_input):
        self.test_interface.habit_dict["today"].add_value_today()
        row_posistion_of_entry_date = self.test_interface.habit_dict["today"].df.index[self.test_interface.habit_dict["today"].df["today"] == True].tolist()
        row_postion_test = self.test_interface.habit_dict["today"].df.index[self.test_interface.habit_dict["today"].df["Date"] == date_today].tolist()  
        self.assertEqual(row_posistion_of_entry_date, row_postion_test)   

# add value today entry_outside of periodicity entry

    @patch('builtins.input', side_effect=[1])
    def test_add_value_today_right_input(self, mock_input):
        self.test_interface.habit_dict["today"].add_value_today()
        row_posistion_of_entry_date = self.test_interface.habit_dict["today"].df.index[self.test_interface.habit_dict["today"].df["today"] == True].tolist()
        row_postion_test = self.test_interface.habit_dict["today"].df.index[self.test_interface.habit_dict["today"].df["Date"] == date_today].tolist()  
        self.assertEqual(row_posistion_of_entry_date, row_postion_test)   

# test if analysis module works correctly 

    # custom time frame / winning

    @patch('builtins.input', side_effect=[2, right_tracking_start, random_date_end, 2])
    def test_add_analysis_module(self, mock_input):
        self.test_interface.habit_dict["test"].analyse_habit()
        self.assertEqual(self.test_interface.habit_dict["test"].highest_streak, 2)


    # test if analysis module works correctly 
    # Basic time frame / winning

    @patch('builtins.input', side_effect=[1, 2])
    def test_analysis_module_basic_winning(self, mock_input):
        self.test_interface.habit_dict["test"].analyse_habit()
        self.assertEqual(self.test_interface.habit_dict["test"].highest_streak, 2)

    # custom time frame / loosing
    @patch('builtins.input', side_effect=[2, new_entry_within_periodicity, random_date_end, 1])
    def test_analysis_module_custom_loosing(self, mock_input):
        self.test_interface.habit_dict["test"].analyse_habit()
        dt1 = dt.datetime.strptime(new_entry_within_periodicity, "%Y-%m-%d").date()
        dt2 = dt.datetime.strptime(random_date_end, "%Y-%m-%d").date()
        timedelta = (((dt2-dt1).days)+1)/7
        self.assertEqual(self.test_interface.habit_dict["test"].lowest_streak, timedelta)


    # Basic time frame / loosing
    @patch('builtins.input', side_effect=[1, 1])
    def test_analysis_module_custom_loosing(self, mock_input):
        self.test_interface.habit_dict["test_for_no_user_input"].analyse_habit()
        dt1 = dt.datetime.strptime("2022-01-01", "%Y-%m-%d").date()
        dt2 = dt.datetime.strptime("2022-12-31", "%Y-%m-%d").date()
        timedelta = ((dt2-dt1).days)+1
        self.assertEqual(self.test_interface.habit_dict["test_for_no_user_input"].lowest_streak, timedelta)
    
    #"test_for_no_user_input"
    def test_analysis_module_no_user_input_loosing(self):
        self.test_interface.habit_dict["test_for_no_user_input"].analyse_habit_no_user_input()
        dt1 = dt.datetime.strptime("2022-01-01", "%Y-%m-%d").date()
        dt2 = dt.datetime.strptime("2022-12-31", "%Y-%m-%d").date()
        timedelta = ((dt2-dt1).days)+1
        self.assertEqual(self.test_interface.habit_dict["test_for_no_user_input"].lowest_streak, timedelta)
    
    def test_analysis_module_no_user_input_winning(self):
        self.test_interface.habit_dict["test_for_no_user_input"].analyse_habit_no_user_input()
        self.assertEqual(self.test_interface.habit_dict["test_for_no_user_input"].highest_streak, 0)

    #test format check right user input
    @patch('builtins.input', side_effect=[random_date_start])
    def test_format_check_right_user_input(self, mock_input):
        actual_value = self.test_interface.format_check("%Y-%m-%d", "test")
        expected_value = dt.datetime.strptime(random_date_start, "%Y-%m-%d")
        self.assertEqual(actual_value, expected_value)

    #test format check wrong user input
    @patch('builtins.input', side_effect=["some mysterious string", random_date_start])
    def test_format_check_wrong_user_input(self, mock_input):
        actual_value = self.test_interface.format_check("%Y-%m-%d", "test")
        expected_value = dt.datetime.strptime(random_date_start, "%Y-%m-%d")
        self.assertEqual(actual_value, expected_value)


    #test int and range check right user input
    @patch('builtins.input', side_effect=[my_rad_int])
    def test_int_and_range_check_right_user_input(self, mock_input):
        actual_value = self.test_interface.int_and_range_check(1, 100, "test")
        expected_value = my_rad_int
        self.assertEqual(actual_value, expected_value)


    #test int and range check wrong user input
    @patch('builtins.input', side_effect=["some mysterious string", my_rad_int])
    def test_int_and_range_check_wrong_user_input(self, mock_input):
        actual_value = self.test_interface.int_and_range_check(1, 100, "test")
        expected_value = my_rad_int
        self.assertEqual(actual_value, expected_value)

    #delte habit test
    @patch('builtins.input', side_effect=["Max"])
    def test_int_and_range_check_wrong_user_input(self, mock_input):
        self.test_interface.delete_habit()
        self.assertRaises(KeyError, lambda: self.test_interface.habit_dict["Max"])  


   
if __name__ == '__main__':
    unittest.main()



