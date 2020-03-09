Feature: Remove Food Items

As a user,
I would like to remove a food item from a meal
So that the meal will contain only the required ingredients

Scenario: Remove a single Food Item from a User's Meal (Normal Flow)

Given NutriGo user is logged into the application
And there are food items available
And there is a meal that was created by the user
When the user selects a valid food item to remove
And the user requests to remove a food item from that meal
Then the system remembers the updated meal
And the user should see a confirmation message

Scenario: Remove a food item from another User's Meal (Error Flow)

Given NutriGo user is logged into the application
And there are food items available
And there is a meal that was created by another user
When the user selects a valid food item to remove
And the user requests to remove a food item from that meal
Then the system does not allow the user to remove the given food item
And the user should see an error message
