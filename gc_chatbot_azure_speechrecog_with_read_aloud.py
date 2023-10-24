import openai, pyttsx3
import streamlit as st
from streamlit_chat import message
# import os
import speech_recognition as sr


# Setting page title and header
st.set_page_config(page_title="ESDC - EI BOT ", page_icon='./CGI_compressed_logo.png')
st.markdown("<h1 style='text-align: center;'>ESDC-EI Chatbot</h1>", unsafe_allow_html=True)

# Set org ID and API key
# openai.organization = os.getenv('OPENAI_ORGANIZATION')
openai.api_key = "0a66929660e540109d6018844a972748"
openai.api_version = "2023-05-15"
openai.api_base = "https://wbu-gpt-4.openai.azure.com/"
openai.api_type = "azure"

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

# model = "WBU-GPT-4"
model = "WBU-GPT-35"
wait_time=0.5


class voice_input():
    def __init__(self, t=1, language="en-US") -> None:
        self.language = language
        self.r = sr.Recognizer()
        self.source = sr.Microphone()
        with self.source as source:
            self.r.adjust_for_ambient_noise(source=source, duration=t)
        pass

    def take_voice_input(self):
        # r = sr.Recognizer()
        # mic = sr.Microphone()
        # with mic as source:
        #     r.adjust_for_ambient_noise(source)
        with self.source as source:
            audio = self.r.listen(source=source)

        return self.r.recognize_google(audio, language=self.language)
    
    def speak_text(self, text):
	
        # Initialize the engine
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    
# generate a response
def generate_response(prompt):
    st.session_state['messages'].append({"role": "user", "content": prompt})

    completion = openai.ChatCompletion.create(
        engine=model,
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

vi = voice_input(t=wait_time, language="en-US")

with container:
    st.session_state['messages'].append(
        {'role': 'assistant', 'content': 
        """This is an Assistant of Goverment of Canada."""
        })

    st.session_state['messages'].append(
        {'role': 'system', 'content': """
        Here is a set of links provided in curly brackets that contain information about employment insurance benefits of the government of Canada.; \
        url links: {https://www.canada.ca/en/employment-social-development/programs/ei/ei-list.html; \
                    https://www.canada.ca/en/employment-social-development/programs/ei/ei-list/overpayments/repayments.html; \
                    https://www.canada.ca/en/services/benefits/ei/ei-regular-benefit.html; \
                    https://www.canada.ca/en/services/benefits/ei.html; \
                    https://www.canada.ca/en/services/benefits/ei/caregiving.html};

        The link provided above contains 25 url links as chapters and each chapter has subsections.\
        These 25 chapters covers different topics related to employment insurance benefits of the government of Canada.\

        You are a professional chatbot. Answer questions based on the content of the links that I provided above. \
        Please provide reference and ur link of the subsection that you used to answer the question from the provided links. \
        Start your conversation with greetings. 
        The same applies to the answers you provide. At any step you think I'm not eligible to benefit from the servises, let me know that I'm not eligible with mentioning the reason and the URL link ending in ".html" to the page noting the reason. \
        If you finally think I'm eligible help me to apply for the relevant benefit by telling me which type of benefit I'm eligible to apply for together with documetns I need to collect.\
        """}
    )  

    with st.form(key='my_form', clear_on_submit=True):
        user_input = st.text_area("You:", key='input', height=100)
        submit_button = st.form_submit_button(label='Send')
        microphone_button = st.form_submit_button(label='Voice_input')
        read_aloud_button = st.form_submit_button(label='Read aloud')

    if submit_button and user_input:
        output, total_tokens, prompt_tokens, completion_tokens = generate_response(user_input)
        st.session_state['past'].append(user_input)
        st.session_state['generated'].append(output)
    if microphone_button:
        voice_registered = vi.take_voice_input()
        print(voice_registered)
        output, total_tokens, prompt_tokens, completion_tokens = generate_response(voice_registered)
        st.session_state['past'].append(voice_registered)
        st.session_state['generated'].append(output)
        # vi.speak_text(text=output)

    if read_aloud_button:
        try:
            vi.speak_text(text=st.session_state["generated"][-1])
        except:
            pass


if st.session_state['generated']:
    with response_container:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state["past"][i], is_user=True, key=str(i) + '_user', logo=f'{user_avatar}')
            message(st.session_state["generated"][i], key=str(i), logo=f'{bot_avatar}')
        # if microphone_button:
        #     vi.speak_text(text=output)