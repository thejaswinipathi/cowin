import http.client
import mimetypes
import json
import time
import datetime
import os


today = datetime.date.today()
tomo = today + datetime.timedelta(days=1)
day_after = today + datetime.timedelta(days=2)
today_str = today.strftime('%d-%m-%Y')
tomo_str = tomo.strftime('%d-%m-%Y')
day_after_str = day_after.strftime('%d-%m-%Y')	
# The notifier function
def notify(title, subtitle, message):
    t = '-title {!r}'.format(title)
    s = '-subtitle {!r}'.format(subtitle)
    m = '-message {!r}'.format(message)
    os.system('terminal-notifier {} -sound "Glass"'.format(' '.join([m, t, s])))

# Calling the function
def check_avail(date):
	conn = http.client.HTTPSConnection("cdn-api.co-vin.in")
	payload = ''
	headers = {
	  'Content-Type': 'application/json'
	}
	response = conn.request("GET", "/api/v2/appointment/sessions/calendarByDistrict?district_id=294&date="+date, payload, headers)
	res = conn.getresponse()
	data = res.read()
	result = data.decode("utf-8")
	reply = json.loads(result)
	centers = reply['centers']
	for center in centers:
		for session in center["sessions"]:
			min_age_limit = session["min_age_limit"]
			if min_age_limit == 18:
				if session["available_capacity_dose1"] != 0:
					notify(title    = center["name"],
					       subtitle = str(center["pincode"]) + " doses are " +str(session["available_capacity_dose1"]),
					       message  = session["date"])
					print("========================================================================================================================================")
					print("Vaccination available at %s", center["name"])
					print("========================================================================================================================================")
					print("session details are %s", session)
					print("========================================================================================================================================")
					print("center details are %s", center)
					print("========================================================================================================================================")
					print("################################################################################################################################################")
while(True):
	try:
		check_avail(today_str)
		time.sleep(3)
	except Exception as e:
		print("Exception occurred %s", e)
		print("date is %s", today_str)
		time.sleep(3)
	try:
		check_avail(tomo_str)
		time.sleep(3)
	except Exception as e:
		print("Exception occurred %s", e)
		print("date is %s", tomo_str)
		time.sleep(3)
	# try:
	# 	check_avail(day_after_str)
	# 	time.sleep(3)
	# except Exception as e:
	# 	print("Exception occurred %s", e)
	# 	print("date is %s", day_after_str)
