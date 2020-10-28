
Context-Free Grammar Interpreter
===
This package takes a CF grammar G and a word w as an input, transforms G into Chomsky normal form and performs the Cocke-Younger-Kasami-algorithm (CYK) to evaluate wether the word can be created by the grammar or not.
## Table of Contents
* **Requirements**
* **Usage**
* **Example**

## Usage

1. **Requirements**
    → Windows user (my condolences) need to download and install [miktex](https://miktex.org/download).
    
2. **Execute Program** 

    → Compile from command line using `python3 main.py` or execute `main.py` using your favourite IDE or text editor.

3. **Enter Grammar**

    → Enter the members of the grammar in order with following syntax:
        
    | Member  | Syntax/Input  |Output| 
    |---|---|---|
    | Symbols  | S, B, C...  | {S, B, C} | 
    | Terminal Symbols | a, b, c...  |{a, b, c}|
    | Rules per Symbol (eg. S:) |  B, a, \E  | {S -> B | a | \E | ...} |
    |Starting Symbol|S|S|

   → The grammar may also be entered through an external file with following regulations:
    
    Empty lines in the file will be ignored.

    | Order of lines | Grammar member | Rules | Example |
    |---|---|---|---|
    | 1 | Symbols | upper case letters | S,A,B |
    | 2 | Terminal Symbols | lower case letters | a,b |
    | 3 | Starting Symbol | part of Symbols | S |
    | 4 to x | Rules per Symbol | first character of the line is the Symbol | S -> AB, AA |
    | 4 to x | Rules per Symbol | '->' may be inserted for better clarity | A -> BA; a |
    | 4 to x | Rules per Symbol | applying rules are stated after the Symbol | B -> b |
    
    Notice that the notation for epsilon is \E. 
    Also note that the LaTeX table will go out of bound for long words. 
3. **Enter Word**

    → Enter the word, nothing fancy to it.
    → spam `enter` until done.

4. **Open PDF**

    → Open the .pdf file using `evince` or your favourite pdf viewer.

Example
---
- **Input:** 

![](https://i.imgur.com/E7otsnk.png)

- **Grammar in CNF:**

![](https://i.imgur.com/nMcuVZ0.png)

- **Finished CYK-Table of w = aaccca:**

![](https://i.imgur.com/nIM9x1X.png)

