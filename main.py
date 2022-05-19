import requests
from datetime import datetime
import smtplib
import config
import time

# Email and password stored in another file
MyEmail = config.Email
MyPass = config.Pass
MyLat = 40.712776 # your latitude
MyLong = -74.005974 # your longitude

# API pull
def is_iss_overhead():
    response = requests.get(url='http://api.open-notify.org/iss-now.json')
    response.raise_for_status()
    data = response.json()

    latitude = float(data['iss_position']['latitude'])
    longitude = float(data['iss_position']['longitude'])

    #Your position is within +5 or -5 degrees of the iss position.
    if (MyLat-5 <= latitude <= MyLat+5) and (MyLong-5 <= longitude <= MyLong+5):
        return True
    


def is_night():
    parameters = {
        'lat': MyLat,
        'lng': MyLong,
        'formatted': 0,
    }
    response = requests.get(url='https://api.sunrise-sunset.org/json', params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data['results']['sunrise'].split('T')[1].split(':')[0])
    sunset = int(data['results']['sunset'].split('T')[1].split(':')[0])
    
    time_now = datetime.now().hour
    
    if time_now >= sunset or time_now <= sunrise:
       return True

# If the ISS is close to my current position 
# and it is currently dark 
# then send me an email to tell me to look up.
# Run the code every 60 seconds.

while True:
    time.sleep(60)
    if is_iss_overhead() and is_night():
        connection = smtplib.SMTP('smtp.gmail.com')
        connection.starttls()
        connection.login(MyEmail, MyPass)
        connection.sendmail(
            from_addr=MyEmail,
            to_addrs=MyEmail,
            msg='Subject: Look Up . The ISS is above you in the sky!'
        )