#import edge_tts
#import asyncio
#import re
#import os
#import playsound
#
#def preprocess_text(text):
    # Remove emojis or replace with words
#    text = re.sub(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F700-\U0001F77F]', '', text)
#    return text
#
#async def speak_async(text):
#    try:
 #       clean_text = preprocess_text(text)
  #      audio_file = "vynix_response.mp3"
#
 #       # Set up Edge TTS
  #      communicate = edge_tts.Communicate(text=clean_text, voice="en-US-JennyNeural")  # Customize voice here
   ##
     #   # Play the audio file
      #  playsound.playsound(audio_file)
#
 #       # Clean up
  #      os.remove(audio_file)
   # except Exception as e:
    #    print(f"Error with TTS: {e}")
#
#def speak(text):
    # Run the asynchronous speak function
 #   asyncio.run(speak_async(text)) 

Work in progress
