from deep_translator import GoogleTranslator

class Translator:
    """
    A class to handle translation using the Google Translator API.
    
    Attributes:
        source_lang (str): The language code of the source language. Default is 'auto' (auto-detect).
        target_lang (str): The language code of the target language. Default is 'en' (English).
    """
    
    def __init__(self, source_lang='auto', target_lang='en'):
        """
        Initializes the Translator object with source and target languages.
        
        Args:
            source_lang (str): The language code for the source language (default is 'auto').
            target_lang (str): The language code for the target language (default is 'en').
        """
        self.source_lang = source_lang
        self.target_lang = target_lang

    def translate(self, text):
        """
        Translates the given text from the source language to the target language.
        
        Args:
            text (str): The text to be translated.
        
        Returns:
            str: The translated text.
        """
        translated_text = GoogleTranslator(source=self.source_lang, target=self.target_lang).translate(text)
        return translated_text
