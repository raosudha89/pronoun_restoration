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
	starts_with = '1' if f_min < s_min else '2'
        #ends_with   = '2' if f_max > s_max else '1'
        #print line, starts_with
	return (starts_with, f_count, s_count)
	#return ('1', f_count, s_count)
    elif(f_count > s_count):
        return ('1', f_count, s_count)
    else:
        return ('2', f_count, s_count)

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
	starts_with = '1' if f_min < s_min else '2'
	return (starts_with, f_count, s_count, f_zh, s_zh)
	#return (starts_with, f_count, s_count)
	#return ('1', f_count, s_count)
    elif(f_count > s_count):
        return ('1', f_count, s_count, f_zh, s_zh)
    else:
        return ('2', f_count, s_count, f_zh, s_zh)

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

def to_bool(val):
    if(val == True):
	return 1
    else:
	return 0

def extract_features(en, zh, zh_pos, options):
    last_participant = None
    last_en = ""
    last_zh = ""
    last_zh_pos = ""
    expected = 'none'
    label_output = ""
    for l_en in en.readlines():
        l_zh = zh.readline()
        # make sure they're both either <doc lines or _not_ <doc lines
        assert((re.match("^<doc" , l_en) is None) == (re.match("^<DOC" , l_zh) is None))
        assert((re.match("^</doc", l_en) is None) == (re.match("^</DOC", l_zh) is None))
        if re.match("</doc", l_en):
                    label, f_count_en, s_count_en = get_pronoun_label(last_en)
		    label_zh, f_count_zh, s_count_zh, f_zh, s_zh = get_pronoun_label_zh(last_zh)
		    if(label_zh == '1v'):
			label = '1'
		    if(label_zh == '2v'):
			label = '2'
                    if label == 'none':
                        if expected == 'none':
                            total_label = 'none'
                        else:
                            total_label = expected + 'h'   # hidden, but expected
                    else:
                        total_label = label + 'v'
		    label_output += to_searn_label(total_label) + " "
                    if label == '1' or label == '2': expected = label
            	    print label_output
	    	    label_output = ""
    		    last_participant = None
    		    last_en = ""
    		    last_zh = ""
    		    last_zh_pos = ""
            	    expected = 'none'
        m_en = re.match('^<seg id="([^"]+)" msg_id="([^"]+)" participant="([^"]+)"> +(.+) +</seg>', l_en)
        m_zh = re.match('^<seg id="([^"]+)" msg_id="([^"]+)" participant="([^"]+)"> +(.+) +</seg>', l_zh)
        if m_en is not None:
            # make sure they match
            assert(m_zh is not None)
            assert(m_en.group(1) == m_zh.group(1))
            assert(m_en.group(2) == m_zh.group(2))
            assert(m_en.group(3) == m_zh.group(3))
            l_zh_pos = zh_pos.readline()
	    l_zh_pos = l_zh_pos.rstrip("\n")
	    if m_en.group(3) != last_participant:
                if last_participant is not None:
                    label, f_count_en, s_count_en = get_pronoun_label(last_en)
		    label_zh, f_count_zh, s_count_zh, f_zh, s_zh = get_pronoun_label_zh(last_zh)
		    if(label_zh == '1v'):
			label = '1'
		    if(label_zh == '2v'):
			label = '2'
                    if label == 'none':
                        if expected == 'none':
                            total_label = 'none'
                        else:
                            total_label = expected + 'h'   # hidden, but expected
                    else:
                        total_label = label + 'v'
		    label_output += to_searn_label(total_label) + " "
                    if label == '1' or label == '2': expected = label
                last_participant = m_en.group(3)
                last_en = m_en.group(4)
                last_zh = m_zh.group(4)
		last_zh_pos = l_zh_pos
                if expected == '1': expected = '2'
                elif expected == '2': expected = '1'
            else:
                last_en = last_en + " " + m_en.group(4)
                last_zh = last_zh + " " + m_zh.group(4)
		last_zh_pos = last_zh_pos + " " + l_zh_pos
        else:
            assert(m_zh is None)


def do_main(argv):
    if len(argv) < 4:
	print "usage: python to_actual_label_v1.py --en-file <file> --zh-file <file> --zh-pos-file <file> --bow --f-count --s-count --zh-label --pos-tags --verbs --pronouns"
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

if __name__ == '__main__': do_main(sys.argv[1:])
    

