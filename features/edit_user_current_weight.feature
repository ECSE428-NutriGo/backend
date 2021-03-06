Feature: Edit User Current Weight

As a user,
I would like to edit my current weight,
So that the system can accurately reflect my current state.

Scenario: Edit Current Weight (Normal Flow)

Given NutriGo user is logged into the application
When the user enters valid information for their current weight
And the user requests to edit the current weight of their profile
Then the system will register the new current weight for the user
And the user should see a confirmation message

Scenario: Invalid Current Weight (Error Flow)

Given NutriGo user is logged into the application
When the user enters invalid number for their current weight
And the user requests to edit the current weight of their profile
Then the system will maintain the old current weight for the user’s profile
