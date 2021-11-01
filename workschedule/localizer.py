import locale
import gettext

##
# The Localizer class provides localization services for work schedule user-visible text as well as for error messages.
# It is a Singleton class
#
class Localizer:  
    # root folder 
    localePath = "locales"
     
    # single instance
    singleton = None
    
    ##
    # Construct the Localizer
    def __init__(self):
        Localizer.singleton = self
        self.messages = None
    
    ##
    # Get the single instance of Localizer                
    @staticmethod
    def instance():
        if (Localizer.singleton is None):
            Localizer()
        return Localizer.singleton 
    
    ##
    # get the the language country code from the default locale
    @staticmethod
    def getLC() -> str:
        thisLocale = locale.getdefaultlocale()
        langCC = thisLocale[0]
        return langCC
    
    ##
    # Get the translated error message text for the default locale and country code 
    # 
    # @param msgId Message identifier
    # @return translated text    
    def messageStr(self, msgId: str) -> str:
        if (self.messages is None):
            # translated text for this locale and country code
            self.messages = gettext.translation("schedule", localedir=Localizer.localePath, languages=[Localizer.getLC()])
            self.messages.install()
            
        # Get an error message by its id
        return self.messages.gettext(msgId)
