from numpy import true_divide
import openai
import textwrap as tw
import re
import os
# from dotenv import load_dotenv
from pprint import pprint

# load_dotenv
# openai api_key
openai.api_key = os.getenv('openai_key')


class GPTError(Exception):
  pass

def documentResult(input, prompt, result, topic=""):
  prompt = "\n".join(tw.wrap(prompt))
  print("\n****************************************************************************************") 
  print(f"\nInput: {input}")
  print(f"Prompt: {prompt}")
  if topic != "":
    print(topic)
  pprint(result)
  print("\n****************************************************************************************\n")

# Step 1: Given city and list of preferences, generate list of areas
def list5areas(city, preferences):
  prompt = f"List 5 residential areas in {city} that match the following preferences: \n"
  for pref in preferences:
    prompt += "- " + pref + "\n"
  prompt += "."
  completion = openai.Completion.create(engine="text-davinci-002", max_tokens=256, prompt=prompt)
  results = re.split('\n', completion.choices[0].text.strip())
  return prompt, results

# Step 2: Elaborate how selected area matches preferences
def elaborateArea(area, preferences):
  n = len(preferences)
  prompt = f"Explain in detail the reasons why {area} matches the preferences: \n"
  for pref in preferences:
    prompt += "- " + pref + "\n"
  prompt += f" with atleast {n} examples."
  completion = openai.Completion.create(engine="text-davinci-002", max_tokens=256, prompt=prompt)
  results = "\n".join(tw.wrap(completion.choices[0].text.strip()))
  return prompt, results

# Step 3: Generate specific buildings that demonstrate the preference in the area
def generateExamples(area, preference):
  prompt = f"\nGive specific examples on how {area} fulfills the quality: {preference}."
  completion = openai.Completion.create(engine="text-davinci-002", max_tokens=256, prompt=prompt)
  results = "\n".join(tw.wrap(completion.choices[0].text.strip()))
  return prompt, results

# Step 4: Rate the areas according to preferences
def rateAreasAccToPref(areas, pref, city):
  prompt = f"Rate and compare the following areas: {areas} in {city} based on the preference: {pref} with examples"
  completion = openai.Completion.create(engine="text-davinci-002", max_tokens=500, prompt=prompt)
  results = re.split('\n', completion.choices[0].text.strip())
  return prompt, results

# Step 5: Give pros and cons of the area with explanations 
def giveProsAndCons(area, city):
  prompt = f"List 4 pros and cons of living in {area} in {city} with explanations."
  completion = openai.Completion.create(engine="text-davinci-002", max_tokens=256, prompt=prompt)
  results = re.split('\n', completion.choices[0].text.strip())
  return prompt, results

def getProsOfArea(area, city):
  prompt = f"List and explain 4 pros of living in {area} in {city} with numbering."
  completion = openai.Completion.create(engine="text-davinci-002", max_tokens=256, prompt=prompt)
  results = re.split('\n', completion.choices[0].text.strip())
  return prompt, results

def getConsOfArea(area, city):
  prompt = f"List and explain 4 cons of living in {area} in {city} with numbering."
  completion = openai.Completion.create(engine="text-davinci-002", max_tokens=256, prompt=prompt)
  results = re.split('\n', completion.choices[0].text.strip())
  return prompt, results


def getExamplesForPreference(area, pref):
  while(True):
    try:
      _, result = generateExamples(area, pref)
      print(f"Results: {result}")
      print(f"Type: {type(result)}")
      if not isinstance(result, str):
        raise GPTError
      result = ' '.join(result.strip().split())
      break
    except GPTError:
        print("Ill-formed GPT response")
  return result
