from intervaltree import Interval, IntervalTree
import sys
import directio
import time
import numpy 
import random

global t
t = IntervalTree()

# Constants
SECTOR_SZ = 512
NUM_SECTORS_PER_MB = 1954
NUM_SECTORS_PER_GB = 1954000


# Partitions intervals
def partition_overlapping_intervals(new_interval):
	t.slice(new_interval[0])
	t.slice(new_interval[1])
	t.remove_envelop(new_interval[0], new_interval[1])
	t.add(new_interval)


def main():

	# Open disk for reading and writing 
	disk = directio.DirectFile(str(sys.argv[1]), 512)

	# Keep track of total time spend using the interval tree
	time_list_read = []
	time_list_write = []

	# Write out 1 GB file in 1 MB increments
	buf = 'a' * (NUM_SECTORS_PER_MB * SECTOR_SZ)
	for i in range(0, 1000):

		# Construct new interval
		new_interval = Interval(i*NUM_SECTORS_PER_MB, (i+1)*NUM_SECTORS_PER_MB)

		# Add new interval to tree
		if (t.overlaps(new_interval[0], new_interval[1])):
			partition_overlapping_intervals(new_interval)
		else:
			t.add(new_interval)

		# Write to disk
		disk.pwrite(NUM_SECTORS_PER_MB * SECTOR_SZ * i, buf)

	# Write to random sectors
	buf = 'b' * SECTOR_SZ
	for i in range(0,int(sys.argv[2])):

		# Choose random sector
		n = random.randint(0, NUM_SECTORS_PER_GB - 1)

		# Construct new interval 
		new_interval = Interval(n, n+1)

		# Add new interval to tree
		start = time.time()
		if (t.overlaps(new_interval[0], new_interval[1])):
			partition_overlapping_intervals(new_interval)
		else:
			t.add(new_interval)
		end = time.time()
		time_list_write.append(end - start)

		disk.pwrite(SECTOR_SZ * n, buf)

	# Calculate number of intervals in interval tree
	num_intervals = len(list(t))
	print num_intervals

	# Read 1 GB file in 1 MB increments
	for i in range(0, 1000):

		start = time.time()
		interval_list = t.search(NUM_SECTORS_PER_MB * i, NUM_SECTORS_PER_MB * (i+1))
		end = time.time()
		time_list_read.append(end - start)

		for interval in interval_list:
			start = max(interval[0], NUM_SECTORS_PER_MB * i)
			end = min(interval[1], NUM_SECTORS_PER_MB * (i+1))
			length = end - start
			disk.pread(start * SECTOR_SZ, length * SECTOR_SZ)

	disk.release()

	read_list = numpy.asarray(time_list_read)
	numpy.savetxt(str(sys.argv[2]) + "_read_worst_case.csv", read_list, delimiter=",")
	hist1 = numpy.histogram(time_list_read, bins=50)
	print hist1

	write_list = numpy.asarray(time_list_write)
	numpy.savetxt(str(sys.argv[2]) + "_write_worst_case.csv", write_list, delimiter=",")
	hist2 = numpy.histogram(time_list_write, bins=50)
	print hist2

if __name__ == '__main__':
   main()

