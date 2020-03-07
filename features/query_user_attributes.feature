Feature: Query User Attributes

As a system administrator,
I would like to query the attributes of the users of the system,
So that I can see individual information of users.

Scenario: Query User Attributes (Normal Flow)

Given NutriGo admin is logged into the application
When the System Admin requests to view the attributes of an individual user of the system
And the System Admin enters the appropriate filter to search the individual user of the system
Then the system will fetch the attributes of the requested user
And the System Admin should see the attributes of the user

Scenario: Query Users With Invalid Filter (Error Flow)

Given NutriGo admin is logged into the application
When the System Admin requests to view the attributes of an individual user of the system
And the System Admin enters an incorrect filter to search the individual user of the system
Then the system will not fetch the attributes of the requested user
And the System admin should see an error message
