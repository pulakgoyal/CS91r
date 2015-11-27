from intervaltree import Interval, IntervalTree
import sys
import re
import os 
import mmap

global t
t = IntervalTree()


def main():

	# Open blktrace output file
	inptr = open(sys.argv[1], "r")

	# Open disk
	disk = os.open(str(sys.argv[2]), os.O_CREAT | os.O_DIRECT | os.O_TRUNC | os.O_RDWR)

	while(True):

		# Extract new interval 
		line = inptr.readline()
		if (line == ""):
			break;
		match = re.search(r"([D]\s*) ([W]) (\d+) \+ (\d+)", line)

		if(match != None):

			# Write data to disk
			buf = mmap.mmap(-1, 512 * int(match.group(4)))
			s = 'a' * (512 * match.group(4))
			buf.write(s)
			os.lseek(disk, int(match.group(3)), SEEK_SET)
			os.write(disk, buf)

			# Construct new interval
			new_interval = Interval(int(match.group(3)), int(match.group(3)) + int(match.group(4)))

			# Add new interval to tree
			if (t.overlaps(new_interval[0], new_interval[1])):
				partition_overlapping_intervals(new_interval)
			else:
				t.add(new_interval)


	inptr.close()
	os.close(disk)

	print t

if __name__ == '__main__':
   main()

