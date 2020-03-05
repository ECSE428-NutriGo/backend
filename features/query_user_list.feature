Feature: Query User List

As a system administrator, 
I would like to query the user list, 
So that I can see the users of the system. 

Scenario: Query All Users (Normal Flow)

Given the System Admin is signed in as an admin
When the System Admin requests to view the users of the system
Then the System will fetch the users of the system
And the System Admin should see the users of the system

Scenario: Query Users With Filter (Alternate Flow)

Given System Administrator is signed in as an admin
When the System Admin requests to view the users of the system
And the System Admin enters appropriate filters of search
Then the system will fetch the users of the system that satisfy the filters
And the System Admin should see the filtered list of users 

Scenario: Query Users With Unmatched Filter (Error Flow)

Given the System Admin is signed in as an admin
When the System Admin requests to view the users of the system
And the System Admin enters appropriate filters of search
And no users within the system match the filter criteria
Then the system will display no users 
And the System Admin should see an error message  