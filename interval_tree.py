from intervaltree import Interval, IntervalTree
import sys
import re

global t
t = IntervalTree()

# Partitions two overlapping intervals into three disjoint intervals (DONT USE THIS FOR NOW)
def partition_intervals(old_intervals, new_interval):
	t.add(new_interval)
	t.slice(new_interval[0])
	t.slice(new_interval[1])
	for interval in old_intervals: 
		t.slice(interval[0])
		t.slice(interval[1])

# Partitions intervals
def partition_overlapping_intervals(new_interval):
	t.slice(new_interval[0])
	t.slice(new_interval[1])
	t.remove_envelop(new_interval[0], new_interval[1])
	t.add(new_interval)

# Function to calculate number of dead sectors
# A dead sector is defined as a physical sector on a remote machine that used 
# to hold data for virtual sector X, but whose data has been invalidated by 
# an overwrite to X
def calculate_dead_sectors(old_intervals, new_interval):
	old_intervals_sorted = sorted(old_intervals)
	# Calculate total sectors touched by old_intervals
	count = 0
	for i in xrange(0, len(old_intervals_sorted)):
		count += old_intervals_sorted[i][1] - old_intervals_sorted[i][0]
	# Adjust calculation to only include total sectors touched by old intervals within
	# range of new_interval
	if(old_intervals_sorted[0][0] < new_interval[0]):
		count -= new_interval[0] - old_intervals_sorted[0][0]
	if(old_intervals_sorted[len(old_intervals_sorted) - 1][1] > new_interval[1]):
		count -= old_intervals_sorted[len(old_intervals_sorted) - 1][1] - new_interval[1]
	return count


# returns list of all sectors that have been the target of writes (increasing order)
def virtual_disk_explorer():
	new_list = []
	interval_list = list(sorted(t))
	# Merge adjacent intervals
	counter = 0
	while(counter <= len(interval_list) - 2):
		begin = interval_list[counter][0]
		end = interval_list[counter][1]
		while(interval_list[counter][1] == interval_list[counter + 1][0]):
			end = interval_list[counter + 1][1]
			if (counter == len(interval_list) - 2):
				break
			counter += 1
		new_list.append(Interval(begin, end))
		counter += 1
	# Check last interval
	if(interval_list[counter][1] != new_list[len(new_list) - 1][1]):
		new_list.append(interval_list[counter])
	return new_list


def main():

	inptr = open(sys.argv[1], "r")

	# Create histogram
	hist = [0] * 500

	# Create overwrite counter
	overwrites = 0

	# Create dead sector counter
	dead_sectors = 0

	while(True):

		# Extract new interval 
		line = inptr.readline()
		if (line == ""):
			break;
		match = re.search(r"([D]\s*) ([W]) (\d+) \+ (\d+)", line)

		if(match != None):

			# Add write to histogram
			hist[int(match.group(4))] += 1

			# Construct new interval
			new_interval = Interval(int(match.group(3)), int(match.group(3)) + int(match.group(4)))

			# Calculate number of invalidated (dead) sectors
			if (t.overlaps(new_interval[0], new_interval[1])):
				dead_sectors += calculate_dead_sectors(t.search(new_interval[0], new_interval[1]), new_interval)

			# Add new interval to tree
			if (t.overlaps(new_interval[0], new_interval[1])):
				partition_overlapping_intervals(new_interval)
				overwrites += 1
			else:
				t.add(new_interval)

	inptr.close()

	print hist
	print "There were these many overwrites: " + str(overwrites)
	print "There were these many dead sectors: " + str(dead_sectors)
	print virtual_disk_explorer()

if __name__ == '__main__':
   main()








