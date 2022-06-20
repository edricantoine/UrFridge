# YourFridge

## An easy-to-use food tracking and recipe generating application, powered by the Spoonacular API

This application allows the user to add and remove ingredients from four separate spaces (Fridge, Freezer, Pantry, and
Miscellaneous), as well as edit the amounts of these ingredients already tracked in the application. In addition to
this, the application also allows for the user to select ingredients and retrieve recipes tailored to 
those particular ingredients using the Spoonacular API. Multiple different local users can use the application with 
unique User IDs, with each user having their own 'application state'. Additional features are also currently in 
development.

The user interface is written in Python, using the Kivy and KivyMD graphical user interface libraries.
Data persistence is done by way of SQLite3, and a local database is created on the user's device storing all local 
user IDs of the application, ingredients, and which ingredients belong to which users.

### TO INSTALL AND RUN

The current latest version of the APK is included in this repository. Currently, only Android users are able to 
install and run this application on a mobile device. If you, for whatever reason, wish to run this application from
the command line, navigate to the urFridge directory (the one with main.py and main.kv) and run:

python3 -m main


### TO RUN AND ADD TESTS

This application has a thorough test suite written using the unittest framework. In order to run these tests from the 
command line, navigate to the urFridge directory and run the command

python3 -m unittest

If you want to add tests, you can either:
1. Add tests to an already existing file in the test directory, or
2. Create a new file, which MUST follow the naming convention of test_Something.py

That way, the above command will continue to work even if new tests are added.

### TO CONTRIBUTE

As this is a relatively small personal project, I don't really mind how you write your code as long as it's, you know,
actually readable and has proper formatting and whatnot. Be sure to **open a new issue and new branches / pull requests for each new 
feature you want to add, though! (Just so I, and other contributors, know what's going on.)**

### Credits:
Created in 2022 by Edric Antoine. (That's me.)

Special thanks to [johnwmillr](https://github.com/johnwmillr) for the excellent Spoonacular API wrapper!

### Thanks for taking the time to look at this project!





