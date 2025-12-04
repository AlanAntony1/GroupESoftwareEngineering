# To - Do

Task: Housing Lot Locator - Aditi Mahangade\
Description: Feature that locates closest parking lot based on location for housing students at OU. Uses some of the same data as the parking lot locator.
Acceptance Criteria: Page displays clear instructions, includes a drop down of housing locations, and successfully stores uploaded data
Page has instructions, upload button, and file successfully stores.

Task: Gather Parking Data - Jordan Musselman\
Description: Collect and format data on available parking spaces.\
Acceptance Criteria: Dataset is stored, cleaned, and accessible for app features.

Task: Output Closest Lots Based on Schedule Data - Jordan Musselman\
Description: Return to the user the closests parking lots to each of their classes based on parking pass type\
Acceptance Criteria: Parking lot is displayed to user for each class location entered

Task: Create Tests for Parking Lot Outputs - Jordan Musselman\
Description: Test that correct parking lots are returned to the user based on distance from their class and parking pass type\
Acceptance Criteria: All tests pass

Task: Google Maps Integration - Jason Salinas\
Description: Embed Google Maps showing campus with parking locations.\
Acceptance Criteria: Users can zoom, pan, and see parking locations pinned along with highlighted open spots.


Task: Parking History -Elizabeth Glass\
Description: Add the ability for a history to be added to and seen once a user starts viewing building and parking distances.\
Acceptance Criteria: Once a building is picked and "show info" button is hit add the building to a parking history list. 


# In Progress

Task: User Class Schedule Page Display - Jordan Musselman\
Description: Design a user facing web page for the user to enter and see their class schedule data.\
Acceptance Criteria: Classes can be added to the web page, are saved, and appear formatted to the user.


Task: Create Tests for Housing Model - Aditi Mahangade\
Description: Write and run unit tests for the Housing model to ensure correct behavior of methods and data validation.
Acceptance Criteria: All Housing model test cases execute successfully with no errors.

Task: 
# Complete

Task: Create a Model for Parking History
Description: Made a model for parking data.  
Acceptance Criteria: Model was successfully created and migrated. 

Task: Create Tests for Parking History
Description: Test for all equivalences parts in the parkingLotHistory model. 
Acceptance Criteria: Test cases for lot history executes and passes.

Task: Create Unit for Schedule Input - Jordan Musselman\
Description: Add unit to the project that will be used for users to enter their class schedules\
Acceptance Criteria: Unit is created with appropriate files and is successfully pushed to GitHub

Task: Create a Model for Class Input - Jordan Musselman\
Description: Make a model with fields for all class data and added to web page\
Acceptance Criteria: Model is added to web pages and added class inputs can be viewed on page

Task: Create Tests for Class Input Model - Jordan Musselman\
Description: Test for all equivalence partitions in the ClassInput model fields\
Acceptance Criteria: Tests all pass successfully

Task: Create Model for buildings -Alan Antony\
Description: Added a building model that contains the distance and address to its closest parking lot.\
Acceptance Criteria: Model appears in Django Admin Page.

Task: Created Tests for building mode -Alan Antony\
Description: Test for equivalence partitions within building model.\
Acceptance Criteria: Tests all pass successfully.

Task: Create a Parking Lot Locator -Alan Antony\
Description: Allows a user to select a building and gives the assosciated information from the model\
Acceptance Criteria: User is able to select a building and the correct matchin information is given.

Task: Connect GitHub to Visual Studio - All team members\
Description: Ensure repo is cloned and project builds in VS.\
Acceptance Criteria: Team can pull/push code; project compiles without errors.

Task: Create a basic blank web app & server - Alan Antony\
Description: Set up a running web server with placeholder homepage.\
Acceptance Criteria: Web app runs locally

Task: Deploy basic app on cloud platform - Alan Antony\
Description: Set up deployment on an AWS server.\
Acceptance Criteria: App is fully functional and accessible through AWS.

Task: Implement Continiuous Deployment - Alan Antony\
Description: Set up a protocol that updates website whenever GitHub is pushed too.\
Acceptance Criteria: Change made in GitHub is updated on AWS Server.


Task: Create Tests for Highlight Button model - Jason Salinas\
Description: Test for all User input of the button and if it holds the correct state.
Acceptance Criteria: Tests all pass

Task: Create a Model for available lots - Reese Zimmermann\
Description: Initialized a Django app that runs a single test case for lot availability. Implemented model with basic fields to represent parking lot data and verified functionality through the initial unit test.\
Acceptance Criteria: Model successfully created and migrated; test case for lot availability executes and passes.


Task: Add Housing Model - Aditi Mahangade\
Description: Created a model for housing data including fields for housing name, closest parking, and distance.
Acceptance Criteria: Model successfully added to Django, migrated, and visible in the admin panel.

Task: AI Schedule Matcher - Reese Zimmermann\
Description: Build AI feature to recommend best parking based on user schedule and data.\
Acceptance Criteria: Given an uploaded schedule, system outputs suggested parking with >70% accuracy on test cases.

Task: Establish fields for AvailableLots - Reese Zimmermann\
Description: Implement AvailableLots model with validated fields for lot name, total spaces, and available spaces, ensuring accurate and consistent parking lot data.
Acceptance Criteria: Migrations generate successfully, and invalid values (negative or exceeding total spaces) are rejected during model validation.

Task: Implement Business Logic for AvailableLots - Reese Zimmermann\
Description: Added business logic to update lot availability, compute occupancy rate, and manage lot status in alignment with expected system behavior.
Acceptance Criteria: Local tests for the model logic pass.
