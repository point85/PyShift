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
        self.units = None
                    
    @staticmethod
    def instance():
        if (Localizer.localizer is None):
            Localizer()
        return Localizer.localizer 
    
    @staticmethod
    def getLC():
        # get the default locale and the language code
        thisLocale = locale.getdefaultlocale("LANGUAGE")
        langCC = thisLocale[0]
        return langCC
    
    ##
    # Get the translated user-visible text for the default locale and country code 
    # 
    # @param msgId Message identifier
    # @return translated text  
    def langStr(self, msgId):        
        if (self.units is None):
            # translated user-visible text for this locale  and country code
            self.units = gettext.translation("lang", localedir=Localizer.localePath, languages=[Localizer.getLC()])
            self.units.install()
        
        # Get a unit name, symbol or description by its id
        return self.units.gettext(msgId)
