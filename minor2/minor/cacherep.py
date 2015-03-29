import os
import datetime

class replace:

#	len1=len(os.listdir("/home/varsha/Desktop/CD/minor/cache4"))	
	userdata={} 
	'''	
	def __init__(self):
		userdata={}
		self.updatedict()
	'''

	

#cache4='/home/varsha/Desktop/CD/minor/cache4/'
	

    #no. of files in cache4
	def modification_date(self,filename):
		t = os.path.getmtime('/home/varsha/Desktop/CD/minor/cache4/'+filename)
    		return datetime.datetime.fromtimestamp(t)

	def updatedict(self):
		for key in os.listdir('/home/varsha/Desktop/CD/minor/cache4/'):
          		self.userdata[key]=self.modification_date(key)


#updatedict()
#print len(userdata)

"""
while len1 >2:
     
	 min1=min(userdata,key=userdata.get)
	 del userdata[min1]
	 print '\n'
         os.remove("/home/varsha/Desktop/CD/minor/cache4/"+min1)
	 print "min1 removed"
	 print '\n'
         
         print userdata
	 print len(userdata)

	 len1=len(os.listdir("/home/varsha/Desktop/CD/minor/cache4/"))

print 'size less'
"""
