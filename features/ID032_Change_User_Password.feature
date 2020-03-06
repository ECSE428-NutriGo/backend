Feature: Change User Password

As a user 
I would like to be able to change my password 
So that I can use a different password to log into the application

Scenario: Change User Password to New Password (Normal Flow)

Given the User is signed in as a user 
When the user requests to change their password
And the user enters their old password
And the user enters a new password in both places to enter the new password
Then the system will update the new password for the user
And the user should see a success message 

Scenario: Change User Password to Old Password (Error Flow)

Given the User is signed in as a user
When the user requests to change their old password
And the user enters their old password
And the user enters their old password in both places to enter the new password
Then the system will not update the password for the user 
And the system will keep the old password for the user
And the user should see a error message saying new password cannot be the same as the old password

Scenario: Change User Password without correct double input (Error Flow)

Given the User is signed in as a user
When the user requests to change their old password
And the user enters their old password
And the user enters two different passwords in both places to enter the new password
Then the system will not update the password for the user 
And the system will keep the old password for the user
And the user should see a error message saying new password must match in both places to enter the new password

