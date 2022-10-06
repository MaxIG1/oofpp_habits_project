import pandas as pd
import datetime as dt
from functools import reduce
from tabulate import tabulate


class Habits:
    def __init__(self, name, periodicity):
        self.df = ()
        self.periodicity = periodicity
        self.habit_name = name
        self.entry_time_name = "entry time " + self.habit_name
        self.start_date = ()
        self.row_position_start_date = ()
        self.created = ()
        self.lowest_streak = ()
        self.highest_streak = ()
        self.end_date = ()
        self.number_of_days_highest = ()
        self.number_of_days_lowest = ()

    # this function is the analysis function. It analyses streaks depending on the periodicity of the habit and depending on the users wishes.
    def analyse_habit(self):
        lowval = 1
        highval = 2
        text = f"Press 1. if you want to analyse your habit {self.habit_name} from the start day {self.start_date}\
 until the end of the existing data, which is the {self.end_date}.\n\
Press 2. if you want to analyse a custom timeframe.\n\
You have data between {self.start_date} and {self.end_date}."

        # the functions only accepts user input as integeger and within the definerd range Loval, highval.
        input_check = interface.int_and_range_check(lowval, highval, text)

        # option 1 creates a temporary dataframe, from the tracking start date to today or to the end of the existing dataframe.
        # The analysis method works only with adjacent rows, therefore only cells within periodicity are stored within the temporary dataframe.
        if input_check == 1:
            row_position_start_date = self.row_position_start_date
            df = self.df.iloc[row_position_start_date[0] :: self.periodicity, :]
            df = df.reset_index(drop=True)

        # option 2 creates a temporary dataframe, from the custom inputs. The analysis method works only
        # with adjacent rows, therefore only cells within periodicity are stored within the temporary dataframe.
        elif input_check == 2:
            
            # input check to check if the user enters date within the existing data.
            x = False
            while x == False:

                fmt = "%Y-%m-%d"
                text = "Enter yyyy-mm-dd of beginning date of your analysis"
                date_start = interface.format_check(fmt, text)

                text = "Enter yyyy-mm-dd of end date of your analysis"
                date_end = interface.format_check(fmt, text)

                x = (
                    self.start_date
                    <= date_start.date()
                    <= date_end.date()
                    <= self.end_date
                )

            row_position_start_index = self.df.index[
                self.df["Date"] == date_start
            ].tolist()
            row_position_end_index = self.df.index[self.df["Date"] == date_end].tolist()

            # this is the temp. dataframe for analysis.
            df = self.df.iloc[
                row_position_start_index[0] : row_position_end_index[
                    0
                ] : self.periodicity,
                :,
            ]
            df = df.reset_index(drop=True)

        text = f"Press 1. to analyse your failure streak for your habit {self.habit_name}.\n\
Press 2. to analyse your sucess streak for your habit {self.habit_name}.\n"

        lowval = 1
        highval = 2
        input_check = interface.int_and_range_check(lowval, highval, text)

        # the following lines of code until the next input check calculate the longest streak#
        # of not achieving ones goal.
        if input_check == 1:

            df["start_of_streak"] = df[self.habit_name].ne(df[self.habit_name].shift())
            df["streak_id"] = df["start_of_streak"].cumsum()
            df["streak_counter"] = df.groupby("streak_id").cumcount() + 1

            # gives back the max value of the streak counter
            df_loosing_subset = df[df[self.habit_name] == False]
            self.lowest_streak = df_loosing_subset["streak_counter"].max(0)
            # the NaN check is necessary since if the users have not missed any steps, this would create not zero but NaN.
            # the function Interface.analyse_habit_max_streak() uses a comparison function max that only works with numbers.
            nan_check = pd.isna(self.lowest_streak)
            if nan_check == True:
                self.lowest_streak = 0
                print("You have completed every step")

            else:
                index_up_of_lowest_streak = df_loosing_subset.index[
                    df_loosing_subset["streak_counter"] == self.lowest_streak
                ].tolist()
                index_low_of_lowest_streak = (
                    index_up_of_lowest_streak[0] - self.lowest_streak + 1
                )
                start_date_of_lowest_streak = df_loosing_subset.at[
                    index_low_of_lowest_streak, "Date"
                ]
                end_date_of_lowest_streak = df_loosing_subset.at[
                    index_up_of_lowest_streak[0], "Date"
                ]

                # the following two variables are needed to give the user a more precise information about his streak.
                # Hence the the number of ticked of habits alone doesnt give enough information.
                number_of_days = self.lowest_streak * self.periodicity
                number_of_weeks = round((self.lowest_streak * self.periodicity / 7), 4)

                # the calculation within the number of days is necessary hence if the user again checks off their habit after missing e.g. one streak
                # they miss the first time periodicty and the days until cheking off.
                print(
                    f"Your habit {self.habit_name} with the periodicity of {self.periodicity} has  the longest streak of not achieving your goal \n\
the following number of days: {number_of_days+self.periodicity-1} or the following number of weeks: {number_of_weeks}  between \n\
the {start_date_of_lowest_streak.date()} and the {end_date_of_lowest_streak.date()}. You did not check off your habit {self.lowest_streak} times during that time period."
                )

        # the following lines of code calculate the longest streak
        # of achieving ones goal.
        elif input_check == 2:

            df["start_of_streak"] = df[self.habit_name].ne(df[self.habit_name].shift())
            df["streak_id"] = df["start_of_streak"].cumsum()
            df["streak_counter"] = df.groupby("streak_id").cumcount() + 1

            # gives back the max value of the streak counter
            df_winning_subset = df[df[self.habit_name] == True]
            self.highest_streak = df_winning_subset["streak_counter"].max(0)
            # the NaN check is necessary since if the users have completed all steps, this would create not zero but NaN.
            # the function Interface.analyse_habit_max_streak() uses a comparison function max that only works with numbers.
            nan_check = pd.isna(self.highest_streak)
            
            if nan_check == True:
                self.highest_streak = 0
                print(f"You have no streaks with your habit {self.habit_name}.\n")

            else:
                index_up_of_highest_streak = df_winning_subset.index[
                    df_winning_subset["streak_counter"] == self.highest_streak
                ].tolist()
                index_low_of_highest_streak = (
                    index_up_of_highest_streak[0] - self.highest_streak + 1
                )
                start_date_of_highest_streak = df_winning_subset.at[
                    index_low_of_highest_streak, "Date"
                ]
                end_date_of_highest_streak = df_winning_subset.at[
                    index_up_of_highest_streak[0], "Date"
                ]

                number_of_days = self.highest_streak * self.periodicity
                number_of_weeks = round((self.highest_streak * self.periodicity / 7), 4)

                print(
                    f"Your habit {self.habit_name} with the periodicity of {self.periodicity} has  the longest streak of achieving your goal \n\
the following number of days: {number_of_days} or the following number of weeks: {number_of_weeks}  between \n\
{start_date_of_highest_streak.date()} and {end_date_of_highest_streak.date()}. You checked your habit {self.highest_streak} times during that time period."
                )

    # this function does the same as the function with user input but without user input.
    # it is needed for the comparison of max and min streaks, which the functions Interface.analyse_habit_max_streak()
    # and Interface.analyse_habit_min_streak() use. Since it is unprobale that the user has analysed all of his habits
    # recently this function will do that.
    def analyse_habit_no_user_input(self):
        df = self.df.iloc[self.row_position_start_date[0] :: self.periodicity, :]
        df = df.reset_index(drop=True)

        df["start_of_streak"] = df[self.habit_name].ne(df[self.habit_name].shift())
        df["streak_id"] = df["start_of_streak"].cumsum()
        df["streak_counter"] = df.groupby("streak_id").cumcount() + 1

        df_loosing_subset = df[df[self.habit_name] == False]
        df_loosing_subset["streak_counter"].max(0)
        self.lowest_streak = df_loosing_subset["streak_counter"].max(0)
        nan_check = pd.isna(self.lowest_streak)
        if nan_check == True:
            self.lowest_streak = 0

        self.number_of_days_lowest = self.lowest_streak * self.periodicity

        df["start_of_streak"] = df[self.habit_name].ne(df[self.habit_name].shift())
        df["streak_id"] = df["start_of_streak"].cumsum()
        df["streak_counter"] = df.groupby("streak_id").cumcount() + 1

        df_winning_subset = df[df[self.habit_name] == True]
        df_winning_subset["streak_counter"].max(0)
        self.highest_streak = df_winning_subset["streak_counter"].max(0)
        nan_check = pd.isna(self.highest_streak)
        if nan_check == True:
            self.highest_streak = 0

        self.number_of_days_highest = self.highest_streak * self.periodicity

    # this functions sets the start day, where the user wants to start tracking. Since the dataframe might a different
    # start date it is necessary to create a start_date for tracking, so that the analysis know for which date on to
    # analyse streaks.
    def set_start_day(self):

        # the normed row name is necessary so that the import works properly.
        start_row_name = "start " + self.habit_name
        while True:
            try:

                fmt = "%Y-%m-%d"
                text = f"Which date do you want to start tracking ýour habit {self.habit_name}? yyyy-mm-dd"
                # the following line checks if the user input has the necessary date format.

                start_date_to_be_transformed = interface.format_check(fmt, text)
                start_date = str(start_date_to_be_transformed.date())
                self.row_position_start_date = self.df.index[
                    self.df["Date"] == start_date
                ].tolist()
                self.df[start_row_name] = False
                self.df.loc[[self.row_position_start_date[0]], start_row_name] = True
                self.start_date = start_date_to_be_transformed.date()

                return

            except (IndexError):
                print("Start of tracking date outside of dataframe. Try Again.")

    # this function adds an entry today. Its is slighly redundant with the function add_value_anyday(self)
    # but since it needs less user input it is more convenient.

    def add_value_today(self):

        date_today = str(dt.date.today())
        date_today_index = self.df.index[self.df["Date"] == date_today].tolist()

        lowval = 1
        highval = 2
        text = f"Press 1. if you did achieve your goal for habit {self.habit_name} today, the {date_today}.\n\
Press 2. if you did not achieve your goal habit {self.habit_name} today, the {date_today}\n"

        # the functions only accepts user input as integeger and within the definerd range Loval, highval.
        input_check = interface.int_and_range_check(lowval, highval, text)

        # the following lines of code check if "today" is within the needed periodicity. If so users can enter their entry,
        # elso it does not work.
        if input_check == 1:

            timedelta = self.start_date - dt.date.today()
            timedelta_days_check = timedelta.days % self.periodicity
            if timedelta_days_check == 0:
                self.df.loc[[date_today_index[0]], self.habit_name] = True
                print("Positive entry added for", dt.date.today())
            else:
                print("no", self.periodicity, "days have passed")

        elif input_check == 2:

            timedelta = self.start_date - dt.date.today()
            timedelta_days_check = timedelta.days % self.periodicity
            if timedelta_days_check == 0:
                self.df.loc[[date_today_index[0]], self.habit_name] = False
                print("Negativ entry added for", dt.date.today())
            else:
                print("no", self.periodicity, "days have passed")

    # the following function allows users to add values on anyday.

    def add_value_anyday(self):
        now = dt.datetime.now()
        current_time = now.strftime("%H:%M:%S")

        x = True
        while x == True:

            fmt = "%Y-%m-%d"
            text = f"For which day do you want to change habit {self.habit_name}?\n"

            # the following line checks if the user input has the necessary date format.

            entry_date = interface.format_check(fmt, text)

            # this line checks if the entry date is within the allowed boundries. Else the user will be notified.
            if self.start_date <= entry_date.date() <= self.end_date:

                # the following lines of code do the checking of the periodicity
                timedelta = self.start_date - entry_date.date()
                timedelta_days_check = timedelta.days % self.periodicity
                row_posistion_of_entry_date = self.df.index[
                    self.df["Date"] == str(entry_date)
                ].tolist()
                if timedelta_days_check == 0:

                    lowval = 1
                    highval = 2
                    text = f"Press 1. if you did achieve your goal for habit {self.habit_name} on the {entry_date.date()}.\n\
Press 2. if you did not achieve your goal habit {self.habit_name} on the {entry_date.date()}.\n"

                    # the functions only accepts user input as integeger and within the definerd range Loval, highval.
                    # Option 1 does create a positive entry
                    input_check = interface.int_and_range_check(lowval, highval, text)
                    if input_check == 1:
                        self.df.loc[
                            [row_posistion_of_entry_date[0]], self.habit_name
                        ] = True
                        self.df.loc[
                            [row_posistion_of_entry_date[0]], self.entry_time_name
                        ] = current_time
                        print("Positive entry added for", entry_date.date())
                    # Option 2 does create a positive entry
                    elif input_check == 2:
                        self.df.loc[
                            [row_posistion_of_entry_date[0]], self.habit_name
                        ] = False
                        self.df.loc[
                            [row_posistion_of_entry_date[0]], self.entry_time_name
                        ] = current_time
                        print("Negativ entry added for", entry_date.date())

                else:
                    print("the time period of", self.periodicity, "has not passed")

            else:
                print("you are outside of your timeframe")

            lowval = 1
            highval = 2
            text = f"Press 1. if you want to add another day for your habit {self.habit_name}.\n\
Press 2. if you are done with creating new entries\n"

            # the functions only accepts user input as integeger and within the definerd range Loval, highval.
            input_check = interface.int_and_range_check(lowval, highval, text)

            if input_check == 1:
                x = True
            elif input_check == 2:
                x = False


