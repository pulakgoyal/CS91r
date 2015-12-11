import sys
import re

#sudo mount -t vfat -o rw,exec,uid=1000,gid=1000,umask=022 /dev/sdb1 usbdrive

def main():

	blktrace_raw = open(sys.argv[1], "rw+")
	blktrace_output = open(sys.argv[2], "a")
	thread = re.escape(sys.argv[3])

	for line in blktrace_raw:
		#match = re.search(r'sysbench', line)
		match = re.search(thread, line)
		if (match != None):
			blktrace_output.write(line)

if __name__ == '__main__':
   main()




