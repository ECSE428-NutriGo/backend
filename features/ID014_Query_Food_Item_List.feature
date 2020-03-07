Feature: Query Food Item List

As a user
I would like to query the list of food item available
So that I can view food items to add to my meals

Scenario: Query Food Item List (Normal Flow)

Given the user is signed in as a User
When the user requests to query food items in the system
And the user enters a valid search filter to filter the results
Then the system displays a list of food items containing the search filters

Scenario: Query all Food Items (Alternate Flow)

Given the user is signed in as a User
When the user requests to query all food items in the system
And the system displays a list of all food items in the system
And the user then enters a valid search filter to filter the results
Then the system filters the current results to only those containing the search filters

Scenario: Query Food Items with No Result (Error Flow)

Given the user is signed in as a User
When the user requests to query food items in the system
And the user enters a valid search filter to filter the results
And no food items in the system contain the search filter
Then the system displays an error message


