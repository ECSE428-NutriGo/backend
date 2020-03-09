Feature: Query Food Item List

As a user
I would like to query the list of food item available
So that I can view food items to add to my meals

Scenario: Query all Food Item List (Normal Flow)

Given NutriGo user is logged into the application
And food items have been created
When the user requests to query food items in the system
Then the system displays a list of all food items

Scenario: Query all then filters some Food Items (Alternate Flow)

Given NutriGo user is logged into the application
And food items have been created
When the user requests to query food items in the system
Then the system displays a list of all food items
And the user then enters a valid search filter to filter the results
Then the system filters the current results to only those containing the search filters

Scenario: Query some Food Items (Alternate Flow)

Given NutriGo user is logged into the application
And food items have been created
When the user enters a valid search filter to filter the results
When the user requests to query food items in the system
Then the system displays a list of food items containing the search filters

Scenario: Query Food Items with No Result (Error Flow)

Given NutriGo user is logged into the application
And food items have been created
When the user enters a valid search filter to filter the results
But no food items in the system contain the search filter
And the user requests to query food items in the system
Then the system should see an error message
