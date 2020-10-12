from __future__ import print_function
import time
import spoonacular
from spoonacular.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = spoonacular.DefaultApi(spoonacular.ApiClient(configuration))
username = 'dsky' # str | The username.
hash = '4b5v4398573406' # str | The private hash for the username.
inline_object9 = spoonacular.InlineObject9() # InlineObject9 | 

try:
    # Add to Meal Plan
    api_response = api_instance.add_to_meal_plan(username, hash, inline_object9)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->add_to_meal_plan: %s\n" % e)