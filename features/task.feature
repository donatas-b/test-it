Feature: QA Task

  Scenario: system can be started and run
    Given I have backend file
    And I have UI file
    When I run the backend
    Then csv file should be generated
    And generated csv file should have correct data
    When I try to open UI page
    Then UI page should be opened
    And UI chart should show correct data