from subprocess import Popen,PIPE,STDOUT

resetline="ProgramTest.exe -adapterslot 1 -fec 4 -ring 8 -reset"
#redundancyline="ProgramTest.exe -adapterslot 1 -fec 4 -ring 7 -redundancy  FEC-B-B 0x1-B-A 0x2-A-B 0x5f-B-A 0x68-A-B 0x1b-B-B"
#redundancyline="ProgramTest.exe -adapterslot 1 -fec 4 -ring 7 -redundancy FEC-B-A 0x5f-A-B 0x2d-B-B 0x7e-B-A"
redundancyline="ProgramTest.exe -adapterslot 1 -fec 4 -ring 8 -redundancy FEC-A-A 0x76-A-B 0x22-B-A"
scanline="ProgramTest.exe -adapterslot 1 -fec 4 -ring 8 -scanCCU"
#p = Popen(["ProgramTest.exe","-fec","16","-ring","1","-reset"],stdout=PIPE,stdin=PIPE,stderr=PIPE)
p = Popen(resetline.split(),stdout=PIPE,stdin=PIPE,stderr=PIPE)
stdout_data = p.communicate(input='')[0]
print stdout_data
#p = Popen(["ProgramTest.exe","-fec","16","-ring","1","-redundancy","FEC-B-A","0x5f-B-A"],stdout=PIPE,stdin=PIPE,stderr=PIPE)
#p = Popen(["ProgramTest.exe","-fec","16","-ring","1","-redundancy","FEC-A-B","0x3f-A-B"],stdout=PIPE,stdin=PIPE,stderr=PIPE)
nRed = 0
while True:
    p = Popen(redundancyline.split(),stdout=PIPE,stdin=PIPE,stderr=PIPE)
    stdout_data = p.communicate(input='')[0]
    print stdout_data
    if "FEC SR0 = 0x5c80" in stdout_data or "FEC SR0 = 0x4c90" in stdout_data: break
    if nRed > 10: break
    nRed += 1
#p = Popen(["ProgramTest.exe","-fec","16","-ring","1","-scanCCU"],stdout=PIPE,stdin=PIPE,stderr=PIPE)
nScan = 0
while True:
    p = Popen(scanline.split(),stdout=PIPE,stdin=PIPE,stderr=PIPE)
    stdout_data = p.communicate(input='')
    print stdout_data[1]
    if not "ERROR" in stdout_data[1]:
        print stdout_data[0]
        break
    nScan += 1
    if nScan > 10: break
p = Popen(resetline.split(),stdout=PIPE,stdin=PIPE,stderr=PIPE)
#p = Popen(["ProgramTest.exe","-fec","16","-ring","1","-reset"],stdout=PIPE,stdin=PIPE,stderr=PIPE)
stdout_data = p.communicate(input='')[0]
print stdout_data
