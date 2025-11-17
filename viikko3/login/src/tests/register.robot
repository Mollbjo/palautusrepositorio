*** Settings ***
Resource  resource.robot
Suite Setup     Open And Configure Browser
Suite Teardown  Close Browser
Test Setup      Reset Application Create User And Go To Register Page

*** Test Cases ***

Register With Valid Username And Password
    Set Username  ${Username}
    Set Password  ${Password}
    Set Password Confirmation  ${Password Confirmation}
    Click Button  Register
    Registration Should Succeed

Register With Too Short Username And Valid Password
    Set Username  ab
    Set Password  ${Password}
    Set Password Confirmation  ${Password Confirmation}
    Click Button  Register
    Registration Should Fail With Message  Username should have at least 3 characters

Register With Valid Username And Too Short Password
    Set Username  ${Username}
    Set Password  short
    Set Password Confirmation  short
    Click Button  Register
    Registration Should Fail With Message  Password should have at least 8 characters

Register With Valid Username And Invalid Password
# salasana ei sisällä halutunlaisia merkkejä
    Set Username  ${Username}
    Set Password  password
    Set Password Confirmation  password
    Click Button  Register
    Registration Should Fail With Message  Password should contain at least one non-alphabetic character

Register With Nonmatching Password And Password Confirmation
    Set Username  ${Username}
    Set Password  ${Password}
    Set Password Confirmation  differentpassword
    Click Button  Register
    Registration Should Fail With Message  Password and password confirmation do not match

Register With Username That Is Already In Use
    Set Username  seessaas
    Set Password  seessaas123
    Set Password Confirmation  seessaas123
    Click Button  Register
    Registration Should Fail With Message  User with username seessaas already exists

*** Keywords ***
Reset Application Create User And Go To Register Page
    Reset Application
    Create User  seessaas  seessaas123
    Go To Register Page

Registration Should Succeed
    Welcome Page Should Be Open

Registration Should Fail With Message
    [Arguments]  ${message}
    Register Page Should Be Open
    Page Should Contain  ${message}

Set Username
    [Arguments]  ${username}
    Input Text  username  ${username}

Set Password
    [Arguments]  ${password}
    Input Password  password  ${password}        

Set Password Confirmation
    [Arguments]  ${password_confirmation}
    Input Password  password_confirmation  ${password_confirmation}
