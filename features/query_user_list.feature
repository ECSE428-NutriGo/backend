Feature: Query User List

As a system administrator,
I would like to query the user list,
So that I can see the users of the system.

Scenario: Query All Users (Normal Flow)

Given NutriGo admin is logged into the application
And another user exists in the system
When the System Admin requests to view the users of the system
Then the System will fetch the users of the system
And the System Admin should see a confirmation message

Scenario: Query Users With Filter (Alternate Flow)

Given NutriGo admin is logged into the application
And another user exists in the system
When the System Admin enters appropriate filters of search
And the System Admin requests to view the users of the system
Then the system will fetch the users of the system that satisfy the filters
And the System Admin should see a confirmation message

Scenario: Query Users With Unmatched Filter (Error Flow)

Given NutriGo admin is logged into the application
And another user exists in the system
When the System Admin enters appropriate filters of search
But no users within the system match the filter criteria
And the System Admin requests to view the users of the system
Then the system will display no users
And the System Admin should see an error message
