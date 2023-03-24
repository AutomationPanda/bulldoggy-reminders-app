"""
This module contains Web UI tests for the Bulldoggy app.
"""

# Behaviors to test:

# Navigation:
# load the login page
# load the reminders page
# home redirects to login when not authenticated
# home redirects to reminders when logged in
# invalid navigation redirects to not found

# Login:
# log in successfully
# no login credentials
# no username
# no password
# incorrect username
# incorrect password
# log out

# Reminders:
# the initial reminders page is empty
# create the first list
# create more lists
# create the first item in a list
# create more items in a list
# strike an item as completed
# unstrike an item from being completed
# edit the name of an uncompleted item
# edit the name of a completed item
# begin editing the name of a list but cancel by clicking X
# begin editing the name of a list but cancel by clicking away
# delete an item
# delete all items
# creat new items after deleting all items in a list
# select a different list
# edit the name of an unselected list
# edit the name of a selected list
# commit an edit by clicking check
# commit an edit by typing ENTER
# begin editing the name of a list but cancel by clicking X
# begin editing the name of a list but cancel by clicking away
# delete an unselected list
# delete a selected list
# delete all lists
# create new lists after deleting all lists
# verify only one row (list or item) may be edited at a time:
#   list name
#   new list name
#   item description
#   new item description
# data persists after page refresh
# data persists after logout and log back in

# Users:
# log in as separate users in separate sessions
# one user cannot see another user's reminders