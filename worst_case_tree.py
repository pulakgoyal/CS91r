from intervaltree import Interval, IntervalTree
import sys
import directio
import time
import numpy 
import random

global t
t = IntervalTree()

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
	buf = 'a' * (1000448)
	for i in range(0, 1000):

		# Construct new interval
		new_interval = Interval(1954*i, 1954*(i+1))

		# Add new interval to tree
		if (t.overlaps(new_interval[0], new_interval[1])):
			partition_overlapping_intervals(new_interval)
		else:
			t.add(new_interval)

		# Write to disk
		disk.pwrite(1000448*i, buf)

	# Write to random sectors
	buf = 'b' * (512)
	for i in range(0,1000):

		# Choose random sector
		n = random.randint(0, 1953999)

		# Construct new interval 
		new_interval = Interval(n, n+1)

		# Add new interval to tree
		if (t.overlaps(new_interval[0], new_interval[1])):
			partition_overlapping_intervals(new_interval)
		else:
			t.add(new_interval)

		disk.pwrite(512*n, buf)

	# Calculate number of intervals in interval tree
	num_intervals = len(list(t))
	print num_intervals

	# Read 1 GB file in 1 MB increments
	for i in range(0, 1000):

		interval_list = t.search(1954*i, 1954*(i+1))

		for interval in interval_list:
			start = interval[0]
			if (start < 1954*i):
				start = 1954*i
			end = interval[1]
			if (end > 1954(i+1)):
				end = 1954(i+1)
			length = end - start
			disk.pread(start*512, length * 512)

	disk.release()

if __name__ == '__main__':
   main()

