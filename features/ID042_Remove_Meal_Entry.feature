Feature: Remove of Meal Entry

As a user, 
I would like to remove a meal entry that I have previously entered,
So that the application can accurately reflect my eating patterns.

Scenario: Remove a Meal Entry (Normal Flow)

Given the User is signed in as a user 
And the user requests to remove a meal entry
And the user selects a given meal entry from their list of meal entries
Then the system will remove the given meal entry from that user 
And the user should see a confirmation message

Scenario: Remove a Meal Entry without selection (Error Flow)

Given the User is signed in as a user
And the user requests to remove a meal entry 
And the user does not select a given meal entry from their list of meal entries
Then the system will not remove a given meal entry from that user 
And the user should see an error message