# here is Interface class. The interface communicates with the user and holds the user_inteface.
class Interface:
    def __init__(self):
        # this is the core functionality. All habits instances are stored within a dictionary.
        self.habit_dict = {}

    # the format check does check if the entered date has the right format.
    def format_check(self, fmt, text):
        while True:
            try:
                date = input(text)
                date = dt.datetime.strptime(date, fmt)
                return date
            except (ValueError):
                print("Wrong format")

    # this function checks if the user input is wihtin the accepted range and is an integer.
    def int_and_range_check(self, lowval, highval, text):
        while True:
            try:
                number = int(input(text))
                if lowval <= number <= highval:
                    return number
            except (ValueError, TypeError):
                pass

    # this funcion creates habits and saves them in the habit_dict of the interface.
    def create_habit(self):

        x = True
        while x == True:

            name = input("Enter the name of your habit.\n")
            print("Your habit has the name " + name)

            # no such thing as an integer infinity exist in the basic python package. Adding an indefinite integer would be possible
            # but I dont think it would be worth it. So the maximum range is three years
            lowval = 1
            highval = 1095
            text = "Enter the periodicity of your habit as an integer.\n "

            # the functions only accepts user input as integeger and within the definerd range Loval, highval.
            periodicity = self.int_and_range_check(lowval, highval, text)

            # this is where the habits instances with their periodicities are stored within the dictionary.
            self.habit_dict[name] = Habits(name, periodicity)

            lowval = 1
            highval = 2
            text = "Which time frame do you want to cover\n\
Press 1: From today to the end of the year\n\
Press 2: From custom date to custom date\n"

            # the user has two option. Created a basic dataframe from today to the end of the year or a custom dataframe.
            input_check = self.int_and_range_check(lowval, highval, text)

            if input_check == 1:
                start = str(dt.date.today())
                end = str(dt.datetime.now().year) + "-12-31"
                end_date_to_be_transformed = datetimeobj = dt.datetime.strptime(
                    end, "%Y-%m-%d"
                )
                self.habit_dict[name].end_date = end_date_to_be_transformed.date()

            elif input_check == 2:
                while x == True:

                    fmt = "%Y-%m-%d"
                    text = "Enter your start date yyyy-mm-dd"
                    # the following line checks if the user input has the necessary date format.

                    start_to_be_transformed = self.format_check(fmt, text)
                    type(start_to_be_transformed)
                    start = str(start_to_be_transformed.date())

                    text = "Enter your end date yyyy-mm-dd"
                    # the following line checks if the user input has the necessary date format.

                    end_to_be_transformed = self.format_check(fmt, text)
                    end = str(end_to_be_transformed.date())
                    self.habit_dict[name].end_date = end_to_be_transformed.date()

                    x = start_to_be_transformed > end_to_be_transformed

            self.habit_dict[name].df = pd.DataFrame(
                {
                    "Date": pd.date_range(start, end),
                    self.habit_dict[name].habit_name: False,
                    self.habit_dict[name].entry_time_name: " ",
                }
            )

            self.habit_dict[name].set_start_day()

            # This variable stores the creation date-time, when the habit was created.
            self.habit_dict[name].created = dt.datetime.now()

            lowval = 1
            highval = 2
            text = f"Press 1. if you want to add another habit.\n\
Press 2. if you are done with creating habits\n"

            # The functions only accepts user input as integeger and within the definerd range Loval, highval.
            input_check = interface.int_and_range_check(lowval, highval, text)

            if input_check == 1:
                x = True
            elif input_check == 2:
                x = False

    # As the name might suggest, this is for deleting a habit.
    def delete_habit(self):

        print("The following habits exist:")
        self.show_all_habit()

        name = input("which habit do you want to delete?\n")

        # A little user input check, if the habit the user wants to delete exists.
        if name in self.habit_dict:
            del self.habit_dict[name]
            print(f"Deleted your habit {name} successfully")

        else:
            print("No such habit exists. Try again")

    # As the name suggests, this shows all habits.
    def show_all_habit(self):
        list_names = ["Habit name"]
        list_created = ["Date created"]

        for x in self.habit_dict:
            list_names.append(self.habit_dict[x].habit_name)
            list_created.append(self.habit_dict[x].created.date())

        table = [list_names, list_created]
        print(tabulate(table))

    # As the name suggests, this presents all habits with equal periodicity.
    def present_habits_with_equal_periodicity(self):

        lowval = 1
        highval = 1095
        text = "For which periodicity do you want to see your habits? \n\
Enter an integer. For example for daily periodicity 1, for weekly periodicity 7.\n"

        # the functions only accepts user input as integeger and within the definerd range Loval, highval.
        periodicity_check = interface.int_and_range_check(lowval, highval, text)

        # this habit_list is used as a header of the tabulate table.
        habit_list = [(str(periodicity_check) + " day habit(s):")]

        for x in self.habit_dict:
            if self.habit_dict[x].periodicity == periodicity_check:
                habit_list.append(self.habit_dict[x].habit_name)

        if habit_list == [(str(periodicity_check) + " day habit(s):")]:
            print(f"You have no habits of periodicity {periodicity_check}!")

        elif habit_list != [(str(periodicity_check) + " day habit(s):")]:
            table = [habit_list]
            print(tabulate(table))

    # this function gives back all the habit with the maximum streaks.
    def analyse_habit_max_streak(self):

        habit_list = []

        # first all habits are analysed.
        for x in self.habit_dict:
            self.habit_dict[x].analyse_habit_no_user_input()

        # a list of all habits is created, so that they can be compared
        for x in self.habit_dict:
            habit_list.append(self.habit_dict[x])

        max_attr = max(habit_list, key=lambda x: x.highest_streak)
        max_attr_days = max(habit_list, key=lambda x: x.number_of_days_highest)

        if max_attr.highest_streak == 0:
            print("You have no streaks")

        else:
            # since the number of the most ticked of habits must not be the longest streak two options are presented.
            for x in self.habit_dict:
                if self.habit_dict[x].highest_streak == max_attr.highest_streak:
                    print(
                        "Your",
                        self.habit_dict[x].periodicity,
                        "day habit",
                        self.habit_dict[x].habit_name,
                        "has the highest streak of",
                        self.habit_dict[x].highest_streak,
                        "ticked of habits in a row",
                    )

                if (
                    self.habit_dict[x].number_of_days_highest
                    == max_attr_days.number_of_days_highest
                ):
                    print(
                        "Your",
                        self.habit_dict[x].periodicity,
                        "day habit",
                        self.habit_dict[x].habit_name,
                        "has the longest consecutive streak of",
                        self.habit_dict[x].number_of_days_highest,
                        "days",
                    )

    # this function gives back all the habit with the minimum streaks.
    # the rest is equivalent to the function above.
    def analyse_habit_min_streak(self):

        habit_list = []

        for x in self.habit_dict:
            self.habit_dict[x].analyse_habit_no_user_input()

        for x in self.habit_dict:
            habit_list.append(interface.habit_dict[x])

        min_attr = max(habit_list, key=lambda x: x.lowest_streak)
        min_attr_days = max(habit_list, key=lambda x: x.number_of_days_lowest)

        if min_attr.lowest_streak == 0:
            print("You have completed all your habits perfectly")

        else:

            for x in self.habit_dict:
                if self.habit_dict[x].lowest_streak == min_attr.lowest_streak:
                    print(
                        "Your",
                        interface.habit_dict[x].periodicity,
                        "day habit",
                        interface.habit_dict[x].habit_name,
                        "has the longest streak of not ticking of your habit",
                        interface.habit_dict[x].lowest_streak,
                        "times in a row",
                    )

                if (
                    self.habit_dict[x].number_of_days_lowest
                    == min_attr_days.number_of_days_lowest
                ):

                    print(
                        "Your",
                        self.habit_dict[x].periodicity,
                        "day habit",
                        self.habit_dict[x].habit_name,
                        "has the longest consecutive streak of not achieving your goal",
                        self.habit_dict[x].number_of_days_lowest,
                        "days",
                    )

    # the user interface method takes the user input and presents the options with tabulate.
    def user_interface(self):

        table = [
            "1. Import",
            "2. Create habit",
            "3. Delete habit",
            "4. Add new entry",
            "5. Anaylse habit",
            "6. Save",
            "7. Close",
        ]
        print(
            "USER INTERFACE \n Press the following numbers for your options\n",
            tabulate(table),
        )

        lowval = 1
        highval = 7
        text = "Choose your option"
        input_check = self.int_and_range_check(lowval, highval, text)

        if input_check == 1:
            datamanager.import_from_file()
            self.user_interface()

        elif input_check == 2:
            self.create_habit()
            self.user_interface()

        elif input_check == 3:
            self.delete_habit()
            self.user_interface()

        elif input_check == 4:
            print("you have data for the following habits:\n")
            self.show_all_habit()

            habit_input = input("For which habit do you want to add a new entry?")

            if habit_input in self.habit_dict:
                lowval = 1
                highval = 2
                text = f"Press 1. to add a new entry today for habit {habit_input}. \n\
Press 2. to add a new entry on anyday.\n"

                new_entry_check = self.int_and_range_check(lowval, highval, text)

                if new_entry_check == 1:
                    interface.habit_dict[habit_input].add_value_today()
                    self.user_interface()
                elif new_entry_check == 2:
                    interface.habit_dict[habit_input].add_value_anyday()
                    self.user_interface()

            if habit_input not in self.habit_dict:
                print("No such habit exists. Try again")
                self.user_interface()

        elif input_check == 5:
            table = [
                "1. Show all habits",
                "2. Analyse streaks",
                "3. Show all habit with equal periodicity",
                "4. Analyse habit with highest / lowest streak",
            ]
            print(tabulate(table))

            lowval = 1
            highval = 4
            text = "Choose your option\n"

            input_check = self.int_and_range_check(lowval, highval, text)

            if input_check == 1:
                interface.show_all_habit()
                self.user_interface()

            elif input_check == 2:
                print("you have data for the following habits:\n")
                self.show_all_habit()
                habit_input = input("Which habit do you want to analyse?\n")
                if habit_input in self.habit_dict:
                    interface.habit_dict[habit_input].analyse_habit()
                else:
                    print("No such habit exists. Try again")

                self.user_interface()
            elif input_check == 3:
                interface.present_habits_with_equal_periodicity()
                self.user_interface()
            elif input_check == 4:
                lowval = 1
                highval = 2
                text = "Press 1. to analyse the habit with the longest sucessful streak. \n\
Press 2. to analyse the habit with the longest unsucessful streak.\n"

                input_check = self.int_and_range_check(lowval, highval, text)
                if input_check == 1:
                    interface.analyse_habit_max_streak()
                    self.user_interface()
                elif input_check == 2:
                    interface.analyse_habit_min_streak()
                    self.user_interface()

        elif input_check == 6:
            datamanager.saveall_merged_to_file()
            self.user_interface()

        elif input_check == 7:
            print("Goodbye")


