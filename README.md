# messaging
Messaging system for companies to communicate with clients.

This program was designed on Ubuntu 16.04 using Python 3.5+, but should run on most machines with python 3.5+

## Using Messaging.py
To run the program use "Python3 ./Messaging.py".  You will be presented with a menu from which you can either message guests with a new or existing template, create a new template for later use, or view existing templates.  
  If you choose to message a guest you will be presented with a second menu from which you can choose to use an existing template or create a new template that you can choose to save or not. Whichever options you choose, you will be prompted to enter necessary information.  When messages are "sent" they will be printed to the screen.  After actions are taken you should return to the main menu.  Use ctr+C or option 5 at the main menu to exit

  When writing templates you can use angle brackets to write <variableNames>.  Valid variable names include: timeOfDay, greeting, company, city, timezone, firstName, lastName, roomNumber, startTimestamp, and endTimestamp.


## Design
  The design revolved around simple printed menus.  Each menu has it's own function, with helper functions preceding the rest for obvious reasons.  The json library for python was used for most of the heavy lifting.  Json writing straight to file was used since templates aren't often, or can't be, deleted and a presumably reasonable number and size of templates will exist.  If this was not the case, a type of "appending" to the json information would need to be performed instead.  This puts saving at O(n+m) instead of O(m).


## Language
  Python was the language of choice for this project.  Of the languages that I am most familiar with Python is the most efficient for small projects.  Python has a solid json library and is easy to use.  Input validation is fairly straightforward  and easy with Python as well.
  

## Testing
  Given the size of the project, no automated testing was created.  The program was tested manually on both Ubuntu 16.04 and Windows 10.  Both myself and couple of friends spent a short time trying to break the program unsuccessfully.  
  
  
## Potential Improvements
  - Time zones could be used to modify <timeOfDay> and <greeting> given a default timezone to adjust from.  
  - A pretty GUI.  
  - Templates are completely rewritten on every save, taking O(n+m) time.  If a VERY large number of templates was created this might need to be changed to a special type of append.
  - Deleting and re-ordering templates
  - Adding guests and companies through the menu
  - An option to automatically replace missing <variable> fields.
  - Checks for data read from file. e.g. check if <roomNumber> is an integer.  
  - Automated tests
  - If a small number of templates is expected, a re-read/append method would allow for safer multi-user file saving.
