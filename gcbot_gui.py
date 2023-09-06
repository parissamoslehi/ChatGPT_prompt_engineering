import os
import openai
from dotenv import load_dotenv, find_dotenv
import panel as pn  # GUI
pn.extension(loading_spinner='dots', loading_color='#00aa41')
_ = load_dotenv(find_dotenv()) # read local .env file
openai.api_key = os.getenv('OPENAI_API_KEY')

# Task 1: Rephrase the context. Possible confliction of enquiry. 
context = [{'role': 'assistant', 'content': """
This is an Assistant of Goverment of Canada.
"""
}, 

{'role': 'system', 'content': """
Here is a set of links provided in curly brackets that contain information about employment insurance benefits of the government of Canada.
 
url links: {https://www.canada.ca/en/employment-social-development/programs/ei/ei-list/reports/digest.html}

The link provided above contains 25 url links as chapters and each chapter has subsections.\
 These 25 chapters covers different topics related to employment insurance benefits of the government of Canada.\
 
You are a professional chatbot. Answer questions based on the content of the links that I provided above.\
 Please provide reference and ur link of the page that you used to answer the question from the provided links.\
 Start your conversation with greetings. When the user asks a question and you find different factors impacting the answer,\
 provide the list of the factors, and then ask them ony by one to narrow down the case and find the answer.
"""}]#\
#  Please keep in mind, when you ask me questions to understand my situation you should keep it relevant to the contents from the given link.\
#  The same applies to the answers you provide. \

# Global parameters.
model_to_use = "gpt-4"
temperature = 0.1

def get_completion_from_messages(messages, model=model_to_use, temperature=temperature):
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
        pn.Row('Assistant:', pn.pane.Markdown(response, width=600, styles={'background-color': '#F6F6F6'})))

    return pn.Column(*panels)


inp = pn.widgets.TextInput(value="Hi", placeholder='Enter text here…', width=600)
button_conversation = pn.widgets.Button(name="Chat!")
panels = []  # collect display

interactive_conversation = pn.bind(collect_messages, button_conversation)
dashboard = pn.Column(
                pn.Column("./logo_cgi_color_jpg.jpg"),
                pn.Column(
                    pn.Row(
                        pn.panel(interactive_conversation, loading_indicator=True, height=300),
                        scroll=True,
                        height=750,
                        width=850 
                        ),
                    pn.Row(inp, button_conversation)
                ),
                width=1000
)
dashboard.servable()

