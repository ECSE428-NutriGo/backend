Feature: Query List of Meal Entries

As a user
I would like to see the list of meal entries that I have eaten
So that I can keep track of all my previous meals

Scenario: Query List of Meal Entries (Normal Flow)

Given the user is signed in as a User
When the user requests to query all their meal entries
Then the system displays a list of all meal entries entered by the user


Scenario: Query List of All Meal Entries (Alternate Flow)

Given the user is signed in as a User
When the user requests to query all their meal entries
And the user provides a food item to filter meal entries by
Then the system displays a list of all meal entries entered by the user containing that food item 
