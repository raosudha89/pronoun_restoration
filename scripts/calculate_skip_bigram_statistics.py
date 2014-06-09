# -*- coding: utf-8 -*- 
import sys
import math

def get_bigrams(line):
	words = line.split()
	bigrams = []
	for i in range(len(words)):
		for j in range (i+1, len(words)):
			bigrams.append((words[i], words[j]))
	return bigrams

def filter_pro_bigrams(bigrams):
	pro_bigrams = []
	#pronouns = ['i', 'you'] 
	#pronouns = ['i'] 
	pronouns = ['you'] 
	for bigram in bigrams:
		if bigram[0] in pronouns or bigram[1] in pronouns:
			pro_bigrams.append(bigram)
	return pro_bigrams

def nCr(n,r):
	f = math.factorial
	return f(n) / f(r) / f(n-r)

def skip_bigram(ref_bigrams, out_bigrams):
	count = 0
	for bigram in ref_bigrams:
		if bigram in out_bigrams:
			count += 1
	return count

def main(argv):
	if len(argv) != 2:
		print "usage: python calculate_skip_bigram.py ref_file out_file"
		return
	ref_file = open(argv[0])
	out_file = open(argv[1])
	lines = 0
	pro_lines = 0
	total_recall = 0
	total_precision = 0
	total_pro_recall = 0
	total_pro_precision = 0
	for ref_line in ref_file.readlines():
		ref_line = ref_line.strip("\n")
		out_line = out_file.readline()
		out_line = out_line.strip("\n")
		#print
		#print "%s" % ref_line
		#print "%s" % out_line
		if len(ref_line.split()) < 2 or len(out_line.split()) < 2:
			continue
		lines += 1
		ref_bigrams = get_bigrams(ref_line)
		out_bigrams = get_bigrams(out_line)
		#print ref_bigrams
		#print out_bigrams
		#print skip_bigram(ref_bigrams, out_bigrams)
		recall = float(skip_bigram(ref_bigrams, out_bigrams))/len(ref_bigrams)
		precision = float(skip_bigram(ref_bigrams, out_bigrams))/len(out_bigrams)
		#print recall, precision
		total_recall += recall
		total_precision += precision
		ref_pro_bigrams = filter_pro_bigrams(ref_bigrams)
		out_pro_bigrams = filter_pro_bigrams(out_bigrams)
		if len(ref_pro_bigrams) == 0 and len(out_pro_bigrams) == 0:
			continue
		pro_lines += 1
		if len(ref_pro_bigrams) != 0:
			pro_recall = float(skip_bigram(ref_pro_bigrams, out_pro_bigrams))/len(ref_pro_bigrams)
		if len(out_pro_bigrams) != 0:
			pro_precision = float(skip_bigram(ref_pro_bigrams, out_pro_bigrams))/len(out_pro_bigrams)
		#print pro_recall, pro_precision
		total_pro_recall += pro_recall
		total_pro_precision += pro_precision
	#print "Skip bigram Recall: " + str(float(total_recall)/lines)
	#print "Skip bigram Precision: " + str(float(total_precision)/lines)
	#print "Skip bigram pro Recall: " + str(float(total_pro_recall)/pro_lines)
	#print "Skip bigram pro Precision: " + str(float(total_pro_precision)/pro_lines)
	print "%0.2f & %0.2f & %0.2f & %0.2f \\\\ \\hline" % (float(total_pro_recall)/pro_lines, float(total_pro_precision)/pro_lines, float(total_recall)/lines, float(total_precision)/lines)
if __name__ == "__main__":
	main(sys.argv[1:])
