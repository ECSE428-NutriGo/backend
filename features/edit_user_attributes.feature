Feature: Edit User Attributes

As a user,
I would like to be able to change my profile attributes,
So that the system is up to date with all my contact and personal information.

Scenario Outline: Edit All User Attributes (Normal Flow)

Given NutriGo user is logged into the application
When the user enters valid "<email>", "<age>", "<hours_activity>", "<protein_target>", "<fat_target>", "<carb_target>" for all changing attributes
And the user requests to edit the attributes of their profile
Then the system will register the new user attributes for the user
And the user should see a confirmation message

Examples: Valid Information
   | email         | age         | hours_activity   | protein_target    | fat_target    | carb_target   |
   | test@user.com | 25          | 20               | 100               | 101           | 102           |

Scenario Outline: Edit Some User Attributes (Alternate Flow)

Given NutriGo user is logged into the application
When the user enters some valid "<email>", "<age>", "<hours_activity>", "<protein_target>", "<fat_target>", "<carb_target>" for changing attributes and leaves other attributes blank
And the user requests to edit the attributes of their profile
Then the system will register the new user attributes for the ones changed and will keep the old attributes for the fields left blank
And the user should see a confirmation message

Examples: Partial Information
   | email         | age         | hours_activity   | protein_target    | fat_target    | carb_target   |
   | test@user.com | 25          | .                | 100               | 101           | 102           |
   | test@user.com | 25          | 20               | .                 | 101           | 102           |
   | test@user.com | 20          | 20               | 10                | .             | .             |
   | test@user.com | 22          | .                | .                 | .             | .             |

Scenario Outline: Invalid User Attributes (Error Flow)

Given NutriGo user is logged into the application
When the user enters invalid "<email>", "<age>", "<hours_activity>", "<protein_target>", "<fat_target>", "<carb_target>" for a given attributes
And the user requests to edit the attributes of their profile
Then the system will not register the new user attributes for the invalid data

Examples: Invalid Information
   | email         | age         | hours_activity   | protein_target    | fat_target    | carb_target   |
   | test@user.com | -1          | 20               | 100               | 101           | 102           |
   | test@user.com | 25          | -1               | 100               | 101           | 102           |
   | test@user.com | 20          | 20               | -1                | -1            | -1            |
   | test@user.com | 20          | 20               | 100               | -2            | 102           |
   | test@user.com | 20          | 20               | 100               | -2            | -2            |
