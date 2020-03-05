Feature: Edit User Attributes

As a user, 
I would like to be able to change my profile attributes, 
So that the system is up to date with all my contact and personal information.

Scenario: Edit All User Attributes (Normal Flow)

Given the User is signed in as a user
When the user requests to edit the attributes of their profile 
And the user enters valid information for all changing attributes
Then the system will register the new user attributes for the user
And the user should see a confirmation message
 
Scenario: Edit Some User Attributes (Alternate Flow)

Given the User is signed in as a user
When the user requests to edit the attributes of their profile
And the user enters some valid information for changing attributes and leaves other attributes blank 
Then the system will register the new user attributes for the ones changed and will keep the old attributes for the fields left blank
And the user should see a confirmation message

Scenario: Invalid User Attributes (Error Flow)

Given the User is signed in as a user
When the user requests to edit the attributes of their profile
And the user enters invalid information for a given attributes
Then the system will not register the new user attributes for the invalid data 
And the user should see an error message