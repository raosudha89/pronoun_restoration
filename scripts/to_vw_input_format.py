# -*- coding: utf-8 -*- 
import sys
import re
from collections import defaultdict
from optparse import OptionParser

def get_pronoun_person_zh(pronoun):
	pronoun = pronoun.strip(' \t\n\r')
	if(pronoun == '我' or pronoun == '我们' or pronoun == '我 的'):
		return '1'
	elif(pronoun == '你' or pronoun == '你们' or pronoun == '你 的'):
		return '2'
	else:
		return '3'

def get_pronoun_label(line):
	f_pronouns = ['i', 'my', 'me', 'we', 'us','our']
	s_pronouns = ['you', 'your']
	f_count = 0
	s_count = 0
	f_positions = []
	s_positions = []
	for pro in f_pronouns:
		f_count += len(re.findall('^' + pro + ' ', line)) + len(re.findall(' ' + pro + ' ', line))
		f_positions += [m.span()[0] for m in re.finditer('^' + pro + ' ', line)] +  [m.span()[0] for m in re.finditer(' ' + pro + ' ', line)]
	for pro in s_pronouns:
		s_count += len(re.findall('^' + pro + ' ', line)) + len(re.findall(' ' + pro + ' ', line))
		s_positions += [m.span()[0] for m in re.finditer('^' + pro + ' ', line)] +  [m.span()[0] for m in re.finditer(' ' + pro + ' ', line)]
	if f_count == 0 and s_count == 0:
		return ('none', 0, 0)
	if(f_count == s_count):
		f_min = min(f_positions)
		s_min = min(s_positions)
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
		f_zh = re.findall('^' + pro + ' ', line) + re.findall(' ' + pro + ' ', line)
		f_positions += [m.span()[0] for m in re.finditer('^' + pro + ' ', line)] +  [m.span()[0] for m in re.finditer(' ' + pro + ' ', line)]
		f_count += len(f_zh)
	for pro in s_pronouns:
		s_zh = re.findall('^' + pro + ' ', line) + re.findall(' ' + pro + ' ', line)
		s_positions += [m.span()[0] for m in re.finditer('^' + pro + ' ', line)] +  [m.span()[0] for m in re.finditer(' ' + pro + ' ', line)]
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
		
def extract_features(en, zh, zh_pos, options):
	last_label_en = 'none'
	last_label_zh = 'none'
	for en_line in en.readlines():
		en_line = en_line.strip("\n")
		zh_line = zh.readline()
		zh_line = zh_line.strip("\n")
		if "<DOC" in en_line:
			continue
		if "</DOC>" in en_line:
			last_label_en = 'none'
			last_label_zh = 'none'
			print
			continue
		zh_pos_line = zh_pos.readline()
		zh_pos_line = zh_pos_line.strip("\n")
		label_en, f_count_en, s_count_en = get_pronoun_label(en_line)
		label_zh, f_count_zh, s_count_zh, f_zh, s_zh = get_pronoun_label_zh(zh_line)
		if label_en == 'none':
			label_en = get_hidden_label(last_label_en)
		if label_zh == 'none':
			label_zh = get_hidden_label(last_label_zh)
		zh_line = zh_line.replace("|", " ").replace(":", " ") 
		zh_pos_line = zh_pos_line.replace("|", " ").replace(":", " ") 
		word_tag_list = zh_pos_line.split()
		tags = ""
		verbs = ""
		pronouns = ""
		for word_tag in word_tag_list:
			if(len(word_tag.split("#")) != 2):
				continue
			word = word_tag.split("#")[0].strip(' \t\n\r') + " "
			tag = word_tag.split("#")[1].strip(' \t\n\r') + " "
			if(tag.strip(' \t\n\r') == "PN"):
				tag = tag.strip(' \t\n\r')+ "_" + get_pronoun_person_zh(word) + " "
			tags += tag
			if(tag.strip(' \t\n\r') == "VV"):
				 verbs += word + " "
			if(get_pronoun_person_zh(word) == '1' or get_pronoun_person_zh(word) == '2'):
				  pronouns += word + " "
		feature_set = ""
		if(options.bow):
			feature_set += "|w <s> %s </s>" % (zh_line)
		if(options.f_count):
			feature_set += "|f %s " % (f_count_zh)
		if(options.s_count):
			feature_set += "|s %s " % (s_count_zh)
		if(options.zh_label):
			feature_set += "|l %s " % (to_searn_label(label_zh))
		if(options.pos_tags):
			feature_set += "|t <s> %s</s>" % (tags.strip("\n"))
		if(options.verbs):
			feature_set += "|v <s> %s</s>" % (verbs)
		if(options.pronouns):
			feature_set += "|p <s> %s</s>" % (pronouns)
		print "%s " % (to_searn_label(label_en)) + feature_set
		last_label_en = label_en
		last_label_zh = label_zh

def main(argv):
	if len(argv) < 4:
		print "usage: python to_vw_input_format.py --en-file <file> --zh-file <file> --zh-pos-file <file> --bow --f-count --s-count --zh-label --pos-tags --verbs --pronouns"
		return
	parser = OptionParser()
	parser.add_option("--en-file", dest="en_file", action="store",
				  help="write report to FILE", metavar="FILE")
	parser.add_option("--zh-file", dest="zh_file", action="store",
				  help="write report to FILE", metavar="FILE")
	parser.add_option("--zh-pos-file", dest="zh_pos_file", action="store",
				  help="write report to FILE", metavar="FILE")
	parser.add_option("--bow",
				  action="store_true", dest="bow", default=False)
	parser.add_option("--f-count",
				  action="store_true", dest="f_count", default=False)
	parser.add_option("--s-count",
				  action="store_true", dest="s_count", default=False)
	parser.add_option("--zh-label",
				  action="store_true", dest="zh_label", default=False)
	parser.add_option("--pos-tags",
				  action="store_true", dest="pos_tags", default=False)
	parser.add_option("--verbs",
				  action="store_true", dest="verbs", default=False)
	parser.add_option("--pronouns",
				  action="store_true", dest="pronouns", default=False)
	(options, args) = parser.parse_args()
	en = open(options.en_file)
	zh = open(options.zh_file)
	zh_pos = open(options.zh_pos_file)
	extract_features(en, zh, zh_pos,options)
	en.close()
	zh.close()
	zh_pos.close()
	

if __name__ == "__main__":
	main(sys.argv[1:])
