class TranslateUK:
    def __init__(self):
        from google.cloud import translate
        self.target = 'uk'
        self.tc = translate.Client()

    def get(self, text):
        target = self.target
        translation = self.tc.translate(
            text,
            target_language=target)
        return translation['translatedText']
