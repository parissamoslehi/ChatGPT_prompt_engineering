import os
import openai
from dotenv import load_dotenv, find_dotenv
import panel as pn  # GUI
pn.extension(loading_spinner='dots', loading_color='#00aa41')
_ = load_dotenv(find_dotenv()) # read local .env file
openai.api_key  = os.getenv('OPENAI_API_KEY')

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

