import sys
import gzip

def main(argv):
	sgm_file = open(argv[0])
	zh_file = gzip.open(argv[1])
	en_file = gzip.open(argv[2])
	zh_out = open(argv[3], 'w')
	en_out = open(argv[4], 'w')
	for sgm_line in sgm_file.readlines():
		if "<DOC" in sgm_line or "</DOC>" in sgm_line:
			zh_out.write(sgm_line)
			en_out.write(sgm_line)
			continue
		zh_line = zh_file.readline()
		en_line = en_file.readline()
		if zh_line == "":
			break
		zh_out.write(zh_line)
		en_out.write(en_line)

if __name__ == "__main__":
	main(sys.argv[1:])
