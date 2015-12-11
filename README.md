# CS91r
Computer Science 91r Research Project

This directory contains all of the programs used to generate results for the Titan paper:

 blktrace_parse.py

 Description:

 Blktrace_parse.py is a python script that filters all the I/O operations for a given thread. 

 Usage:

 Blktrace_parse.py takes in three arguments: 1) blktrace output file 2) name of new file 3) name of thread

 Interval_tree.py

 Description: 

 Interval_tree.py calculates various statistics about the program's I/O workload based on the blktrace output. For example, it calculates the total number of overwrites, the number of dead sectors, among other things. 

 Usage: 

 Interval_tree.py takes in one argument:  Blktrace output file

 Setup.py and directio.pyx

 Description: 

 directio.pyx is a cython module that contains methods to execute direct reads and writes. You can use the cython module in any python script by running setup.py to create a cython binary, and then import the binary to your python script by adding "import directio" to your code. 

 Usage: 
 
 N/A

 Disk_simulator.py

 Description:

 Simulates the I/O workload of an application by replaying the I/O operations from the applications corresponding blktrace output. 

 Usage:

 Disk_simulator.py takes in two arguments: 1) blktrace output file 2) path to block device (e.g. /dev/sdb1)

 Worst_case_tree.py 

 Description: 

 Simulates the worst case I/O workload for the interval tree. It issues 1000 1 MB writes, then x number of random sector wide writes, and then 1000 1 MB reads. 

 Usage:

 Worst_case_tree.py takes in two arguments: 1) path to block device 2) number of writes to issue