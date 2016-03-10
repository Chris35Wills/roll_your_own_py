import time
import threading
import winsound

def get_out_of_your_chair_timer_WINDOWS(interval_len="15", interval_no="10", duration_min=""):
	
	"""
	interval_len = length of interval in seconds
	interval_no  = number of intervals (USED over duration_min) << PRIOITY
	duration_min = length of total session (ignored if interval_no is set)
	
	"""
	interval_len=3
	interval_no=2
	duration_min=""
	#convert duration to seconds (prioritise interval_no over duration_min)
	if interval_no == "" and duration_min != "":
		dur_seconds=duration_min*60
	elif interval_no != "" and duration_min == "":
		dur_seconds=interval_no*interval_len
	elif interval_no == "" and duration_min == "":		
		sys.exit("Must set either a number of intervals or a session time (in minutes)")
	elif interval_no != "" and duration_min != "":
		print("Basing time on number of intervals rather than session duration value")
		dur_seconds=interval_no*interval_len

	#if interval is duration_min is set, round accordingly so that the number of intervals fits into the time period

	n = dur_seconds/interval_len # currently just rounds to nearest whole interval
	print("Length of session: %i sec(s) (%i min(s))" %((n*interval_len),(n*interval_len)/60.))

	for i in range(n):
		print "Interval %i/%i" %(i+1, n)

		#print interval timer	
		for sec in range(interval_len):
			print("%i/%i seconds" %(sec+1,interval_len))
			if sec != interval_len-1:
				time.sleep(1)

		if i != n-1:
			winsound.Beep(1500,500)
			time.sleep(0.5)
		else:
			winsound.Beep(1500,500)

	winsound.Beep(1000,700)	
	print("End of session")

if __name__ == "__main__":
	print("Run from import")