# the datamanager class saves and importes files.
class Datamanager:
    def __init__(self):
        pass

    # this method saves the file to the computer. Users have two options, either to take the name provided by the programm or enter a custom name.
    def saveall_merged_to_file(self):

        text = "Press 1. for the system namescape of your file\nPress 2. for custom name of your file."
        lowval = 1
        highval = 2

        input_check = interface.int_and_range_check(lowval, highval, text)

        if input_check == 1:
            date_today = "{:%Y_%m_%d_%H_%M_%S}".format(dt.datetime.now())
            file_name_today = "habit_file" + "_" + date_today + ".csv"

        elif input_check == 2:
            file_name_today = input("Enter your file name.")
            file_name_today = file_name_today + ".csv"

        df_list = []
        meta_data_list = ["Blank"]
        merged_df = []

        # a list of all dataframes is created and in the next step, merged succesive.
        for x in interface.habit_dict:
            df_var = interface.habit_dict[x].df
            df_list.append(df_var)

        # the reduce function merges in the following way. First df 1 and 2. AFter that the resuslt of the merge with df3 and so on.
        # an outer merge is ued whihc keeps all information and enters nan where no information exsits.
        # in this case that means that were no entries for a date exists nan will be entered, which will be used during the import.
        merged_df = reduce(lambda l, r: pd.merge(l, r, on="Date", how="outer"), df_list)
        merged_df = merged_df.sort_values(by=["Date"])
        merged_df = merged_df.reset_index(drop=True)

        # the following lines create a row with the metadata, that is passed into the merged df,
        # so that it can be identified to which habit, which metadatabelongs
        for x in interface.habit_dict:
            meta_data_list.extend(
                [
                    interface.habit_dict[x].periodicity,
                    interface.habit_dict[x].created,
                    "Blank",
                ]
            )

        merged_df.loc[len(merged_df.index)] = meta_data_list

        merged_df.to_csv(file_name_today, index=False)
        print("saved as", file_name_today)

    # the datamanager import method imoprt the files
    def import_from_file(self):

        # file_name = (
        # r"C:\Users\Max_G\ProgrammierProjekte\Habit-Tracker_IU\example file.csv"
        # )
        file_name = input("Enter your the directory and filename of your file")

        df = pd.read_csv(f"{file_name}")

        # this line does export the metadata from the datafame.
        meta_data = df.loc[len(df) - 1].tolist()
        df = df.drop([len(df) - 1])

        # this line tells the user which habits will be imported
        collum_list = df.columns.tolist()
        print("the following habits have beein imported", collum_list[1::3])

        # this does the following: Iterate through a zipped list. The first iteration
        # will use the first habit_name from collum list. Since every thrid entry in the df is a new
        # habit name this is is necessary code. The meta data list works the same way. The
        # for loop takes every third entry, which is the periodicty, and every third entry starting from
        # position two is the meta data of the creation.
        for name, periodicity, created in zip(
            collum_list[1::3], meta_data[1::3], meta_data[2::3]
        ):
            interface.habit_dict[name] = Habits(name, int(periodicity))
            interface.habit_dict[name].created = pd.to_datetime(created)
            col_name1 = "entry time " + name
            col_name2 = "start " + name
            
            # creates the collums of the datafrmae
            interface.habit_dict[name].df = df[
                ["Date", interface.habit_dict[name].habit_name, col_name1, col_name2]
            ]
            # drop all rows where in the collum habit name an na is included. That way only the original dataframe
            # is restored
            interface.habit_dict[name].df = interface.habit_dict[name].df[
                interface.habit_dict[name]
                .df[interface.habit_dict[name].habit_name]
                .notna()
            ]
            # resets index, just to be sure.
            interface.habit_dict[name].df = interface.habit_dict[name].df.reset_index(
                drop=True
            )
            # trasnfroms text false and true to boolean. This collum contains the acutal ticked off habits
            interface.habit_dict[name].df[name] = (
                interface.habit_dict[name].df[name].map({"True": True, "False": False})
            )
            # trasnfroms text false and true to boolean. This collum contains the start-date of tracking
            interface.habit_dict[name].df[col_name2] = (
                interface.habit_dict[name]
                .df[col_name2]
                .map({"True": True, "False": False})
            )
            # the following lines of code recreated meta-data or information that is need for analyis:
            # here the row position start date, which the analyse habit method uses.
            interface.habit_dict[name].row_position_start_date = (
                interface.habit_dict[name]
                .df.index[interface.habit_dict[name].df[col_name2] == True]
                .tolist() 
            )
            # this function transforms pandas date method to datetime, since the program mostly uses datetime.
            interface.habit_dict[name].df["Date"] = pd.to_datetime(
                interface.habit_dict[name].df["Date"]
            )

            # the next line is abundand but to makes the code clearer the start date is created
            # so that the next function, can use it.
            row_position_start_date = interface.habit_dict[
                name
            ].row_position_start_date[0]
    
            # this function creates the start of tracking of the habit instance.
            interface.habit_dict[name].start_date = (
                interface.habit_dict[name]
                .df["Date"]
                .iloc[row_position_start_date]
                .date()
            )

            # this function creates the end date of the dataframe, which is need for the analysis.
            interface.habit_dict[name].end_date = (
                interface.habit_dict[name]
                .df.loc[len(interface.habit_dict[name].df) - 1, "Date"]
                .date()
            )


interface = Interface()
datamanager = Datamanager()
interface.user_interface()
