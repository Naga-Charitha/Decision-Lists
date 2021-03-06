# Decision-Lists
A Python program called decision-list.py that implements a decision list classifier to perform word sense disambiguation. 


$ python decision-list.py line-train.xml line-test.xml my-decision-list.txt > my-line-answers.txt

This command should learn a decision list from line-train.xml and apply that decision list to each of the sentences found in line-test.xml in order to assign a sense to the word line. Do not use line-test.xml in any other way (and only identify features from line-train.xml). The program should output the decision list it learns to my-decision-list.txt. 


line-train.xml contains examples of the word line used in the sense of a phone line and a product line where the correct sense is marked in the text (to serve as an example from which to learn). line- test.xml contains sentences that use the word line without any sense being indicated, where the correct answer is found in the file line-answers.txt. 


The program decision-list.py should learn its decision list from line-train.xml and then apply that to line-test.xml.


Also wrote a utility program called scorer.py which will take as input your sense tagged output and compare it with the gold standard "key" data in line-answers.txt. The scorer program should report the overall accuracy of your tagging, and provide a confusion matrix.


The scorer program should be run as follows:
$ python scorer.py my-line-answers.txt line-answers.txt
A script file called decision-list-log.txt that was created as follows:
$ script decision-list-log.txt
$ python decision-list.py line-train.xml line-test.xml my-decision-list.txt > my-line-answers.txt
$ head -50 my-decision-list.txt
$ head -10 my-line-answers.txt
$ python scorer.py my-line-answers.txt line-answers.txt
$ exit
