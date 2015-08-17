import authomatic
from authomatic.providers import oauth2

CONFIG = {
    'google': {
           
        'class_': oauth2.Google,
        'id': authomatic.provider_id(),

        # Google is an AuthorizationProvider too.
        'consumer_key': os.getenv('GOOGLE_KEY'),
        'consumer_secret': os.getenv('GOOGLE_SECRET'),
        
        # But it is also an OAuth 2.0 provider and it needs scope.
        'scope': ['https://www.googleapis.com/auth/plus.login profile email'],
    }
}
