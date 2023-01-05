import random
import json
from flask import Flask
from flask import render_template
from flask import Response, request, jsonify, render_template, redirect, url_for
from gpt import *
app = Flask(__name__)

# Global Variables

# list of areas suggested by GPT
gpt_areas = []
preferences = []
city = ""

def display():
  print(f"GPT Areas: {gpt_areas}")
  print(f"Preferences: {preferences}")
  print(f"City: {city}")

# ROUTES
@app.route('/')
def home():
  return render_template('home.html')

@app.route('/input')
def input():
  return render_template('input.html')


@app.route('/areas')
def areas():
  return render_template('areas.html', gpt_areas = gpt_areas)

# this route will return the top 5 areas according to user preferences
@app.route('/suggested_areas', methods=['GET', 'POST'])
def suggested_areas():
    '''
    Data format to be followed:
    json_data = {
          "user_input": {
              "city": "Seattle",
              "preferences": ["close to downtown", 
                  "near bustling nightlife",
                  "close to high quality restaurants"]
          }
      }
    '''
    global city, preferences, gpt_areas
    json_data = request.get_json() 
    data = json_data["user_input"]
    city = data["city"]
    city = str(city).title()
    preferences = data["preferences"]
    preferences = list(map(lambda p:p.title(), preferences))
    while True:
      try:
        _, results = list5areas(city, preferences)
        gpt_areas = []
        print(f"Results: {results}")
        print(f"Type: {type(results)}")
        n = len(results)
        if n!=5 or '/' in results or '' in results:
          raise GPTError
        pattern = r'[^a-zA-z\' ]'
        for area in results:
          area = re.sub(pattern, '', area)
          area = area.strip()
          gpt_areas.append(area)
        break
      except GPTError:
        print("Ill-formed GPT response")
    print(f"gpt areas = {gpt_areas}")
    return jsonify(gpt_areas = gpt_areas)

# this route will return more info on a particular area and how it satisfies each of the user preferences
@app.route('/area/<id>', methods=['GET', 'POST'])
def area(id):
  global gpt_areas
  '''
  Data format to be followed:
  preferences = ["close to downtown", 
                "near bustling nightlife",
                 "close to high quality restaurants"]
  '''
  print("gpt_areas: ", gpt_areas)
  print("preferences: ", preferences)
  area_name = gpt_areas[int(id)]
  print(area_name)
  while(True):
    try:
      _, more_info = elaborateArea(area_name, preferences)
      print(f"Results: {more_info}")
      print(f"Type: {type(more_info)}")
      if not isinstance(more_info, str):
        raise GPTError
      more_info = ' '.join(more_info.strip().split())
      break
    except GPTError:
        print("Ill-formed GPT response")
  print(f"Final Result: {more_info}")

  # a dictionary to store preference:examples as key value pairs for this area
  pref_reasons = dict()
  for p in preferences:
    pref_reasons[p] = getExamplesForPreference(area_name, p)
  print(f"Final Pref Result: {pref_reasons}")

  # send the string and dictionary results back 
  return render_template('area.html', n_name = area_name, more_info = more_info, pref_reasons = pref_reasons)

@app.route('/preferences')
def display_preferences():
  global preferences
  return render_template('preferences.html', preferences=preferences)

# this route will return comparisons of each area with respect to a particular preference
@app.route('/compare/<id>', methods=['GET', 'POST'])
def compare(id):
  global preferences
  print(preferences)
  pref = preferences[int(id)]
  print(f"Preference chosen: {pref}")
  while(True):
    try:
      _, result = rateAreasAccToPref(gpt_areas, pref, city)
      print(f"Results: {result}")
      print(f"Type: {type(result)}")
      if not isinstance(result, list):
        raise GPTError
      # cleaning the GPT response
      result = " ".join(result)
      result = result.strip().split(".")
      lines = len(result)
      print(f"lines:{lines}")
      if lines < 4:
        raise GPTError
      comparisons = []
      pattern = r'[()\]\[{}0-9]#'
      for i in result:
        i = re.sub(pattern, '', i)
        i = re.sub(' +', ' ', i)
        i = i.strip()
        if len(i.split()) < 4:
          continue
        if i!="":
          comparisons.append(i)
      break
    except GPTError:
        print("Ill-formed GPT response")
  print(f"Final Pref Result: ")
  print(comparisons)
  return render_template('comparisons.html', pref = pref, gpt_comparisons = comparisons)

# this route will return areas to pick pros and cons
@app.route('/prosconslist')
def proscons_list():
    global city, preferences, gpt_areas
    # send the list of areas back
    return render_template('prosconslist.html', gpt_areas = gpt_areas)

# this route will return pros and cons of user chosen area
@app.route('/proscons/<id>', methods=['GET', 'POST'])
def proscons(id):
  area = gpt_areas[int(id)]
  while(True):
    try:
      prompt, result = getProsOfArea(area, city)
      print(f"Results: {result}")
      print(f"Type: {type(result)}")
      print(f"Prompt: {prompt}")
      if not isinstance(result, list):
        raise GPTError
      pros = []
      #pattern = r'[^a-zA-z ]'
      pattern = r'[.()\]\[{}0-9]#'
      for i in result:
        i = re.sub(pattern, '', i)
        i = i.strip()
        if (i!=""):
          pros.append(i)
      break
    except GPTError:
        print("Ill-formed GPT response")
  print("\n")
  while(True):
    try:
      prompt, result = getConsOfArea(area, city)
      print(f"Results: {result}")
      print(f"Type: {type(result)}")
      print(f"Prompt: {prompt}")
      if not isinstance(result, list):
        raise GPTError
      cons = []
      #pattern = r'[^a-zA-z ]'
      pattern = r'[.()\]\[{}0-9]#'
      for i in result:
        i = re.sub(pattern, '', i)
        i = i.strip()
        if (i!=""):
          cons.append(i)
      break
    except GPTError:
        print("Ill-formed GPT response")
  print(f"Final Pref Result: ")
  print("pros")
  print(pros)
  print("cons")
  print(cons)
  return render_template('proscons.html', n_name = area, pros = pros, cons = cons)

@app.route('/end')
def display_end():
  return render_template('end.html', city = city)

if __name__ == '__main__':
    app.run(debug=True,port=3000)

   
