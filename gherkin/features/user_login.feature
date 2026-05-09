# language: en

Feature: User Login
  As a registered user
  I want to be able to log in to the application
  So that I can access my personalized dashboard

  Background:
    Given the application is running
    And the user is on the login page

  Scenario: Successful login with valid credentials
    Given the user enters a valid email "user@example.com"
    And the user enters a valid password "SecurePass123!"
    When the user clicks the "Login" button
    Then the user should be redirected to the dashboard
    And a welcome message "Welcome back, User!" should be displayed
    And the session token should be stored

  Scenario: Failed login with invalid password
    Given the user enters a valid email "user@example.com"
    And the user enters an invalid password "wrongpassword"
    When the user clicks the "Login" button
    Then an error message "Invalid email or password" should be displayed
    And the user should remain on the login page
    And no session token should be stored

  Scenario: Failed login with unregistered email
    Given the user enters an unregistered email "unknown@example.com"
    And the user enters any password "anyPassword123"
    When the user clicks the "Login" button
    Then an error message "Invalid email or password" should be displayed
    And the user should remain on the login page

  Scenario: Login attempt with empty fields
    Given the user leaves the email field empty
    And the user leaves the password field empty
    When the user clicks the "Login" button
    Then a validation message "Email is required" should be displayed
    And a validation message "Password is required" should be displayed
    And the user should not be authenticated

  Scenario: Login attempt with invalid email format
    Given the user enters an invalid email format "notanemail"
    And the user enters a valid password "SecurePass123!"
    When the user clicks the "Login" button
    Then a validation message "Please enter a valid email address" should be displayed
    And the user should not be authenticated

  Scenario: Account locked after multiple failed attempts
    Given the user enters a valid email "user@example.com"
    And the user enters an invalid password "wrong" 5 times consecutively
    When the user attempts to log in a 6th time
    Then an error message "Account temporarily locked. Try again in 15 minutes." should be displayed
    And the account should be flagged in the system
    And an email notification should be sent to "user@example.com"

  Scenario Outline: Login with different valid user roles
    Given the user enters email "<email>"
    And the user enters password "<password>"
    When the user clicks the "Login" button
    Then the user should be redirected to the "<dashboard>" dashboard
    And the user role "<role>" should be set in the session

    Examples:
      | email                  | password       | dashboard | role  |
      | admin@example.com      | AdminPass123!  | admin     | ADMIN |
      | manager@example.com    | MgrPass123!    | manager   | MANAGER |
      | user@example.com       | UserPass123!   | user      | USER  |

  Scenario: Session persistence after page refresh
    Given the user has successfully logged in
    When the user refreshes the browser page
    Then the user should remain logged in
    And the dashboard should still be displayed

  Scenario: Successful logout
    Given the user is logged in
    When the user clicks the "Logout" button
    Then the user should be redirected to the login page
    And the session token should be cleared
    And the user should not be able to access the dashboard via browser back button
