# Python program to translate
# speech to text and text to speech


import speech_recognition as sr
import pyttsx3
from pynput.keyboard import Key, Listener


# def OnPress(key):
# 	if key==Key.esc:
# 		return False

# Initialize the recognizer
r = sr.Recognizer()

# Function to convert text to
# speech
def SpeakText(command):
	# Initialize the engine
	engine = pyttsx3.init()
	engine.say(command)
	engine.runAndWait()
	
	
# with Listener(on_press=OnPress) as key_listener:
# 	key_listener.join()

# use the microphone as source for input.
with sr.Microphone() as source2:
	# wait for a second to let the recognizer
	# adjust the energy threshold based on
	# the surrounding noise level
	print('adjusting for ambient noise start')
	r.adjust_for_ambient_noise(source2, duration=5)
	print('adjusting for ambient noise finish')

	# Loop infinitely for user to
	# speak until 'esc' is pressed
	# while(True):
	for i in range(3):
		
		# Exception handling to handle
		# exceptions at the runtime
		try:
			#listens for the user's input
			print('listening ...')
			audio2 = r.listen(source2)
			
			# Using google to recognize audio
			print('processing the record ...')
			MyText = r.recognize_google(audio2)
			MyText = MyText.lower()

			print(f"""Here's what you said: "{MyText}".""")
			SpeakText(MyText)
				
		except sr.RequestError as e:
			print("Could not request results; {0}".format(e))
			
		except sr.UnknownValueError:
			print("unknown error occurred")
