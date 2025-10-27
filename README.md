# OU Parking App
## Description
We are developing an app that aims to help OU Students find parking around and on the OU campus reducing stress and wasted time. The app will collect information from students about their schedules and the app's AI will estimate parking availability of specific lots at different times. This app would help alleviate some problems with the scarcity of OU parking spaces and empty spots.

## Usage
Users from the University of Oklahoma will input their schedules as guided to do in the app. The student will then be able to view the “Find a Spot” tab in the app to see a list of recommended parking structures from the AI. By selecting a parking structure the student will be able to view a list of time slots and the likely number of spots available at each time. They will also be able to input a date and time to receive more specific information.

## Current Features

### Parking Lot Locator

- Allows a user to select between a selection of buildings, and gives the closest parking lot to that building
- Gives the user the address of the parking lot and the distance from the building to the lot.

## Prerequisites

- Git [https://git-scm.com]
- Python [https://www.python.org/downloads/]

## Downloading/Cloning the App

- Users may clone the repository directly through Github by downloading the code.
- Users can also clone the repository by issuing the following command
  ```bash
      git clone https://github.com/AlanAntony1/GroupESoftwareEngineering
  ```
## Running the app or Test Cases

Users may download the app for themselves in order to run locally or run tests.

Then, either open the folder in VSCode and use the built-in terminal or navigate to the folder's location using Terminal or Command Prompt.

```bash
    cd GroupESoftwareEngineering
```

Download all dependencies.

```bash
    pip install -r requirements.txt
```
Running the Applicaton: Enter the following into the terminal window - 

```bash
python manage.py runserver
```

Running the Test Cases: Enter the following into the terminal window - 

```bash
python manage.py test
```

## Roadmap
### Hard Data
Collect all hard data that is necessary e.g lot locations, parking space counts, etc.

Continue to update any data as parking structures and maps change on campus.

### AI 
Create an AI tailored to our specifications

Train the AI on parking behavior of OU Students

Revisit any bugs that arise with test input

Finalize AI for initial small release

Revisit any bugs that arise in initial release

Finalize AI for full release

Continue maintenance based on consumer feedback

### Test Input
Create test input of student schedules to be used by the AI

Expand text input based on test results and increase variety of data, to be repeated multiple times

### App Creation
Design a student-facing app that allows for easy use of the product

Test the app in small batches, release to one college at a time

Fully release the app to all OU students

## Authors and acknowledgement
Jordan Musselman 
| Alan Antony 
| Jason Salinas 
| Aditi Mahangade 
| Reese Zimmerman 
| Elizabeth Glass 
| Anh Nyguen
