# -*- coding: utf-8 -*- 
import sys
import re
from collections import defaultdict
from optparse import OptionParser

def min_pos(l):
    mn = None
    for m in l:
        if m is not None:
            v = m.span()[0]
            if mn is None or v < mn:
                mn = v
    return mn

def min_max_pos(l):
    mn = None
    mx = None
    for iterator in l:
        for m in iterator:
            n  = m.span()[0]
            mn = n if mn is None else min(mn, n)
            mx = n if mx is None else max(mx, n)
    return (mn,mx)
            
def get_pronoun_person_zh(pronoun):
    pronoun = pronoun.strip(' \t\n\r')
    if(pronoun == '我' or pronoun == '我们' or pronoun == '我 的'):
	return '1'
    elif(pronoun == '你' or pronoun == '你们' or pronoun == '你 的'):
	return '2'
    else:
	return '3'

def get_pronoun_label(s):
    s = ' ' + s + ' '

    f_min, f_max = min_max_pos([ re.finditer('\s+i\s+', s, re.IGNORECASE),
                                 re.finditer('\s+me\s+', s, re.IGNORECASE),
                                 re.finditer('\s+my\s+', s, re.IGNORECASE),
                                 re.finditer('\s+we\s+', s, re.IGNORECASE),
                                 re.finditer('\s+us\s+', s, re.IGNORECASE),
                                 re.finditer('\s+our\s+', s, re.IGNORECASE) ])
    
    s_min, s_max = min_max_pos([ re.finditer('\s+you\s+', s, re.IGNORECASE),
                                 re.finditer('\s+your\s+', s, re.IGNORECASE) ])
    f_count_en = len(re.findall('\s+i\s+', s, re.IGNORECASE) + 
                         re.findall('\s+me\s+', s, re.IGNORECASE) + 
                         re.findall('\s+my\s+', s, re.IGNORECASE) + 
                         re.findall('\s+we\s+', s, re.IGNORECASE) + 
                         re.findall('\s+us\s+', s, re.IGNORECASE) + 
                         re.findall('\s+our\s+', s, re.IGNORECASE))
    
    s_count_en = len(re.findall('\s+you\s+', s, re.IGNORECASE) +
                                 re.findall('\s+your\s+', s, re.IGNORECASE))

    if f_min is None and s_min is None: return ('none', 0, 0)
    if f_min is None: return ('2', f_count_en, s_count_en)
    if s_min is None: return ('1', f_count_en, s_count_en)
    if(f_count_en == s_count_en):
	starts_with = '1' if f_min < s_min else '2'
        ends_with   = '2' if f_max > s_max else '1'
        return (starts_with, f_count_en, s_count_en)
    elif(f_count_en > s_count_en):
        return ('1', f_count_en, s_count_en)
    else:
        return ('2', f_count_en, s_count_en)

def get_pronoun_label_zh(s):

    f_min, f_max = min_max_pos([ re.finditer(' 我 ', s, re.IGNORECASE),
                                 re.finditer(' 我们 ', s, re.IGNORECASE),
                                 re.finditer(' 我 的 ', s, re.IGNORECASE) ])
    
    s_min, s_max = min_max_pos([ re.finditer(' 你 ', s, re.IGNORECASE),
                                 re.finditer(' 你们 ', s, re.IGNORECASE),
                                 re.finditer(' 你 的 ', s, re.IGNORECASE) ])
    f_zh = re.findall(' 我 ', s, re.IGNORECASE) + re.findall(' 我们 ', s, re.IGNORECASE) + re.findall(' 我 的 ', s, re.IGNORECASE)
    s_zh = re.findall(' 你 ', s, re.IGNORECASE) + re.findall(' 你们 ', s, re.IGNORECASE) + re.findall(' 你 的 ', s, re.IGNORECASE)
    f_count_zh = len(f_zh)
    s_count_zh = len(s_zh)
    if f_min is None and s_min is None: return ('none', 0, 0, [], [])
    if f_min is None: return ('2v', f_count_zh, s_count_zh, f_zh, s_zh)
    if s_min is None: return ('1v', f_count_zh, s_count_zh, f_zh, s_zh)
    # otherwise we have mixed
    if(f_count_zh == s_count_zh):
        starts_with = '1v' if f_min < s_min else '2v'
        ends_with   = '2v' if f_max > s_max else '1v'
        return (starts_with, f_count_zh, s_count_zh, f_zh, s_zh)
    if(f_count_zh > s_count_zh):
        return ('1v', f_count_zh, s_count_zh, f_zh, s_zh)
    else:
        return ('2v', f_count_zh, s_count_zh, f_zh, s_zh)

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

def extract_features(en, zh):
    last_participant = None
    last_en = ""
    last_zh = ""
    for l_en in en.readlines():
        l_zh = zh.readline()
        # make sure they're both either <DOC lines or _not_ <DOC lines
        assert((re.match("^<DOC" , l_en) is None) == (re.match("^<DOC" , l_zh) is None))
        assert((re.match("^</DOC", l_en) is None) == (re.match("^</DOC", l_zh) is None))
        #if re.match("</DOC", l_en):
            #print 
        m_en = re.match('^<seg id="([^"]+)" msg_id="([^"]+)" participant="([^"]+)"> +(.+) +</seg>', l_en)
        m_zh = re.match('^<seg id="([^"]+)" msg_id="([^"]+)" participant="([^"]+)"> +(.+) +</seg>', l_zh)
        if m_en is not None:
            # make sure they match
            assert(m_zh is not None)
            assert(m_en.group(1) == m_zh.group(1))
            assert(m_en.group(2) == m_zh.group(2))
            assert(m_en.group(3) == m_zh.group(3))
            zh_sent = m_zh.group(4)
            zh_sent = zh_sent.strip("\n")
            #zh_sent += "\n"
	    print zh_sent
        else:
            assert(m_zh is None)


def do_main(argv):
    if len(argv) != 4:
	print "usage: python extract_for_pos_tagging.py --en-file <file> --zh-file <file>"
	return
    parser = OptionParser()
    parser.add_option("--en-file", dest="en_file", action="store",
                  help="write report to FILE", metavar="FILE")
    parser.add_option("--zh-file", dest="zh_file", action="store",
                  help="write report to FILE", metavar="FILE")
    (options, args) = parser.parse_args()
    en = open(options.en_file)
    zh = open(options.zh_file)
    extract_features(en, zh)
    en.close()
    zh.close()

if __name__ == '__main__': do_main(sys.argv[1:])
    

