from intervaltree import Interval, IntervalTree
import sys
import re
import os 
import mmap

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

	# Open disk for writing
	disk = os.open(str(sys.argv[2]), os.O_CREAT | os.O_DIRECT | os.O_TRUNC | os.O_RDWR)

	# Open disk for reading 


	while(True):

		# Extract new interval 
		line = inptr.readline()
		if (line == ""):
			break;

		# Match on disk write
		match = re.search(r"([D]\s*) ([W]) (\d+) \+ (\d+)", line)

		if(match != None):

			# Write data to disk (How do we know which physical sector to write to? We would normally rely on a 
			# free list for that, but in this case we don't have to worry about it.)
			buf = mmap.mmap(-1, 512 * int(match.group(4)))
			s = 'a' * (512 * int(match.group(4)))
			buf.write(s)
			os.lseek(disk, int(match.group(3)) * 512, os.SEEK_SET)
			os.write(disk, buf)

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

			# Search interval tree for physical sectors (Data is immutable right? So virtual sectors might be on different physical sectors)
			# You'll probably have to do multiple reads)
			for interval in t.search(int(match.group(3)), int(match.group(3)) + int(match.group(4))):
				# Read from each interval



	inptr.close()
	os.close(disk)


if __name__ == '__main__':
   main()

