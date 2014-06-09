import numpy
import sys, os

def confusion_table(cfm, label):
    """Returns a confusion table in the following format:
    [[true positives, false negatives],
     [false positives, true negatives]]
    for the given label index in the confusion matrix.
    """
    predicted = cfm[label]
    actual    = [cfm[i][label] for i in range(len(cfm))]
    true_pos  = predicted[label]
    false_pos = sum(actual) - true_pos
    false_neg = sum(predicted) - true_pos
    total     = sum([sum(i) for i in cfm])
    true_neg  = total - true_pos - false_pos - false_neg
    confusion_table = numpy.array([[true_pos, false_neg],[false_pos, true_neg]])
    return confusion_table

def main(argv):
	if(len(argv) != 2):
		print "usage: confusion_matrix.py <actual_labels> <predicted_labels>"
	else:
		actual = open(argv[0])
		predicted = open(argv[1])
		#confusion_matrix = numpy.zeros((5,5))
		confusion_matrix = []
		for i in range(5):
		    confusion_matrix.append([])
		    for j in range(5):
			confusion_matrix[i].append(0)
		for l_actual in actual.readlines():
			l_actual = l_actual.strip()
			if(l_actual == ""):
				print 'here'
				continue
			l_predicted = predicted.readline().strip()
			actual_labels = l_actual.split(" ")
			predicted_labels = l_predicted.split(" ")
			assert(len(actual_labels) == len(predicted_labels))
			for i in range(0, len(actual_labels)):
				confusion_matrix[int(actual_labels[i]) - 1][int(predicted_labels[i]) - 1] = confusion_matrix[int(actual_labels[i]) - 1][int(predicted_labels[i]) - 1] + 1
		print "Confusion matrix"
		for i in range(5):
			print confusion_matrix[i]
		print
		print "Confusion table"
		print "[[true positives, false negatives],"
		print "[false positives, true negatives]]"
		print 
		print "label = none"
		print confusion_table(confusion_matrix, 0)
		print "label = 1h"
		print confusion_table(confusion_matrix, 1)
		print "label = 1v"
		print confusion_table(confusion_matrix, 2)
		print "label = 2h"
		print confusion_table(confusion_matrix, 3)
		print "label = 2v"
		print confusion_table(confusion_matrix, 4)
				
if __name__ == '__main__':
	main(sys.argv[1:])
