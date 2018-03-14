 # appengine_config.py
from google.appengine.ext import vendor
from google.appengine.api import app_identity

app_id = app_identity.get_application_id()

headers = {}

#Set your local, stage,qa and prod app url's here
#The links here are example ul's and don't work 
if app_id == 'booking-users-stage':
	project_url = 'https://booking-users-stage.appspot.com/'
	headers['DEBUG_APP_ID'] = 'booking-users-stage'
elif app_id == 'booking-users-qa':
	project_url = 'https://booking-users-qa.appspot.com/'
	headers['DEBUG_APP_ID'] = 'booking-users-qa'
elif app_id == 'booking-users-prod':
	project_url = 'https://booking-users-prod.appspot.com/'
else:
	#else loop for local environment
	project_url = 'https://booking-users-stage.appspot.com'
	headers['DEBUG_APP_ID'] = 'booking-users-stage'