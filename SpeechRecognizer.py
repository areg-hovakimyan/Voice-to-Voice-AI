import speech_recognition as sr
import time

class SpeechRecognizer:
    """
    A class for real-time speech recognition using the Google Web Speech API.

    Attributes:
        recognizer (sr.Recognizer): The speech recognition engine.
        text_final (str): The final recognized text.
        last_time (float): Timestamp of the last recognized speech.
        language (str): The language code for speech recognition.
    """

    def __init__(self, language="hy-AM"):
        """
        Initializes the SpeechRecognizer with a specified language.

        Args:
            language (str): The language code for recognition (default is Armenian: "hy-AM").
        """
        self.recognizer = sr.Recognizer()
        self.text_final = ""  # Store the final recognized text
        self.last_time = time.time()  # Track the last recognition time
        self.language = language  # Set the language for recognition

    def set_language(self, language: str):
        """
        Sets the language for speech recognition.

        Args:
            language (str): The new language code (e.g., "en-US" for English, "fr-FR" for French).
        """
        self.language = language
        print(f"Language set to: {self.language}")

    def recognize_speech(self, source) -> str:
        """
        Captures and recognizes speech from the microphone.

        Args:
            source: The microphone input source.

        Returns:
            str: The recognized text if successful, otherwise an empty string.
        """
        try:
            audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=30)
            print("Recognizing speech...")

            # Recognize speech using Google Web Speech API in the selected language
            text = self.recognizer.recognize_google(audio, language=self.language)
            return text

        except sr.WaitTimeoutError:
            print("Listening timed out. Please try again.")
        except sr.RequestError:
            print("API request error. Please check your connection.")
        except sr.UnknownValueError:
            print("Speech not recognized. Could not understand audio.")

        return ""

    def listen_continuously(self) -> str:
        """
        Continuously listens for speech until a long silence is detected (default 5 seconds).

        Returns:
            str: The final recognized text after the session.
        """
        with sr.Microphone() as source:
            while True:
                print("Listening for speech...")
                recognized_text = self.recognize_speech(source)

                if recognized_text:
                    self.text_final += recognized_text + ' '  # Append recognized text with a space
                    self.last_time = time.time()  # Reset silence timer
                    print(f"Current Recognized Text:\n{self.text_final}")

                # Stop listening after 5 seconds of silence
                if time.time() - self.last_time > 1:
                    print("No speech detected for a while, stopping the function.")
                    break

        return self.text_final  # Return the final recognized text