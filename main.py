
'''
This is a google app engine setup to do basic Get, Patch, Post Rest Api Calls
'''
from google.appengine.api import urlfetch
import webapp2
import logging
import json
import urllib

from appengine_config import project_url
from appengine_config import headers
from appengine_config import app_id

#Get Rest Api call to fetch booking info by providing booking ID
class GetBookingByID(webapp2.RequestHandler):

    def get(self):
        
        headers['Content-Type'] = 'application/json'
        headers['Access-Control-Allow-Origin'] = '*'
        
        booking_id =self.request.GET.get('booking_id')
        get_url = project_url + '/api/v2/bookings/' + booking_id
        
        try:
            result = urlfetch.fetch(get_url, headers=headers, follow_redirects=False)
            
            if result.status_code == 200:
                self.response.headers['Content-Type'] = 'application/json'
                opt_dictionary = json.loads(result.content)
                return json.dump(opt_dictionary, self.response.out)
            elif result.status_code == 404 or result.status_code == 500:
                error_dict = {'error' : 'No Record found for booking ' + booking_id}
                return json.dump(error_dict,self.response.out)
            else:
                self.response.out.write(result.content)
        except urlfetch.Error:
            logging.exception('Caught exception fetching url')
            error_dict = {'error' : 'Caught exception fetching url'}
            return json.dump(error_dict,self.response.out)

#Get Rest Api call to fetch Traveller info by providing traveller ID
class GetTravellerByEmail(webapp2.RequestHandler):
    
    def get(self):

        headers['Content-Type'] = 'application/json'
        headers['Access-Control-Allow-Origin'] = '*'

        #Sample Url = http://localhost:8080/get_traveller/?email=testing123@gmail.com&&booking_id=9999999
        #Check if the booking_id is passed in the url

        if self.request.method == 'GET' and 'booking_id' in self.request.GET:
            booking_id = self.request.get('booking_id')
        else:
            output_dict = {'error' : 'Event Id is required field' }
            return json.dump(output_dict,self.response.out)

        if self.request.method == 'GET' and 'email' in self.request.GET:
            email = self.request.GET.get('email')
        else:
            output_dict = {'error' : 'Email is required field' }
            return json.dump(output_dict,self.response.out)

        get_url = project_url + '/api/v2/bookings/' + booking_id + '/travellers/' + email
        
        try:
            result = urlfetch.fetch(get_url,headers=headers,follow_redirects=False)
            if result.status_code == 200:
                self.response.headers['Content-Type'] = 'application/json'
                opt_dictionary = json.loads(result.content)
                return json.dump(opt_dictionary, self.response.out)
            elif result.status_code == 404:
                error_dict = {'error' : 'No Record found for email ' + email + ' for booking id ' + booking_id}
                return json.dump(error_dict,self.response.out)

            else:
                error_dict = {'error' : 'Server Error Code ' + result.status_code}
                return json.dump(error_dict,self.response.out)
        except urlfetch.Error:
            logging.exception('Caught exception fetching url')
    
#Get call to fetch list of all travellers for a given booking
class getListOfTravellers(webapp2.RequestHandler):

    def get(self):
        
        headers['Content-Type'] = 'application/json'
        booking_id = self.request.get('booking_id')

        if booking_id == '':
            output_dict = {'error' : 'Event Id is required field' }
            return json.dump(output_dict,self.response.out)
        get_url = project_url + '/api/v2/bookings/' + booking_id + '/travellers/'
        try:
            result = urlfetch.fetch(get_url, headers = headers, follow_redirects=False)
            self.response.headers['Content-Type'] = 'application/json'
            opt_dictionary = json.loads(result.content)
            return json.dump(opt_dictionary, self.response.out)
        except urlfetch.Error:
            logging.exception('Caught exception fetching url')

#Get call to fetch list of all bookings
class getEvents(webapp2.RequestHandler):

    def get(self):
        
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        get_url = project_url + '/api/v2/bookings/'
        try:
            result = urlfetch.fetch(get_url, headers = headers, follow_redirects=False)
            self.response.headers['Content-Type'] = 'application/json'
            opt_dictionary = json.loads(result.content)
            return json.dump(opt_dictionary, self.response.out)
        except urlfetch.Error:
            logging.exception('Caught exception fetching url')

#Patch Api call for appending traveller info by email
class patchTravellerByEmail(webapp2.RequestHandler):

    def post(self):

        input_dict = json.loads(self.request.body)
        #Performing check for required fields
        if 'Email' in input_dict:
            email = input_dict["Email"]
        elif 'email' in input_dict:
            email = input_dict["email"]
        else:
            output_dict = {'error' : 'Email is required field' }
            return json.dump(output_dict,self.response.out)

        if 'booking_id' in input_dict:
            booking_id = input_dict["booking_id"]
        else:
            output_dict = {'error' : 'Event Id is required field' }
            return json.dump(output_dict,self.response.out)


        patch_url = project_url + '/api/v2/bookings/' + booking_id + '/travellers/' + email

        headers['Content-Type'] = 'application/json'
        
        try:
            result = urlfetch.fetch(
                url=patch_url,
                payload=self.request.body,
                method=urlfetch.PATCH,
                headers=headers,
                follow_redirects=False)
            if result.status_code == 200:
                output_dict = {'success' : 'OK '}
            else:
                output_dict = {'error' : result.status_code }
            return json.dump(output_dict,self.response.out)
        except urlfetch.Error:
            logging.exception('Caught exception fetching url')

class defaultPage(webapp2.RequestHandler):
    
    def get(self):
        self.response.out.write('Home Page')

#This is the internal routing mapping Url to respective function
app = webapp2.WSGIApplication([
	('/',defaultPage),
    ('/travellers_list/',getListOfTravellers),
    ('/get_booking_by_id/', GetBookingByID),
    ('/get_traveller/', GetTravellerByEmail),
    ('/get_bookings/', getBookings),
    ('/patch_traveller_info/', patchTravellerByEmail)
], debug=True)

def main():
	app.run()

if __name__ == "__main__":
	main()