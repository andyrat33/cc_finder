import re
import os
from collections import Counter

cc_pattern1 = re.compile(b"4[0-9]{12}(?:[0-9]{3})?|3[47][0-9]{13}|6(?:011|5[0-9]{2})[0-9]{12}")
path = ("/etc","/home","/usr")
extension = '.csv'
results_total = list()
total_count = Counter()

def cc_check(filename):
    results = list()
    linePos=1
    try:
        cc_file = open(filename, mode='rb')
    except IOError as e:
        print("Error: {}".format(e))
    else:
        with cc_file:
            for line in cc_file:
                for match in cc_pattern1.findall(line):
                    results.append( (match,filename,linePos) )
                linePos+=1
                    
    return results

for each_dir in path:
    for dir, subdir, fileList in os.walk(each_dir):
        for fname in fileList:
            if os.path.splitext(fname)[-1] == extension:
                file_name_path = os.path.join(dir, fname)
                cc_results = cc_check(file_name_path)
                if len(cc_results) != 0:
                    results_total.append(cc_results)

for item in results_total:
    for line in item:
        print("{}:{}:{}".format(line[1], line[2],line[0].decode('ASCII')))
    total_count += Counter([i[1] for i in item])

for result in total_count.most_common():
    print("{:50} {}".format(result[0],result[1]))
