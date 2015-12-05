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
		if (t.overlaps(new_interval[0], new_interval[1])):
			partition_overlapping_intervals(new_interval)
		else:
			t.add(new_interval)

		disk.pwrite(SECTOR_SZ * n, buf)

	# Calculate number of intervals in interval tree
	num_intervals = len(list(t))
	print num_intervals

	# Read 1 GB file in 1 MB increments
	for i in range(0, 1000):

		interval_list = t.search(NUM_SECTORS_PER_MB * i, NUM_SECTORS_PER_MB * (i+1))

		for interval in interval_list:
			start = max(interval[0], NUM_SECTORS_PER_MB * i)
			end = min(interval[1], NUM_SECTORS_PER_MB * (i+1))
			length = end - start
			disk.pread(start * SECTOR_SZ, length * SECTOR_SZ)

	disk.release()

if __name__ == '__main__':
   main()

