#!/usr/bin/python
'''
Most of this code is not mine I got it from a git hub repository which can be found (https://github.com/scottbrady91/Python-Email-Verification-Script).
But as of December 2016 the code has been changed to reflect a pull request on github.

The original coder wrote this for Python 3 but I was able to make it work in 2.7 since I
just didn't want to upgrade to Python 3. I commented out the parts that made the program crash
on my Linux system. I have no idea if this will work on a Windows Machine and don't plane to 
test it on one. Windows 8 cured me of my Windows addiction and I will never go back, good riddence.

This modification was prompted by my need to validate a large list of emails and the original code
only allowed one email at a time through raw_input(), asside from that I have not deleted any portion
of the orignal code. My solution is probably not the most ellegant looking but it does work. 

I am not that great at coding and it's usually a trial and error process but I keep plugging away at it until
it works the way I want it to. The biggest challenge for me on this project was getting the function to accept
a valid email with out the server throwing up an error. 

The original code had no error trapping so I had to fix that as well especially when an invalid domain came up
and the program would crash.

While I have set it so that it will process 100 emails and quit, I don't know if it will be wise to go higher than that
or if 100 is a safe number. Use at your own risk.
'''

#import re
import socket
import smtplib
import dns.resolver
import time

# Address used for SMTP MAIL FROM command  
fromAddress = 'corn@bt.com'

#Part of original code not working in 2.7, at least not for me.
# Simple Regex for syntax checking
#regex = '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$'

email = ''
count = 0
n_emails = 0

#Funtion to validate email
def getemail():
	
	# Email address to verify
	inputAddress = email.strip()
	addressToVerify = str(inputAddress)
	
	#Part of original code not working in 2.7, at least not for me.
	# Syntax check
	#match = re.match(regex, addressToVerify)
	#if match == None:
	#	print('Bad Syntax')
	#	raise ValueError('Bad Syntax')

	# Get domain for DNS lookup
	splitAddress = addressToVerify.split('@')
	domain = str(splitAddress[1])
	print('Domain:', domain)

	# MX record lookup
	try:
		records = dns.resolver.query(domain, 'MX')
		mxRecord = records[0].exchange
		mxRecord = str(mxRecord)
	except:
		print ('Bad')
		with open('bad.txt', 'a') as b:
			b.write(addressToVerify +'\n')
		with open('checked.txt', 'a') as c:
			c.write(addressToVerify +'\n')
		pass
	else:

		# Get local server hostname
		host = socket.gethostname()

		# SMTP lib setup (use debug level for full output)
		server = smtplib.SMTP()
		server.set_debuglevel(0)
		try:
			# SMTP Conversation
			server.connect(mxRecord)
			server.helo(host)
			server.mail(fromAddress)
			code, message = server.rcpt(str(addressToVerify))
			server.quit()
		except:
			#If there is an error write to bad file and continue
			print ('Bad')
			with open('bad.txt', 'a') as b:
				b.write(addressToVerify +'\n')
			pass
		else:
			print(code)
			print(message)

			# Assume SMTP response 250 is success
			# And write good emails to one file and bad to another file
			#Then write all emails checked to a file.
			if code == 250:
				print('Success')
				with open('good.txt', 'a') as f:
					f.write(addressToVerify +'\n')
				with open('checked.txt', 'a') as c:
					c.write(addressToVerify +'\n')
			elif code == '':
				print ('Bad')
				with open('bad.txt', 'a') as b:
					b.write(addressToVerify +'\n')
				with open('checked.txt', 'a') as c:
					c.write(addressToVerify +'\n')
			else:
				print ('Bad')
				with open('bad.txt', 'a') as b:
					b.write(addressToVerify +'\n')
				with open('checked.txt', 'a') as c:
					c.write(addressToVerify +'\n')

#Loop through text file
with open('tocheck.txt') as f:

	for line in f:
		email = line
		getemail()
		count += 1
		n_emails += 1
		time.sleep(10)

		#Wait 30 seconds and reset counter to zero
		if count == 6:
			time.sleep(30)
			count = 0
		
		#Wait one minute before resuming and terminate after 100 emails
		if n_emails == 20:
			time.sleep(60)
		elif n_emails == 40:
			time.sleep(60)
		elif n_emails == 60:
			time.sleep(60)
		elif n_emails == 40:
			time.sleep(60)
		elif n_emails == 100:
			print '100 Emails processed ending for now.'
			raise SystemExit
			
