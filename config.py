from authomatic.providers import oauth2

CONFIG = {
    
    'google': {
           
        'class_': oauth2.Google,
        
        # Google is an AuthorizationProvider too.
        'consumer_key': '615316435724-k7gu8chlmqc3gkuru56bamcr4f9pv7sm.apps.googleusercontent.com',
        'consumer_secret': 'gSkFr02eGVLVXrlrRqbfBBN_',
        
        # But it is also an OAuth 2.0 provider and it needs scope.
        'scope': ['https://www.googleapis.com/auth/plus.login profile email'],
    }
}