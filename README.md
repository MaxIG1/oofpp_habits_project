
# Habit Tracker

## Overview and functionality
Welcome to my Habit Tracker. This Tracker was developed in the course Obect Oriented Programming of Prof. Dr. Max Pumperla at IU.
With this tracker it is possible to track any number of habits and to display various analytics.
The different habits can have any periodicity, which means that it is possible to track a habit in any interval.
The following functionalities are available:

- Streak analysis of a habit: Analyze how successful or unsuccessful, the user was in achieving their goals during any period of time.

- View habits of the same periodicity.

- View all tracked habits, with information about the periodicity, creation date and the next due date.

- Analysis of the habit with the longest successful streak either 

- Analysis of the habit with the shortest successful streak either 

- Analysis of a habit and its longest or shortest sucess streak within a custom or preset timeframe. 

- Furthermore, of course, deleting and adding of habits at any time.

- Last but not least the option to extend the period of habit tracking.


## how to install
Simply download the trackerpy3.py file and run it in the Python terminal. 
If you prefer a juypter notebook you can use the tracker.ipynb file.
But it is recommended to use the trackerpy3.py in your terminal hence in VS Code trackerp.ipynb output is confusing.


## how to use it
It is best used in the Python terminal, e.g. of VS code.
To use a sample file, download example_file_habit_tracker.csv and import it with option 1. 
To do this, enter the path of the file (right click "copy as path". Don't forget to delete the quotation marks).

Then edit your file and analyse it as you wish.

Do not forget to save before closing if you do not want to loose your progress!

## how to test
The testing of some functions was only possible if return references in the interface were commented out. 
Therefore there is a trackerpy3patched.py file which has to be used for testing if the user wants to make the whole testing automatic, without user input needed. 

It differs only with the following lines from the main file 

- self.userinterface() commented out in lines
720 / 724 / 728 / 746 / 749 / 753 / 772 / 783 / 786 / 796 / 799 / 803 / 807.

- interface.user_interface() commented out in line 958:

- Enabled automatic import of a file rather than manually entering the path in lines
870 - 873. 

- lines 517-518 are commented out, so that the delte_habit() test works 

For automated testing, of course, the appropriate path must be entered here in pythonpy3patched.py before in 
the Datamanger.import_from_file() function at line 871.

It is also possible to test the original file trackerpy3.py, but then manual entries during the testing must be made. 
In this way it is possible to test the complete program automatically.






