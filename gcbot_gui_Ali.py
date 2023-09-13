import os
import openai
from dotenv import load_dotenv, find_dotenv
import panel as pn
pn.extension(loading_spinner='dots', loading_color='#00aa41')
_ = load_dotenv(find_dotenv())  # read local .env file
openai.api_key = os.getenv('OPENAI_API_KEY')

# Task 1: Rephrase the context. Possible confliction of enquiry.
context = [{'role': 'assistant', 'content': """
This is an Assistant of the Government of Canada.
"""},

           {'role': 'system', 'content': """
Here is a set of links provided in curly brackets that contain information about employment insurance benefits of the government of Canada.; \
url links: {https://www.canada.ca/en/employment-social-development/programs/ei/ei-list/reports/digest.html};

The link provided above contains 25 url links as chapters and each chapter has subsections. These 25 chapters cover different topics related to employment insurance benefits of the government of Canada. \

You are a professional chatbot. Answer questions based on the content of the links that I provided above. Please provide reference and your link to the subsection that you used to answer the question from the provided links. \
Start your conversation with greetings. But first before I start asking my questions, I would like you to ask me some questions to narrow down my case and understand my situation to better answer my questions. When asking me the questions, please ask one question at a time.\
Please keep in mind, when you ask me questions to understand my situation you should keep it relevant to the contents from the given link and give options for the correct answer type in 1-2 words bullet points. The same applies to the answers you provide. \
At any step you think I'm not eligible to benefit from the services, let me know that I'm not eligible with mentioning the reason and the link to the page noting the reason. \
If you finally think I'm eligible help me to apply for the relevant benefit by telling me which type of benefit I'm eligible to apply for together with documents I need to collect.\
"""}]

# Global parameters.
model_to_use = "gpt-4"
temperature = 0.0


def get_completion_from_messages(messages, model=model_to_use, temperature=temperature):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,  # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]


def collect_messages(event):
    if event.new:
        prompt = event.new  # Use the event.new attribute to get the updated text from the TextInput widget
        context.append({'role': 'user', 'content': f"{prompt}"})
        response = get_completion_from_messages(context)
        context.append({'role': 'assistant', 'content': f"{response}"})
        panels.append(
            pn.Row('User:', pn.pane.Markdown(prompt, width=600)))
        panels.append(
            pn.Row('Assistant:', pn.pane.Markdown(response, width=600, styles={'background-color': '#F6F6F6'})))

        return pn.Column(*panels)


inp = pn.widgets.TextInput(value="Hi", placeholder='Enter text here…', width=600)

# Use the on_change event to trigger the chat function when "Enter" is pressed
inp.on_change('value', collect_messages)

panels = []  # collect display

dashboard = pn.Column(
    pn.Column("./logo_cgi_color_jpg.jpg"),
    pn.Column(
        pn.Row(
            pn.panel(inp, width=600),
            scroll=True,
            height=750,
            width=850
        )
    ),
    width=1000
)
dashboard.servable()
