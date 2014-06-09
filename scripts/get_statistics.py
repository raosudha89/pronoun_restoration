# -*- coding: utf-8 -*- 

import os, sys
import numpy
import re

def count_pronoun(line, pro):
	return len(re.findall('^' + pro + ' ', line)) + len(re.findall(' ' + pro + ' ', line))	
def main(argv):
	if (len(argv) != 4):
		print "usage: get_statistics.py ref_file baseline_out_file synthetic_out_file zh_file"
		return
	ref_file = open(argv[0])
	baseline_out_file = open(argv[1])
	synthetic_out_file = open(argv[2])
	zh_file = open(argv[3])
	pronouns = ['i', 'my', 'me', 'we', 'us', 'you', 'your']
	#zh_pronouns = ['我', '我 的', '我', '我们', '我们', '你', '你 的']
	zh_pronouns = ['我', '我 的', '我', '我们', '我们', '你|你们', '你 的']
	baseline_matrix = numpy.zeros((len(pronouns) + 1, len(pronouns)))
	synthetic_matrix = numpy.zeros((len(pronouns) + 1, len(pronouns)))
	diff_matrix = numpy.zeros((len(pronouns) + 1, len(pronouns)))
	zh_ref_match = numpy.zeros(len(pronouns))
	zh_ref_base_match = numpy.zeros(len(pronouns))
	zh_ref_syn_match = numpy.zeros(len(pronouns))
	cur = 0
	ref_counts = numpy.zeros(len(pronouns))
	for ref_line in ref_file.readlines():
		cur += 1
		baseline_line = baseline_out_file.readline()
		synthetic_line = synthetic_out_file.readline()
		zh_line = zh_file.readline()
		for i in range(0, len(pronouns)):
			if count_pronoun(ref_line, pronouns[i]) != 0:	
				ref_counts[i] += count_pronoun(ref_line, pronouns[i])
				
				if count_pronoun(zh_line, zh_pronouns[i]) != 0:		
					zh_ref_match[i] += count_pronoun(zh_line, zh_pronouns[i])
					zh_ref_base_match[i] += count_pronoun(baseline_line, pronouns[i])
                                        zh_ref_syn_match[i] += count_pronoun(synthetic_line, pronouns[i])
				baseline_has_pro = False
				synthetic_has_pro = False
				for j in range(0, len(pronouns)):
					if count_pronoun(baseline_line, pronouns[j]) != 0:
						baseline_matrix[j][i] += count_pronoun(baseline_line, pronouns[j])
						baseline_has_pro = True
					if count_pronoun(synthetic_line, pronouns[j]) != 0:	
                                                synthetic_matrix[j][i] += count_pronoun(synthetic_line, pronouns[j])
						synthetic_has_pro = True
				if not baseline_has_pro:
					baseline_matrix[len(pronouns)][i] += count_pronoun(ref_line, pronouns[i])
				if not synthetic_has_pro:
					synthetic_matrix[len(pronouns)][i] += count_pronoun(ref_line, pronouns[i])
	for i in range(len(pronouns) + 1):
		for j in range(len(pronouns)):
			diff_matrix[i][j] = synthetic_matrix[i][j] - baseline_matrix[i][j]


	print "['i', 'my', 'me', 'we', 'us', 'you', 'your']"
	print "ref_counts", ref_counts
	print 
	print "Statistics with Chinese source translation"
	print "zh_ref_match", zh_ref_match
	print "zh_ref_base_match", zh_ref_base_match
	print "zh_ref_syn_match", zh_ref_syn_match
	print "Confusion matrices"
	print "baseline_matrix"
	print baseline_matrix
	pronouns.append('missing')
	for i in range(len(baseline_matrix)):
		print "'" + pronouns[i] + "' & " + " & ".join(str(int(j)) for j in baseline_matrix[i]) + " \\\\ \\hline"
	print "synthetic_matrix"
	print synthetic_matrix
	for i in range(len(synthetic_matrix)):
		print "'" + pronouns[i] + "' & " + " & ".join(str(int(j)) for j in synthetic_matrix[i]) + " \\\\ \\hline"
	print "diff_matrix"
	print diff_matrix
	for i in range(len(diff_matrix)):
		print "'" + pronouns[i] + "' & " + " & ".join(str(int(j)) for j in diff_matrix[i]) + " \\\\ \\hline"

if __name__ == "__main__":
	main(sys.argv[1:])
