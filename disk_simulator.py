from intervaltree import Interval, IntervalTree
import sys
import re
import os 
import mmap
import directio

global t
t = IntervalTree()

# Partitions intervals
def partition_overlapping_intervals(new_interval):
	t.slice(new_interval[0])
	t.slice(new_interval[1])
	t.remove_envelop(new_interval[0], new_interval[1])
	t.add(new_interval)


def main():

	# Open blktrace output file
	inptr = open(sys.argv[1], "r")

	# Open disk for reading and writing 
	disk = directio.DirectFile(str(sys.argv[2]), 512)

	while(True):

		# Extract new interval 
		line = inptr.readline()
		if (line == ""):
			break;

		# Match on disk write
		match = re.search(r"([D]\s*) ([W]) (\d+) \+ (\d+)", line)

		if(match != None):

			# Write to disk
			buf = 'a' * (512 * int(match.group(4)))
			disk.pwrite(int(match.group(3))*512, buf)

			# Construct new interval
			new_interval = Interval(int(match.group(3)), int(match.group(3)) + int(match.group(4)))

			# Add new interval to tree
			if (t.overlaps(new_interval[0], new_interval[1])):
				partition_overlapping_intervals(new_interval)
			else:
				t.add(new_interval)

		# Match on disk read
		match = re.search(r"([D]\s*) ([R]) (\d+) \+ (\d+)", line)

		if(match != None):

			# Read from disk
			for interval in t.search(int(match.group(3)), int(match.group(3)) + int(match.group(4))):
				start = interval[0]
				length = interval[1] - interval[0]
				disk.pread(start*512, length * 512)

	inptr.close()
	disk.release()

if __name__ == '__main__':
   main()

