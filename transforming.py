import openai
import os

from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())  # read local .env file

openai.api_key = os.getenv('OPENAI_API_KEY')


def get_completion(prompt,
                   model="gpt-3.5-turbo"):  # Andrew mentioned that the prompt/ completion paradigm is preferable for this class
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,  # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]


def translate(input_text):
    prompt = f"""
    Translate the following English text to Spanish: \ 
    ```{input_text}```
    """
    response = get_completion(prompt)
    print(response)


def detect_language(input_text):
    prompt = f"""
    Tell me which language this is: 
    ```{input_text}```
    """
    response = get_completion(prompt)
    print(response)


def translate_into_three_languages(input_text, language_1, language_2, language_3):
    prompt = f"""
    Translate the following  text to {language_1} and {language_2}
    and {language_3}: \
    ```{input_text}```
    """
    response = get_completion(prompt)
    print(response)


def translate_into_formal_and_informal(input_text, language):
    prompt = f"""
    Translate the following text to {language} in both the \
    formal and informal forms: 
    '{input_text}'
    """
    response = get_completion(prompt)
    print(response)


def universal_translator(input_list, language_1, language_2):
    for issue in input_list:
        prompt = f"Tell me what language this is: ```{issue}```"
        lang = get_completion(prompt)
        print(f"Original message ({lang}): {issue}")

        prompt = f"""
        Translate the following  text to {language_1} \
        and {language_2}: ```{issue}```
        """
        response = get_completion(prompt)
        print(response, "\n")


def translate_slang_tone_to_business(input_text):
    prompt = f"""
    Translate the following from slang to a business letter: 
    '{input_text}'
    """
    response = get_completion(prompt)
    print(response)


def convert_json_to_html(input_json):
    prompt = f"""
    Translate the following python dictionary from JSON to an HTML \
    table with column headers and title: {input_json}
    """
    response = get_completion(prompt)
    print(response)
    from IPython.display import display, Markdown, Latex, HTML, JSON
    display(HTML(response))


def run():
    translate("Hi, I would like to order a blender")
    detect_language("Combien coûte le lampadaire?")
    translate_into_three_languages("I want to order a basketball", "French", "Spanish", "English pirate")
    translate_into_formal_and_informal("Would you like to order a pillow?", "Spanish")
    universal_translator(
        ["La performance du système est plus lente que d'habitude.",  # System performance is slower than normal
         "Mi monitor tiene píxeles que no se iluminan.",  # My monitor has pixels that are not lighting
         "Il mio mouse non funziona",  # My mouse is not working
         "Mój klawisz Ctrl jest zepsuty",  # My keyboard has a broken control key
         "我的屏幕在闪烁"  # My screen is flashing
         ], "English", "Korean")
    # translate_slang_tone_to_business("Dude, This is Joe, check out this spec on this standing lamp.")
    convert_json_to_html({"resturant employees": [
        {"name": "Shyam", "email": "shyamjaiswal@gmail.com"},
        {"name": "Bob", "email": "bob32@gmail.com"},
        {"name": "Jai", "email": "jai87@gmail.com"}
    ]})
    lst_text = [
        "The girl with the black and white puppies have a ball.",  # The girl has a ball.
        "Yolanda has her notebook.",  # ok
        "Its going to be a long day. Does the car need it’s oil changed?",  # Homonyms
        "Their goes my freedom. There going to bring they’re suitcases.",  # Homonyms
        "Your going to need you’re notebook.",  # Homonyms
        "That medicine effects my ability to sleep. Have you heard of the butterfly affect?",  # Homonyms
        "This phrase is to cherck chatGPT for speling abilitty"  # spelling
    ]
    spellcheck_grammar_check_list_of_text(lst_text)
    text = f"""
    Got this for my daughter for her birthday cuz she keeps taking \
    mine from my room.  Yes, adults also like pandas too.  She takes \
    it everywhere with her, and it's super soft and cute.  One of the \
    ears is a bit lower than the other, and I don't think that was \
    designed to be asymmetrical. It's a bit small for what I paid for it \
    though. I think there might be other options that are bigger for \
    the same price.  It arrived a day earlier than expected, so I got \
    to play with it myself before I gave it to my daughter.
    """
    spellcheck_grammar_check_text(text)
    proofread_and_correct_in_APA_style(text)


def spellcheck_grammar_check_list_of_text(input_list):
    for t in input_list:
        prompt = f"""Proofread and correct the following text
        and rewrite the corrected version. If you don't find
        and errors, just say "No errors found". Don't use 
        any punctuation around the text:
        ```{t}```"""
        response = get_completion(prompt)
        print(response)


def spellcheck_grammar_check_text(input_text):
    prompt = f"proofread and correct this review: ```{input_text}```"
    response = get_completion(prompt)
    print(response)


def proofread_and_correct_in_APA_style(input_text):
    prompt = f"""
    proofread and correct this review. Make it more compelling. 
    Ensure it follows APA style guide and targets an advanced reader. 
    Output in markdown format.
    Text: ```{input_text}```
    """
    response = get_completion(prompt)
    print(response)


if __name__ == '__main__':
    run()

# Requires-Python >=3.8
# from redlines import Redlines
#
# diff = Redlines(text, response)
# display(Markdown(diff.output_markdown))
