Feature: Lock Out User

As a system administrator,
I would like to suspend a user’s account,
So that they can longer use the system's features.

Scenario: Lock Out User (Normal Flow)

Given NutriGo admin is logged into the application
And another user exists in the system
When the admin requests to suspend a user
And the admin provides confirmation to the system
Then the system will suspend the User from the system
And the admin should see a confirmation message
