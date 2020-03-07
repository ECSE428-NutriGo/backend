Feature: Edit User Target Weight

As a user,
I would like to edit my target weight,
So that I can accurately represent my fitness goals and see recommendations based on my goals.

Scenario: Edit Target Weight (Normal Flow)

Given NutriGo user is logged into the application
When the user requests to edit the target weight of their profile
And the user enters valid information for their target weight
Then the system will register the new target weight for the user
And the user should see a confirmation message

Scenario: Invalid Target Weight (Error Flow)

Given NutriGo user is logged into the application
When the user requests to edit the target weight of their profile 
And the user enters invalid number for their target weight
Then the system will not register the new target weight for the user
And the system will maintain the old target weight for the user’s profile
And the user should see an error message
