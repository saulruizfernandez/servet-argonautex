from gps import*
session = gps()
session.stream(WATCH_ENABLE|WATCH_NEWSTYLE)

while True:
	report = session.next()
	if list(report.keys())[0] == 'exp' :
		lat = float(report['lat'])
		lon = float(report['lon'])
		print("lat=%f\tlon=%f\ttime=%s" % (lat, lon, report['time']))
		time.sleep(0.5)

