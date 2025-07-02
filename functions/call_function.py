import os
import sys
from google import genai
from google.genai import types

def call_function(function_call_part, verbose=False):

    if verbose:
        # print the function name and args
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
