import itertools
from subprocess import call
class Ring:
	def __init__(self,n):
		self.inA = True
		self.outA = True
		self.CCUs = []
		for i in range(0,n):
			self.CCUs.append(True)
		return
	def setCCU(self,i,b):
		if i >= len(self.CCUs): return
		self.CCUs[i] = b
		return
	def setInA(self,b):
		self.inA = b
		return
	def setOutA(self,b):
		self.outA = b
		return

def makeRing(sequence,mode):
	ring = Ring(len(sequence))
	for i,b in enumerate(sequence):
		ring.setCCU(i,b)
	if mode == 1:
		ring.setInA(False)
	elif mode == 2:
		ring.setOutA(False)
	elif mode == 3:
		ring.setInA(False)
		ring.setOutA(False)
	return ring

def testRedundancy(redundancy,fecN,ringN):
	lineRed = "-fec %d -ring %d %s" % (fecN,ringN,redundancy,)
	lineReset = "-fec %d -ring %d -reset" % (fecN,ringN,)
	lineScan = "-fec %d -ring %d -scanCCU" % (fecN,ringN,)
	call(["ProgramTest.exe",lineReset])
	call(["ProgramTest.exe",lineRed])
	call(["ProgramTest.exe",lineScan])

def checkRing(ring):
	if len(ring.CCUs) < 2: return False
	if ring.inA and not ring.CCUs[0]: return False
	if not ring.inA and not (ring.CCUs[0] or ring.CCUs[1]): return False
	if ring.outA and ring.CCUs[-1]: return False
	if ring.outA and not ring.CCUs[-2]: return False
	if not ring.outA and not ring.CCUs[-1]: return False
	for i in range(0,len(ring.CCUs)-2):
		if not ring.CCUs[i] and not ring.CCUs[i+1]: return False
	return True

def printRedundancyCommand(ccus,ring):
	outputline = "-redundancy  FEC-"
	#print ring.inA,ring.outA,len(ring.CCUs)
	if ring.inA:
		outputline += "A-"
	else:
		outputline += "B-"
	if ring.outA:
		outputline += "A "
	else:
		outputline += "B "
	for ii,address in enumerate(ccus):
		ccuin = "A"
		ccuout = "A"
		if not ring.CCUs[ii]: continue
		if ii == 0 and not ring.inA:
			ccuin = "B"
		if ii > 0 and not ring.CCUs[ii-1]:
			ccuin = "B"
		if not ring.CCUs[ii+1]:
			ccuout = "B"
		if ii+1 == len(ccus) and not ring.outA:
			ccuout = "B"
		elif ii+1 == len(ccus) and ring.outA:
			ccuout = "A"
		if ccuin == "A" and ccuout == "A": continue
		outputline += address+"-"+ccuin+"-"+ccuout+" "
	return outputline

#
#ccus = ["0x1","0x2","0x48","0x55","0x41","0xd","0x16","0x56"]
fecN=16
ringN=1
ccus = ["0x6f","0x5f","0x7b","0x3f"]

sequences = itertools.product((True,False),repeat = len(ccus)+1)
for sequence in sequences:
	for j in range(0,4):
		ring = makeRing(sequence,j)
		if checkRing(ring):
			redundancy = printRedundancyCommand(ccus,ring)
			line = "ProgramTest.exe -fec %d -ring %d %s" % (fecN,ringN,redundancy,)
			print line
#for i in range(1,9):
#	nGood = 0
#	sequences = itertools.product((True,False),repeat = i+1)
#	for sequence in sequences:
#		#print sequence
#		for j in range(0,4):
#			if checkRing(makeRing(sequence,j)): nGood += 1
#	print i,nGood
	
