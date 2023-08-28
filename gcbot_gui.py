import os
import openai
from dotenv import load_dotenv, find_dotenv
import panel as pn  # GUI
pn.extension(loading_spinner='dots', loading_color='#00aa41')
_ = load_dotenv(find_dotenv()) # read local .env file
openai.api_key  = os.getenv('OPENAI_API_KEY')

# context = [{'role': 'system', 'content': """
# You are OrderBot, an automated service to collect orders for a pizza restaurant. \
# You first greet the customer, then collects the order, \
# and then asks if it's a pickup or delivery. \
# You wait to collect the entire order, then summarize it and check for a final \
# time if the customer wants to add anything else. \
# If it's a delivery, you ask for an address. \
# Finally you collect the payment.\
# Make sure to clarify all options, extras and sizes to uniquely \
# identify the item from the menu.\
# You respond in a short, very conversational friendly style. \
# The menu includes \
# pepperoni pizza  12.95, 10.00, 7.00 \
# cheese pizza   10.95, 9.25, 6.50 \
# eggplant pizza   11.95, 9.75, 6.75 \
# fries 4.50, 3.50 \
# greek salad 7.25 \
# Toppings: \
# extra cheese 2.00, \
# mushrooms 1.50 \
# sausage 3.00 \
# canadian bacon 3.50 \
# AI sauce 1.50 \
# peppers 1.00 \
# Drinks: \
# coke 3.00, 2.00, 1.00 \
# sprite 3.00, 2.00, 1.00 \
# bottled water 5.00 \
# """}]  # accumulate messages

context = [{'role': 'system', 'content': """
I will provide you with a link about the employment insurance benefits of the government of Canada. \
Based on the content of this link, I would like you to give me an answer regarding my situation. \
But first, I would like you to ask me some questions to narrow down my case and understand my problem. \
Then, give me the answer based on only the content you can find in this link. Please ask me one question at a time. \
Also, at the end, give me a direct link to where you got the final answer from: https://www.canada.ca/en/employment-social-development/programs/ei/ei-list/reports/digest.html \
"""}]

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

def collect_messages(_):
    prompt = inp.value_input
    inp.value = ''
    context.append({'role': 'user', 'content': f"{prompt}"})
    response = get_completion_from_messages(context)
    context.append({'role': 'assistant', 'content': f"{response}"})
    panels.append(
        pn.Row('User:', pn.pane.Markdown(prompt, width=600)))
    panels.append(
        pn.Row('Assistant:', pn.pane.Markdown(response, width=600, style={'background-color': '#F6F6F6'})))
    return pn.Column(*panels)


inp = pn.widgets.TextInput(value="Hi", placeholder='Enter text here…')
button_conversation = pn.widgets.Button(name="Chat!")
panels = []  # collect display

interactive_conversation = pn.bind(collect_messages, button_conversation)
dashboard = pn.Column(
    inp,
    pn.Row(button_conversation),
    pn.panel(interactive_conversation, loading_indicator=True, height=300),
)
dashboard.servable()

