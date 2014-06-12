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
				continue
			l_predicted = predicted.readline().strip()
			actual_labels = l_actual.split(" ")
			l_predicted = l_predicted.replace("6","2").replace("7","4").replace("8","2").replace("9","4")
			predicted_labels = l_predicted.split(" ")
			assert(len(actual_labels) == len(predicted_labels))
			for i in range(0, len(actual_labels)):
				confusion_matrix[int(actual_labels[i]) - 1][int(predicted_labels[i]) - 1] += 1
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
		row_sum_1v = 0
		row_sum_2v = 0
		col_sum_1v = 0
		col_sum_2v = 0
		for i in range(5):
			row_sum_1v += confusion_matrix[2][i]
			row_sum_2v += confusion_matrix[4][i]
			col_sum_1v += confusion_matrix[i][2]
			col_sum_2v += confusion_matrix[i][4]
		recall_1v = float(confusion_matrix[2][2])/row_sum_1v
		recall_2v = float(confusion_matrix[4][4])/row_sum_2v
		precision_1v = float(confusion_matrix[2][2])/col_sum_1v
		precision_2v = float(confusion_matrix[4][4])/col_sum_2v
		print "Recall of 1v: " + str(recall_1v)	
		print "Recall of 2v: " + str(recall_2v)
		print "Precision of 1v: " + str(precision_1v)	
		print "Precision of 2v: " + str(precision_2v)
		print "1v confused as 2v: " + str(float(confusion_matrix[2][4])/row_sum_1v)
		print "2v confused as 1v: " + str(float(confusion_matrix[4][2])/row_sum_2v)
			
if __name__ == '__main__':
	main(sys.argv[1:])
