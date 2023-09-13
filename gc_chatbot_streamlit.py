import openai
import streamlit as st
from streamlit_chat import message
import os

# Setting page title and header
# st.set_page_config(page_title="ESDC - EI BOT ", page_icon=":robot_face:")
st.set_page_config(page_title="ESDC - EI BOT ", page_icon='./CGI_compressed_logo.png')
st.markdown("<h1 style='text-align: center;'>ESDC-EI Chatbot</h1>", unsafe_allow_html=True)

# Set org ID and API key
openai.organization = "org-BDtFUFeLKZgRZ9yHCM9MQPRV"
openai.api_key = os.getenv('OPENAI_API_KEY')

# GUI
user_avatar = 'app/static/unisex_avatar.png'
bot_avatar = 'app/static/logo_cgi_color.png'

# Initialise session state variables
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []
if 'messages' not in st.session_state:
    st.session_state['messages'] = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]
if 'model_name' not in st.session_state:
    st.session_state['model_name'] = []
if 'cost' not in st.session_state:
    st.session_state['cost'] = []
if 'total_tokens' not in st.session_state:
    st.session_state['total_tokens'] = []
if 'total_cost' not in st.session_state:
    st.session_state['total_cost'] = 0.0

# Sidebar - let user choose model, show total cost of current conversation, and let user clear the current conversation
st.sidebar.title("Sidebar")
model_name = st.sidebar.radio("Choose a model:", ("GPT-3.5", "GPT-4"))
counter_placeholder = st.sidebar.empty()
counter_placeholder.write(f"Total cost of this conversation: ${st.session_state['total_cost']:.5f}")
clear_button = st.sidebar.button("Clear Conversation", key="clear")

# Map model names to OpenAI model IDs
if model_name == "GPT-3.5":
    model = "gpt-3.5-turbo"
else:
    model = "gpt-4"

# reset everything
if clear_button:
    st.session_state['generated'] = []
    st.session_state['past'] = []
    st.session_state['messages'] = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]
    st.session_state['number_tokens'] = []
    st.session_state['model_name'] = []
    st.session_state['cost'] = []
    st.session_state['total_cost'] = 0.0
    st.session_state['total_tokens'] = []
    counter_placeholder.write(f"Total cost of this conversation: ${st.session_state['total_cost']:.5f}")


# generate a response
def generate_response(prompt):
    st.session_state['messages'].append({"role": "user", "content": prompt})

    completion = openai.ChatCompletion.create(
        model=model,
        messages=st.session_state['messages']
    )
    response = completion.choices[0].message.content
    st.session_state['messages'].append({"role": "assistant", "content": response})

    # print(st.session_state['messages'])
    total_tokens = completion.usage.total_tokens
    prompt_tokens = completion.usage.prompt_tokens
    completion_tokens = completion.usage.completion_tokens
    return response, total_tokens, prompt_tokens, completion_tokens

# container for chat history
response_container = st.container()
# container for text box
container = st.container()

with container:
    st.session_state['messages'].append(
        {'role': 'assistant', 'content': 
        """This is an Assistant of Goverment of Canada."""
        })
    st.session_state['messages'].append(
        {'role': 'system', 'content': """
        Here is a set of links provided in curly brackets that contain information about employment insurance benefits of the government of Canada.; \
        url links: {https://www.canada.ca/en/employment-social-development/programs/ei/ei-list/reports/digest.html};

        The link provided above contains 25 url links as chapters and each chapter has subsections.\
        These 25 chapters covers different topics related to employment insurance benefits of the government of Canada.\

        You are a professional chatbot. Answer questions based on the content of the links that I provided above. \
        Please provide reference and ur link of the subsection that you used to answer the question from the provided links. \
        Start your conversation with greetings. But first before I start asking my questions, I would like you to ask me some questions to narrow down my case and understand my situation to better answer my questions.\
        When asking me the questions, please ask one question at a time. Please keep in mind, when you ask me questions to understand my situation you should keep it relevant to the contents from the given link and give options for the correct answer type in 1-2 words bullet points.\
        The same applies to the answers you provide. At any step you think I'm not eligible to benefit from the servises, let me know that I'm not eligible with mentioning the reason and the URL link ending in ".html" to the page noting the reason. \
        If you finally think I'm eligible help me to apply for the relevant benefit by telling me which type of benefit I'm eligible to apply for together with documetns I need to collect.\
        """}
    )

    with st.form(key='my_form', clear_on_submit=True):
        user_input = st.text_area("You:", key='input', height=100)
        submit_button = st.form_submit_button(label='Send')

    if submit_button and user_input:
        output, total_tokens, prompt_tokens, completion_tokens = generate_response(user_input)
        st.session_state['past'].append(user_input)
        st.session_state['generated'].append(output)
        st.session_state['model_name'].append(model_name)
        st.session_state['total_tokens'].append(total_tokens)

        # from https://openai.com/pricing#language-models
        if model_name == "GPT-3.5":
            cost = total_tokens * 0.002 / 1000
        else:
            cost = (prompt_tokens * 0.03 + completion_tokens * 0.06) / 1000

        st.session_state['cost'].append(cost)
        st.session_state['total_cost'] += cost

if st.session_state['generated']:
    with response_container:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state["past"][i], is_user=True, key=str(i) + '_user', logo=f'{user_avatar}')
            message(st.session_state["generated"][i], key=str(i), logo=f'{bot_avatar}')
            st.write(
                f"Model used: {st.session_state['model_name'][i]}; Number of tokens: {st.session_state['total_tokens'][i]}; Cost: ${st.session_state['cost'][i]:.5f}")
            counter_placeholder.write(f"Total cost of this conversation: ${st.session_state['total_cost']:.5f}")