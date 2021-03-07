# Simple Banking System
My second project on HyperSkill.

## Aim of the Project
Making simple banking processes with user commands.

## Dependencies
`Python > 2.7`

`luhn` algoritm

## What the project can do?
- Creating account with unique credit card and PIN (starting with 400000)
- Login an acoount if credit card and PIN are true
    - Checking balance
    - Adding income
    - Transferring money between two different accounts (if target account and amount valid)
    - Closing an account
    - Quit to main menu
- Exit

## Database Infos
- Project can use the SQLite DBMS from the Python. 
- On the first running, `card.s3db` database file will be created to same location.
- In project, only one table `card` can be created and used.