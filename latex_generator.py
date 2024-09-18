import os
import subprocess
import random

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

choices = ['A', 'B', 'C', 'D']

######### For the user to specify ##########################
questions_count = 26

questions_with_segfaults = [7]

marks_for_each_question = [3 if count <= 3 else 4 for count in range(questions_count)]

# Questions are from 1-26
cpp_files = ['q{}.cpp'.format(i) for i in range(1, questions_count+1)]

does_not_compile_answer = "Does not compile"
segfault_answer = "Segmentation fault/Undefined behaviour"

############################################################

for cpp_file in cpp_files:
    if not os.path.exists(cpp_file):
        continue
    answer = None
    question_index = int(cpp_file.split('.')[0][1:])
    marks = marks_for_each_question[question_index]
    random_choices = random.sample(choices, 2)
    correct_random_choice = random_choices[0]
    incorrect_random_choice = random_choices[1]
    if question_index in questions_with_segfaults:
        answer = segfault_answer
    else:
        # Suppress the output from the compilation in case there are warnings
        if os.system("g++ -std=c++11 -o main {} >/dev/null 2>&1".format(cpp_file)) == 0:
            answer = subprocess.run(['./main'], stdout=subprocess.PIPE).stdout.decode('utf-8').replace('\n', '')
        else:
            answer = does_not_compile_answer
    correctChoiceLine = "answer{}".format(correct_random_choice)
    incorrectChoiceLine = "answer{}".format(incorrect_random_choice)
    with open(os.path.join("texfiles", cpp_file.replace('cpp', 'tex')), 'w') as texFile:
        for line in latex:
            if "codeblock" in line:
                with open(cpp_file, 'r') as file:
                    file_data = file.read()
                texFile.write(line.format(codeblock=file_data))
            # write the correct answer at the respective choice's line
            elif correctChoiceLine in line:
                texFile.write(line.replace(correctChoiceLine, answer))
            # if the correct answer is not "does not compile" then make one of the incorrect choices that
            elif incorrectChoiceLine in line and not (answer == does_not_compile_answer):
                texFile.write(line.replace(incorrectChoiceLine, does_not_compile_answer))
            elif "codeSolution" in line:
                texFile.write(line.format(codeSolution=correct_random_choice)) 
            elif "marksForQuestion" in line:
                texFile.write(line.format(marksForQuestion=marks))
            else:
                texFile.write(line)