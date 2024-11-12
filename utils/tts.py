from gtts import gTTS
import os
import playsound

def speak(phrase):
    """Speaks phrase based on given input.

    Parameters
    ----------
    phrase : str
        The phrase in english text.

    Returns
    -------
    None
    """

    # Create gTTS object
    tts = gTTS(text=phrase, lang='en', slow=False)
    
    # Save the speech to a temporary file
    temp_file = 'temp_audio.mp3'
    tts.save(temp_file)
    
    # Play the saved audio file
    playsound.playsound(temp_file)
    
    # Optionally, remove the temporary file after playback
    os.remove(temp_file)

if __name__ == "__main__":
    speak(input())