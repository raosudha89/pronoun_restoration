# -*- coding: utf-8 -*- 
import sys
import re
from collections import defaultdict
from optparse import OptionParser

def extract_features(en, zh):
    last_participant = None
    count = 0
    label_counts = ""
    for l_en in en.readlines():
        l_zh = zh.readline()
        # make sure they're both either <doc lines or _not_ <doc lines
        assert((re.match("^<DOC" , l_en) is None) == (re.match("^<DOC" , l_zh) is None))
        assert((re.match("^</DOC", l_en) is None) == (re.match("^</DOC", l_zh) is None))
        if re.match("</DOC", l_en):
	    label_counts += "%s " % (count)
	    print label_counts
	    label_counts = ""
    	    last_participant = None
	    count = 0
        m_en = re.match('^<seg id="([^"]+)" msg_id="([^"]+)" participant="([^"]+)"> +(.+) +</seg>', l_en)
        m_zh = re.match('^<seg id="([^"]+)" msg_id="([^"]+)" participant="([^"]+)"> +(.+) +</seg>', l_zh)
        if m_en is not None:
            # make sure they match
            assert(m_zh is not None)
            assert(m_en.group(1) == m_zh.group(1))
            assert(m_en.group(2) == m_zh.group(2))
            assert(m_en.group(3) == m_zh.group(3))
	    if m_en.group(3) != last_participant:
                if last_participant is not None:
		    label_counts += "%s " % (count)
                last_participant = m_en.group(3)
		count = 1
            else:
		count += 1
        else:
            assert(m_zh is None)


def do_main(argv):
    if len(argv) < 4:
	print "usage: python get_expanded_label_counts.py --en-file <file> --zh-file <file>"
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
    

