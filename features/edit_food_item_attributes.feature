Feature: Edit Food Item Attributes

As a user,
I would like to edit a food item’s attributes
So that the food item will have up-to-date information.

Scenario: Edit Self-Created Food Item Attributes (Normal Flow)

Given NutriGo user is logged into the application
And there is a food item created by that user
When the user enters valid attributes
And the user requests to edit that food item’s attributes
Then the system remembers the updated food attributes
And the user should see a confirmation message

Scenario: Edit Other's Food Item Attributes (Error Flow)

Given NutriGo user is logged into the application
And there is a food item that is not created by that user
When the user enters valid attributes
And the user requests to edit that food item’s attributes
Then the system does not allow the user to edit the attributes
And the user should see an error message
