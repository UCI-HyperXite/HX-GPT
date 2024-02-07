#!/usr/bin/env python
# coding: utf-8

import os
import openai
import tiktoken
from dotenv import load_dotenv, find_dotenv
import panel as pn
_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key  = os.environ['OPENAI_API_KEY']

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output 
    )
    return response.choices[0].message["content"]


##################Test 1######################################
response = get_completion("What is the capital of France?")
print(response)
##############################################################

def get_completion_from_messages(messages, 
                                 model="gpt-3.5-turbo", 
                                 temperature=0, 
                                 max_tokens=500):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
        max_tokens=max_tokens, # the maximum number of tokens the model can ouptut 
    )
    return response.choices[0].message["content"]



##########################Test 2#############################
messages =  [  
{'role':'system', 
 'content':"""You are an assistant who\
 responds in the style of Dr Seuss."""},    
{'role':'user', 
 'content':"""write me a very short poem\
 about a happy carrot"""},  
] 
response = get_completion_from_messages(messages, temperature=1)
print(response)
###############################################################



pn.extension()

panels = [] 

context = [ {'role':'system', 'content':"""
You are a chatbot designed to answer questions about the UCI HyperXite team. The UCI HyperXite team is building a\
scalable hyperloop. Introduce yourself as a bot that will help the user know more about HyperXite. Provide concise answers. Tone: friendly\
and resepctful. Keep it conversational.

Introduce yourself as "Hi, do you have any questions about HyperXite?" Also list out a few questions the user could ask\
Format the list properly.

The team is using a linear induction motor for propulsion. The pod can be controlled from a custom Graphical User Interface\
built by the team.

"""} ]  # can be fine tuned further 


inp = pn.widgets.TextInput(value="Hi", placeholder='Enter text here…')
button_conversation = pn.widgets.Button(name="Chat!")

interactive_conversation = pn.bind(collect_messages, button_conversation)

dashboard = pn.Column(
    inp,
    pn.Row(button_conversation),
    pn.panel(interactive_conversation, loading_indicator=True, height=300),
)

dashboard

