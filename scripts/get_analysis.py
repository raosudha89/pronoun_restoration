# -*- coding: utf-8 -*- 
import sys
import re
from collections import defaultdict
from optparse import OptionParser

def get_pronoun_label(line):
	f_pronouns = ['i', 'my', 'me', 'we', 'us','our']
	s_pronouns = ['you', 'your']
	f_count = 0
	s_count = 0
	f_positions = []
	s_positions = []
	for pro in f_pronouns:
		f_count += len(re.findall('^' + pro + ' ', line)) + len(re.findall(' ' + pro + ' ', line)) + len(re.findall(' ' + pro + '$', line))
		f_positions += [m.span()[0] for m in re.finditer('^' + pro + ' ', line)] +  [m.span()[0] for m in re.finditer(' ' + pro + ' ', line)] + [m.span()[0] for m in re.finditer(' ' + pro + '$', line)]
	for pro in s_pronouns:
		s_count += len(re.findall('^' + pro + ' ', line)) + len(re.findall(' ' + pro + ' ', line)) + len(re.findall(' ' + pro + '$', line))
		s_positions += [m.span()[0] for m in re.finditer('^' + pro + ' ', line)] +  [m.span()[0] for m in re.finditer(' ' + pro + ' ', line)] + [m.span()[0] for m in re.finditer(' ' + pro + '$', line)]
	if f_count == 0 and s_count == 0:
		return ('none', 0, 0)
	if f_count != 0 and s_count != 0:
		print "mixed"
	if(f_count == s_count):
		f_min = min(f_positions)
		s_min = min(s_positions)
		print f_min, s_min
		starts_with = '1v' if f_min < s_min else '2v'
		return (starts_with, f_count, s_count)
	elif(f_count > s_count):
		return ('1v', f_count, s_count)
	else:
		return ('2v', f_count, s_count)

def get_pronoun_label_zh(line):
	f_pronouns = ['我', '我们', '我 的']
	s_pronouns = ['你', '你们', '你 的']
	f_count = 0
	s_count = 0
	f_positions = []
	s_positions = []
	for pro in f_pronouns:
		f_zh = re.findall('^' + pro + ' ', line) + re.findall(' ' + pro + ' ', line) + re.findall(' ' + pro + '$', line)
		f_positions += [m.span()[0] for m in re.finditer('^' + pro + ' ', line)] +  [m.span()[0] for m in re.finditer(' ' + pro + ' ', line)] + [m.span()[0] for m in re.finditer(' ' + pro + '$', line)]
		f_count += len(f_zh)
	for pro in s_pronouns:
		s_zh = re.findall('^' + pro + ' ', line) + re.findall(' ' + pro + ' ', line) + re.findall(' ' + pro + '$', line)
		s_positions += [m.span()[0] for m in re.finditer('^' + pro + ' ', line)] +  [m.span()[0] for m in re.finditer(' ' + pro + ' ', line)] + [m.span()[0] for m in re.finditer(' ' + pro + '$', line)]
		s_count += len(s_zh)

	if f_count == 0 and s_count == 0:
		return ('none', 0, 0, [], [])
	if(f_count == s_count):
		f_min = min(f_positions)
		s_min = min(s_positions)
		starts_with = '1v' if f_min < s_min else '2v'
		return (starts_with, f_count, s_count, f_zh, s_zh)
		#return ('1v', f_count, s_count, f_zh, s_zh)
	elif(f_count > s_count):
		return ('1v', f_count, s_count, f_zh, s_zh)
	else:
		return ('2v', f_count, s_count, f_zh, s_zh)

def to_searn_label(label):
	if label == 'none':
		return '1'
	elif label == '1h':
		return '2'
	elif label == '1v':
		return '3'
	elif label == '2h':
		return '4'
	elif label == '2v':
		return '5'

def get_hidden_label(last_label):
	if last_label == '1v' or last_label == '1h':
		return '2h'
	if last_label == '2v' or last_label == '2h':
		return '1h'
	return 'none'
		
def extract_labels(en, zh):
	last_label_en = 'none'
	last_label_zh = 'none'
	labels = ""
	for en_line in en.readlines():
		en_line = en_line.strip("\n")
		zh_line = zh.readline()
		zh_line = zh_line.strip("\n")
		if "<DOC" in en_line:
			continue
		if "</DOC>" in en_line:
			last_label_en = 'none'
			last_label_zh = 'none'
			#print labels
			labels = ""
			continue
		label_en, f_count_en, s_count_en = get_pronoun_label(en_line)
		label_zh, f_count_zh, s_count_zh, f_zh, s_zh = get_pronoun_label_zh(zh_line)
		print
		print en_line, label_en
		if label_zh == '1v' or label_zh == '2v':
			if label_zh != label_en:
				print "zh: %s en: %s" % (label_zh, label_en)
		if label_en == 'none':
			label_en = get_hidden_label(last_label_en)
		if label_zh == 'none':
			label_zh = get_hidden_label(last_label_zh)
		labels += to_searn_label(label_en) + " "
		last_label_en = label_en
		last_label_zh = label_zh

def main(argv):
	if len(argv) < 4:
		print "usage: python get_analysis.py --en-file <file> --zh-file <file>"
		return
	parser = OptionParser()
	parser.add_option("--en-file", dest="en_file", action="store",
				  help="write report to FILE", metavar="FILE")
	parser.add_option("--zh-file", dest="zh_file", action="store",
				  help="write report to FILE", metavar="FILE")
	(options, args) = parser.parse_args()
	en = open(options.en_file)
	zh = open(options.zh_file)
	extract_labels(en, zh)
	en.close()
	zh.close()

if __name__ == "__main__":
	main(sys.argv[1:])
