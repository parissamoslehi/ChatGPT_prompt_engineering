import os
import openai
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())  # read local .env file

openai.api_key = os.getenv('OPENAI_API_KEY')


def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,  # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]


def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,  # this is the degree of randomness of the model's output
    )
    #     print(str(response.choices[0].message))
    return response.choices[0].message["content"]


def run():
    messages = [
        {'role': 'system', 'content': 'You are an assistant that speaks like Shakespeare.'},
        {'role': 'user', 'content': 'tell me a joke'},
        {'role': 'assistant', 'content': 'Why did the chicken cross the road'},
        {'role': 'user', 'content': 'I don\'t know'}]
    response = get_completion_from_messages(messages, temperature=1)
    print(response)

    messages = [
        {'role': 'system', 'content': 'You are friendly chatbot.'},
        {'role': 'user', 'content': 'Hi, my name is Isa'}]
    response = get_completion_from_messages(messages, temperature=1)
    print(response)

    messages = [
        {'role': 'system', 'content': 'You are friendly chatbot.'},
        {'role': 'user', 'content': 'Yes,  can you remind me, What is my name?'}]
    response = get_completion_from_messages(messages, temperature=1)
    print(response)

    messages = [
        {'role': 'system', 'content': 'You are friendly chatbot.'},
        {'role': 'user', 'content': 'Hi, my name is Isa'},
        {'role': 'assistant', 'content': "Hi Isa! It's nice to meet you. \
    Is there anything I can help you with today?"},
        {'role': 'user', 'content': 'Yes, you can remind me, What is my name?'}]
    response = get_completion_from_messages(messages, temperature=1)
    print(response)

    # give the context
    messages = [
        {'role': 'system', 'content': 'You are friendly chatbot.'},
        {'role': 'user', 'content': 'Hi, my name is Isa'},
        {'role': 'assistant', 'content': "Hi Isa! It's nice to meet you. \
    Is there anything I can help you with today?"},
        {'role': 'user', 'content': 'Yes, you can remind me, What is my name?'}]
    response = get_completion_from_messages(messages, temperature=1)
    print(response)


#the system message helps to
# set the behavior and persona of
# the assistant and it acts as
# a high-level instruction for the conversation. So you can think of
# it as whispering in the assistant's ear and guiding its responses
# without the user being aware of the system
# message. So as the user, if you've ever used
# ChatGPT, you probably don't know what's in ChatGPT's system message.
# The benefit of the system message is that it provides you, the
# developer, with a way to frame the conversation without
# making the request itself part of the conversation. So you can
# guide the assistant and
# whisper in its ear and guide its responses without
# making the user aware.

if __name__ == '__main__':
    run()
