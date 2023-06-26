# Blumen Geospatial Application

This is the README file for the Blumen systems Geospatial application.

## Introduction

Blumen Geospatial is a web application that allows users to perform spatial analysis on geographic data. It consists of a frontend built with React and a backend built with Python using Flask.

## Installation

### Running with Docker

1. Install Docker on your machine. 

2. Clone the repository to your local machine: <br>
    git clone desired-directory
3. Build and run the Docker containers using Docker Compose:<br>
     cd project-directory
     docker-compose up
   
The frontend container is responsible for running the React-based user interface and handling client-side interactions.

The backend container runs the Flask server and handles API requests, performs spatial analysis, and interacts with the database or external services.

## Important Note

When running the frontend and backend containers together using Docker Compose, you may encounter issues with the communication between them. Although both the frontend and backend work separately, there might be a connectivity problem between the containers when they are run together.

### Running Locally
In order to test and run the application you can run it locally on your system:
make sure you have __PADUS3_0Geopackage_4326.gpkg__ file
1. Download the the PADUS3 file from here: https://drive.google.com/file/d/1l0m-8OXPUPjx7VyTCBQ_3JO4cIlFQ7BA/view?usp=drive_link
after downloading, __place the file in the PADUS3 folder in the root directory__.

2.Activate the virtual environment:
    On macOS and Linux:<br>
        source venv/bin/activate<br>
    On Windows: <br>
        venv\Scripts\activate<br>

3. Install the dependencies for the frontend:
     cd <project-directory>/client
     npm install

4. Install the dependencies for the backend:
     cd <project-directory>
     pip3 install -r requirements.txt

5. Start the backend server:
    cd <project-directory>
    python3 main.py

6. Start the frontend development server:
    cd <project-directory>/client
    npm start
   
This will start the frontend application and open it in a web browser.

7. Access the application by opening your web browser and navigating to http://localhost:3000.

  ## Note
To run the application locally, make sure to update the URL in both the __setupProxy.js__ and __App.js__ files. In the __handleSubmit__ function of App.js, change the URL to __http://localhost:5001/api/overlap__. Similarly, in the setupProxy.js file, update the target URL to __http://localhost:5001__. This ensures that the frontend communicates with the locally running backend server.

  ## Note
  When entering coordinates in the text area on the frontend, ensure to follow this format:
  ensure that each pair of latitude and longitude is on a new line, and separate the latitude and    longitude values with a comma. Do not include any square brackets or commas at the end of each     line. 
  
  for example:<br>
-105.00432014465332, 39.96167604831683<br>
-105.00715255737305, 39.95868749291691<br>
-105.00921249389647, 39.95948888179304<br>
-105.01067161560059, 39.9602543440034<br>
-105.01195907592773, 39.9607242332767<br>
-105.00989913940431, 39.96321407936762<br>
-105.00758171081543, 39.96275549363738<br>
-105.00432014465332, 39.96167604831683<br>


### Running Tests (Pytest)
To run the tests, make sure you have the dependencies installed. You can then run the tests using the following command:
  in the root directory run : pytest -s tests/test_.py
  
## Test Cases
The project includes test cases to ensure the correctness of the implementation for calcualting the AOI overlap for 1) small polygons and 2) polygons with no overlap

## Backend Code and Handling Large AOI requests (Flask)
The calculate_overlap function in the utilities.py takes a GeoJSON representation of the Area of Interest (AOI) as input and calculates the overlap with the PAD-US dataset. Here's how it handles different scenarios:

No overlap: If there is no overlap between the AOI and the PAD-US data, the function returns a dictionary with the message "No overlap found."

Large AOI size: If the AOI size exceeds a predefined limit (US_SIZE), the function logs a warning message and returns an error indicating that the AOI size exceeds the limit. This serves as a reminder to make the AOI smaller.

Very large AOI size: If the AOI size exceeds another limit (FOUR_STATES_SIZE CA_OR_NV_WA), the function logs a warning message indicating that it is a very large AOI. This is for informational purposes to alert the user about the size of the AOI being processed.  

AOI size within limits: If the AOI size is within the acceptable limits, the function proceeds with calculating the overlap.

## Calculation for each Categories
For each category (Mang_Type, FeatClass, Des_Tp) in the PAD-US dataset, the function utilities.py calculates the total area of overlap and the percentage overlap for each category. It also accounts for categories in PAD-US that did not appear in the overlap, assigning a 0% overlap for those categories.

## Frontend Code (React)
The frontend code uses React hooks to manage state variables for user input and interpretation results. It sends a POST request to the backend API with entered coordinates and displays the interpretation results to the user.

## Testing the API endpoint with Postman or a similar tool
If you want to test the api endpoint http://127.0.0.1:5001/api/overlap you can use these sample data:

__No Overlap:__

{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Polygon",
        "coordinates": [
          [
            [-105.00432014465332, 39.96167604831683],
            [-105.00715255737305, 39.95868749291691],
            [-105.00921249389647, 39.95948888179304],
            [-105.01067161560059, 39.9602543440034],
            [-105.01195907592773, 39.9607242332767],
            [-105.00989913940431, 39.96321407936762],
            [-105.00758171081543, 39.96275549363738],
            [-105.00432014465332, 39.96167604831683]
          ]
        ]
      },
      "properties": {}
    }
  ]
}

__very Large AOI:__

{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {},
      "geometry": {
        "type": "Polygon",
        "coordinates": [
          [
            [-125.0, 24.3963],
            [-125.0, 49.3845],
            [-66.9346, 49.3845],
            [-66.9346, 24.3963],
            [-125.0, 24.3963]
          ]
        ]
      }
    }
  ]
}

__AOI that Exceeds the Limit:__

{
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {},
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [-130, 10],
                        [-130, 60],
                        [-60, 60],
                        [-60, 10],
                        [-130, 10]
                    ]
                ]
            }
        }
    ]
}






