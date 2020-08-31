
Context-Free Grammar Evaluator
===
This package takes a CF grammar G and a word w as an input, transforms G into Chomsky NF and performs the Cocke-Younger-Kasami-algorithm (CYK) to avaluate wether the word can be created by the grammar or not.
## Table of Contents

* **User Manual**
* **Example**

## User Manual

1. **Execute Program** 
    → Compile from command line using `python3 main.py` or execute `main.py` using your favourite IDE or text editor.

2. **Enter Grammar**
    → Enter the members of the grammar in order with following syntax:
    | Member  | Syntax/Input  |Output| 
    |---|---|---|
    | Symbols  | A, B, C...  | {A, B, C} | 
    | Terminal Symbols | a, b, c...  |{a, b, c}|
    | Rules per Symbol (eg. A:) |  B, a, \E  | {A -> B ; a ; \E,...} |
    |Starting Symbol|A|A|
    
    Notice that the notation for epsilon is \E. 
    Also note that the LaTeX table will go out of bound for long words. 
3. **Enter Word**
    → Enter the word, nothing fancy to it.

4. **Open PDF File**
    → Open the PDF file to see the table resulting from the CYK algorithm and wether the word can be created or not.

Example
---
- **Input:** 

![](https://i.imgur.com/E7otsnk.png)

- **Grammar in CNF:**

![](https://i.imgur.com/nMcuVZ0.png)

- **Finished CYK-Table of w = aaccca:**

![](https://i.imgur.com/nIM9x1X.png)

