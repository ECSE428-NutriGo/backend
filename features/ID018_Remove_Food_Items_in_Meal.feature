Feature: Remove Food Items

As a user,
I would like to remove a food item from a meal
So that the meal will contain only the required ingredients

Scenario: Remove a single Food Item from a User's Meal (Normal Flow)

Given the user is signed in as a User
When the user requests to remove a food item from a meal
And the meal was created by the user
And the user selects a valid food item to remove
Then the system remembers the updated meal
And the user should see a success message

Scenario: Remove multiple Food Items from a User's Meal (Alternative Flow)

Given the user is signed in as a User
When the user requests to remove a food item from a meal
And the meal was created by that user
And the user selects multiple valid food items to remove
Then the system remembers the updated meal
And the user should see a success message

Scenario: Remove a food item from another User's Meal (Error Flow)

Given the user is signed in as a User
When the user requests to remove a food item from a meal
And the meal was not created by that user
Then the system does not allow the user to remove the given food item
And the user should see an error message 

