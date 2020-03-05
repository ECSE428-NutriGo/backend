Feature: Lock Out User

As a system administrator, 
I would like to suspend a user’s account, 
So that they can longer use the system's features. 

Scenario: Lock Out User (Normal Flow)

Given the System Administrator is signed in as a system admin
When the System Administrator requests to suspend a user
And the System Admin provides confirmation to the system
Then the System will suspend the User from the system
And the System Admin will see a confirmation message 
And the suspended user will receive an email of suspension