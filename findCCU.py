import itertools
from subprocess import Popen,PIPE,STDOUT
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

def testRedundancy(redundancy,adapterslotN,fecN,ringN):
	lineRed = "ProgramTest.exe -adapterslot %d -fec %d -ring %d %s" % (adapterslotN,fecN,ringN,redundancy,)
	lineReset = "ProgramTest.exe -adapterslot %d -fec %d -ring %d -reset" % (adapterslotN,fecN,ringN,)
	lineScan = "ProgramTest.exe -adapterslot %d -fec %d -ring %d -scanCCU" % (adapterslotN,fecN,ringN,)
	p = Popen(lineReset.split(),stdout=PIPE,stdin=PIPE,stderr=PIPE)
	stdout_reset = p.communicate(input='')
	nRed = 0
	while True:
		p = Popen(lineRed.split(),stdout=PIPE,stdin=PIPE,stderr=PIPE)
		stdout_red = p.communicate(input='')
		if "FEC SR0 = 0x5c80" in stdout_red[0] or "FEC SR0 = 0x4c90" in stdout_red[0]: break
		if nRed > 10: return -1
		nRed += 1
	nScan = 0
	while True:
		p = Popen(lineScan.split(),stdout=PIPE,stdin=PIPE,stderr=PIPE)
		stdout_scan = p.communicate(input='')
		if not "ERROR" in stdout_scan[1]:
			break
		nScan += 1
		if nScan > 10: return -2
	p = Popen(lineReset.split(),stdout=PIPE,stdin=PIPE,stderr=PIPE)
	stdout_reset = p.communicate(input='')
	return 0


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
	if ring.outA:
		outputline += "A-"
	else:
		outputline += "B-"
	if ring.inA:
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
	dummyind = ii+1
	if ring.CCUs[dummyind] and not ring.CCUs[dummyind-1]:
		outputline += "0x7e-B-A"
	return outputline

def analyzeRing(ring,ccuAnalysis,test):
	for ii,nbad in ccuAnalysis.iteritems():
		if not ring.CCUs[ii]:
			if test != 0: ccuAnalysis[ii][0] = ccuAnalysis[ii][0] + 1
			else: ccuAnalysis[ii][1] = ccuAnalysis[ii][1] + 1
	return
	
def main():
	#
	#ccus = ["0x1","0x2","0x48","0x55","0x41","0xd","0x16","0x56"]
	#ccus = ["0x1","0x2","0x60","0x5f","0x68","0x2d","0x1b"]
	ccus = ["0x1","0x2","0x76","0xe","0x22"]
	fecN=4
	ringN=8
	adapterN=1
	#ccus = ["0x6f","0x5f","0x7b","0x3f"]

	ccuAnalysis = dict()
	for ii,ccu in enumerate(ccus): ccuAnalysis[ii] = [0,0]

	sequences = itertools.product((True,False),repeat = len(ccus)+1)
	nBad = 0
	for sequence in sequences:
		for j in range(0,4):
			ring = makeRing(sequence,j)
			if checkRing(ring):
				redundancy = printRedundancyCommand(ccus,ring)
				line = "ProgramTest.exe -adapterslot %d -fec %d -ring %d %s" % (adapterN,fecN,ringN,redundancy,)
				test = testRedundancy(redundancy,adapterN,fecN,ringN)
				print test,line
				if test != 0:
					nBad += 1
				analyzeRing(ring,ccuAnalysis,test)

	print nBad
	for ii,ccu in enumerate(ccus): print ccu,ccuAnalysis[ii]

	#for i in range(1,9):
	#	nGood = 0
	#	sequences = itertools.product((True,False),repeat = i+1)
	#	for sequence in sequences:
			#print sequence
	#		for j in range(0,4):
	#			if checkRing(makeRing(sequence,j)): nGood += 1
	#	print i,nGood
	return

if __name__  == "__main__":
	main()
