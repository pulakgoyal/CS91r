from intervaltree import Interval, IntervalTree
import sys
import re
import os 
import mmap
import directio
import time
import numpy 

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

	# Keep track of total time spend using the interval tree
	counter = 0;
	time_list_read = []
	time_list_write = []

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
			start = time.time()
			if (t.overlaps(new_interval[0], new_interval[1])):
				partition_overlapping_intervals(new_interval)
			else:
				t.add(new_interval)
			end = time.time()
			time_list_read.append(end - start)
			counter += end - start

		# Match on disk read
		match = re.search(r"([D]\s*) ([R]) (\d+) \+ (\d+)", line)

		if(match != None):

			# Read from disk
			start = time.time()
			interval_list = t.search(int(match.group(3)), int(match.group(3)) + int(match.group(4)))
			end = time.time()
			time_list_write.append(end - start)
			counter += end - start
			for interval in interval_list:
				start = interval[0]
				length = interval[1] - interval[0]
				disk.pread(start*512, length * 512)

	inptr.close() 
	disk.release()

	print str(sys.argv[1]) + ": " + str(counter)

	f1 = open("read_distribution.txt", "a")
	f1.write("time_list_read for " + str(sys.argv[1]) + "\n")
	hist1 = numpy.histogram(time_list_read, bins=50)
	f1.write(str(hist1))
	f1.close


	f2 = open("write_distribution.txt", "a")
	f2.write("time_list_write for " + str(sys.argv[1]) + "\n")
	hist2 = numpy.histogram(time_list_write, bins=50)
	f2.write(str(hist2))
	f2.close

if __name__ == '__main__':
   main()

