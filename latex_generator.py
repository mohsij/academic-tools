import os
import subprocess
import random

cpp_files = [file for file in os.listdir() if "cpp" in file]

latex = [
"\question[{marksForQuestion}]\n",
r"\begin{samepage}","\n", 
r"\begin{tcolorbox}","\n",
r"\begin{lstlisting}","\n",
"{codeblock}","\n",
r"\end{lstlisting}","\n",
r"\end{tcolorbox}","\n",
r"What is the output when trying to compile and run the above code?","\n",
r"\begin{itemize}[leftmargin=.2\linewidth]","\n",
"\n",
"\t\\item[\\textbf{A:}] answerA","\n",
"\t\\item[\\textbf{B:}] answerB","\n",
"\t\\item[\\textbf{C:}] answerC","\n",
"\t\\item[\\textbf{D:}] answerD","\n",
"\n"
r"\begin{solution}","\n",
"{codeSolution}","\n",
r"\end{solution}","\n",
r"\end{itemize}","\n",
r"%\droptotalpoints","\n",
r"% \newpage","\n",
r"\rule{8cm}{0.1pt}","\n",
r"\end{samepage}","\n",
]

count = 1

choices = ['A', 'B', 'C', 'D']

for cpp_file in cpp_files:
    answer = None
    marks = 3 if count <= 4 else 4
    random_choice = random.choice(choices)
    if os.system("g++ -std=c++11 -o main {} >/dev/null 2>&1".format(cpp_file)) == 0:
        answer = subprocess.run(['./main'], stdout=subprocess.PIPE).stdout.decode('utf-8').replace('\n', '')
    else:
        answer = "Does not compile"
    choiceLine = "answer{}".format(random_choice)
    with open(cpp_file.replace('cpp', 'tex'), 'w') as texFile:
        for line in latex:
            if "codeblock" in line:
                with open(cpp_file, 'r') as file:
                    file_data = file.read()
                texFile.write(line.format(codeblock=file_data))
            elif choiceLine in line:
                texFile.write(line.replace(choiceLine, answer))
            elif "codeSolution" in line:
                texFile.write(line.format(codeSolution=random_choice)) 
            elif "marksForQuestion" in line:
                texFile.write(line.format(marksForQuestion=marks))
            else:
                texFile.write(line)
    count += 1
    break