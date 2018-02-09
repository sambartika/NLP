import sys
import os
import re
import pprint

#The regex for email address
email_pat_1 = '([\w-]+)\s*(@|\(at\)|WHERE|\s+at\s+|&#x40;|\(followed by &ldquo;@)\s*(([\w-]+\s*(\.|;|dot|DOM|at)\s*)+)(-?[eE]-?[dD]-?[uU]|com)'
email_pat_2 = 'obfuscate\(\'(([\w-]+\s*(\.|;|dot|DOM)\s*)+)(-?[eE]-?[dD]-?[uU]|com)\',\'(\w+)\'\)'
#The regex for phone number
phone_pat_1 = '\(?(\d{3})(\)\s*|\s|-|\&thinsp;|\.|\/)(\d{3})(\s|-|\&thinsp;|\.|\/)(\d{4})\D+'

""" 
TODO
This function takes in a filename along with the file object (actually
a StringIO object) and
scans its contents against regex patterns. It returns a list of
(filename, type, value) tuples where type is either an 'e' or a 'p'
for e-mail or phone, and value is the formatted phone number or e-mail.
The canonical formats are:
     (name, 'p', '###-###-#####')
     (name, 'e', 'someone@something')
If the numbers you submit are formatted differently they will not
match the gold answers

NOTE: ***don't change this interface***

NOTE: You shouldn't need to worry about this, but just so you know, the
'f' parameter below will be of type StringIO. So, make
sure you check the StringIO interface if you do anything really tricky,
though StringIO should support most everything.
"""
def process_file(name, f):
    # note that debug info should be printed to stderr
    res = []
    for line in f:
        matches = re.findall(email_pat_1,line, re.IGNORECASE)
		#Extract email address from the string
        for m in matches:
            ls = list(m)
            email=""
            for i in range(len(ls)):
                if i == 0:
                    email=email+ls[i]
                elif i == 1:
                    email=email+"@"
                elif (i-2)%3 ==0:
                    email=email+ls[i]
                elif i==(len(ls)-1):
                    email=email+ls[i]
            email=email.replace("-","").replace(";",".").replace(" dot ",".").replace(" DOM ", ".").replace(" ","")
            if ls[0]!="Server":
				res.append((name,'e',email))
            
        matches = re.findall(email_pat_2,line)
		#Extract email address from the string
        for m in matches:
            ls = list(m)
            email=""
            for i in range(len(ls)):
                if i%3 == 0:
                    email=email+ls[i]
                elif i==(len(ls)-1):
                    email=ls[i]+"@"+email
            email=email.replace("-","").replace(";",".").replace(" dot ",".").replace(" DOM ", ".").replace(" ","")
            res.append((name,'e',email))
        
		#Extract phone number from the string
        matches = re.findall(phone_pat_1,line)
        for m in matches:
            phone=m[0]+"-"+m[2]+"-"+m[4]
            res.append((name,'p',phone))
    return res

"""
You should not need to edit this function, nor should you alter
its interface
"""
def process_dir(data_path):
    # get candidates
    guess_list = []
    for fname in os.listdir(data_path):
        if fname[0] == '.':
            continue
        path = os.path.join(data_path,fname)
        f = open(path,'r')
        f_guesses = process_file(fname, f)
        guess_list.extend(f_guesses)
    return guess_list

"""
You should not need to edit this function.
Given a path to a tsv file of gold e-mails and phone numbers
this function returns a list of tuples of the canonical form:
(filename, type, value)
"""
def get_gold(gold_path):
    # get gold answers
    gold_list = []
    f_gold = open(gold_path,'r')
    for line in f_gold:
        gold_list.append(tuple(line.strip().split('\t')))
    return gold_list

"""
You should not need to edit this function.
Given a list of guessed contacts and gold contacts, this function
computes the intersection and set differences, to compute the true
positives, false positives and false negatives.  Importantly, it
converts all of the values to lower case before comparing
"""
def score(guess_list, gold_list):
    guess_list = [(fname, _type, value.lower()) for (fname, _type, value) in guess_list]
    gold_list = [(fname, _type, value.lower()) for (fname, _type, value) in gold_list]
    guess_set = set(guess_list)
    gold_set = set(gold_list)

    tp = guess_set.intersection(gold_set)
    fp = guess_set - gold_set
    fn = gold_set - guess_set

    pp = pprint.PrettyPrinter()
    #print 'Guesses (%d): ' % len(guess_set)
    #pp.pprint(guess_set)
    #print 'Gold (%d): ' % len(gold_set)
    #pp.pprint(gold_set)
    print 'True Positives (%d): ' % len(tp)
    pp.pprint(tp)
    print 'False Positives (%d): ' % len(fp)
    pp.pprint(fp)
    print 'False Negatives (%d): ' % len(fn)
    pp.pprint(fn)
    print 'Summary: tp=%d, fp=%d, fn=%d' % (len(tp),len(fp),len(fn))

"""
You should not need to edit this function.
It takes in the string path to the data directory and the
gold file
"""
def main(data_path, gold_path):
    guess_list = process_dir(data_path)
    gold_list =  get_gold(gold_path)
    score(guess_list, gold_list)

"""
commandline interface takes a directory name and gold file.
It then processes each file within that directory and extracts any
matching e-mails or phone numbers and compares them to the gold file
"""
if __name__ == '__main__':
    if (len(sys.argv) != 3):
        print 'usage:\tSpamLord.py <data_dir> <gold_file>'
        sys.exit(0)
    main(sys.argv[1],sys.argv[2])
