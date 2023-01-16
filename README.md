# CityScout: Neighbourhood Recommender
This App recommends neighborhoods in a city based on user preferences.
- Users: People that are looking to move into a new neighborhood
- Need: There are a lot of pros and cons for different cities, towns, etc so it gets difficult to 
choose the right place. Prospective tenants need a solution that can optimize their 
preferences. For example, a tenant would want a quiet neighborhood, close access to a 
subway, and nearby a dog friendly park.
- Solution: Using a recommendation system will help narrow down options for people 
without having to discover places the long way around.

Demo Link: https://youtu.be/WPYWaYYD9aM

| |
|:-------------------------:|
|<h3><b>1. GPT-powered website that helps users find places that suite their needs</b></h3> <img src="images/i1.jpg"/> | 
|<h3><b>2. Enter up to 5 preferences regarding the neighbourhood you want to shift to</b></h3> <img src="images/i2.jpg"/> |
|<h3><b>3. Choose and learn more from the recommended locations</b></h3> <img src="images/i3.jpg"/> | 
|<h3><b>4. Learn how each location suits your requirements and preferences</b></h3> <img src="images/i4.jpg"/> |
|<h3><b>5. Compare each location based on your preferences to help you shortlist</b></h3> <img src="images/i5.jpg"/> | 
|<h3><b>6. Find out pros and cons for living in each suggested neighbourhood to make an informed decision</b></h3> <img src="images/i6.jpg"/> |

### Configuration Details
  This app uses OpenAI api for recommending neighbourhoods. <br>
  1. Get access by creating an account here: https://openai.com/api <br>
  2. Enter your openAI API key in the `gpt.py` file. <br>
      `openai.api_key = ""` <br>
      
      OR <br>
      
     Give the api key through command line while running the application. <br>
     `openai.api_key = os.getenv('openai_key')` <br>

### Steps to Run
  #### 1. Install virtualenv
    py -2 -m pip install virtualenv

  #### 2. Create Environment
    mkdir <project name>
    cd <project name>

  #### 3. Activate Environment
    <name of environment>\Scripts\activate

  #### 4. Install Flask
    pip install Flask
  
  #### 5. Set FLASK_APP environment variable.
    setx FLASK_APP "server.py"

  #### 6. Run the application
    flask run 
    or  
    python server.py

