import locale
import gettext

##
# The Localizer class provides localization services for work schedule user-visible text as well as for error messages.
#
class Localizer:  
    # root folder 
    localePath = "locales"
     
    # single instance
    localizer = None
    
    def __init__(self):
        Localizer.localizer = self
        self.messages = None
                    
    @staticmethod
    def instance():
        if (Localizer.localizer is None):
            Localizer()
        return Localizer.localizer 
    
    @staticmethod
    def getLC():
        # get the default locale and the language code
        thisLocale = locale.getdefaultlocale()
        langCC = thisLocale[0]
        return langCC
    
    ##
    # Get the translated error message text for the default locale and country code 
    # 
    # @param msgId Message identifier
    # @return translated text    
    def messageStr(self, msgId):
        if (self.messages is None):
            # translated text with error messages for this locale and country code
            self.messages = gettext.translation("messages", localedir=Localizer.localePath, languages=[Localizer.getLC()])
            self.messages.install()
            
        # Get an error message by its id
        return self.messages.gettext(msgId)
