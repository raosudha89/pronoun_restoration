import sys

def main(argv):
	if len(argv) != 3:
		print "usage: python expand_labels.py label_file label_count_file expanded_label_file"
		return
	label_file = open(argv[0])
	label_count_file = open(argv[1])
	expanded_label_file = open(argv[2], 'w')
	labels = []
	label_counts = []
	for label_line in label_file.readlines():
		label_line = label_line.strip("\n")
		labels = label_line.split()
		label_count_line = label_count_file.readline()
		label_count_line = label_count_line.strip("\n")
		label_counts = label_count_line.split()
		assert(len(labels) == len(label_counts))
		expanded_label_line = ""
		for i in range(len(labels)):
			for j in range(int(label_counts[i])):
				expanded_label_line += "%s " % (labels[i])
		expanded_label_file.write(expanded_label_line + "\n")
if __name__ == "__main__":
	main(sys.argv[1:])
