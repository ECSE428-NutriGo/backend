Feature: Edit Food Item Attributes

As a user,
I would like to edit a food item’s attributes
So that the food item will have up-to-date information.

Scenario: Edit Self-Created Food Item Attributes (Normal Flow)

Given NutriGo user is logged into the application
When the user requests to edit a food item’s attributes
And the food item was created by that user
And the user enters valid attributes
Then the system remembers the updated food attributes
And the user should see a success message

Scenario: Edit Other's Food Item Attributes (Error Flow)

Given NutriGo user is logged into the application
When the user requests to edit a food item’s attributes
And the food item was not created by that user
Then the system does not allow the user to edit the attributes
And the user should see an error message
