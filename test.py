from subprocess import Popen,PIPE,STDOUT

p = Popen(["ProgramTest.exe","-fec","16","-ring","1","-reset"],stdout=PIPE,stdin=PIPE,stderr=PIPE)
stdout_data = p.communicate(input='')[0]
print stdout_data
#p = Popen(["ProgramTest.exe","-fec","16","-ring","1","-redundancy","FEC-B-A","0x5f-B-A"],stdout=PIPE,stdin=PIPE,stderr=PIPE)
p = Popen(["ProgramTest.exe","-fec","16","-ring","1","-redundancy","FEC-A-B","0x3f-A-B"],stdout=PIPE,stdin=PIPE,stderr=PIPE)
stdout_data = p.communicate(input='')[0]
print stdout_data
p = Popen(["ProgramTest.exe","-fec","16","-ring","1","-scanCCU"],stdout=PIPE,stdin=PIPE,stderr=PIPE)
stdout_data = p.communicate(input='')[1]
print stdout_data
p = Popen(["ProgramTest.exe","-fec","16","-ring","1","-reset"],stdout=PIPE,stdin=PIPE,stderr=PIPE)
stdout_data = p.communicate(input='')[0]
print stdout_data
