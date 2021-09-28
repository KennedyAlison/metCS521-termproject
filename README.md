# metCS521-termproject
Python implementation creating a report from sample extracted code for Jira 

# Instructions 
In this project you will find the following items: 
- **TERM PROJECT** – Jira Analysis.py – This is the main file for the project. When this program is run, it will be asked for 3 input excel files which have also been provided. My program uses both pandas and datetime, if pandas is not already installed, the following can be run to install:
  - pip install pandas – if you have Anaconda installed, use this instead – conda install pandas
- **Sample Epic Data.xlsx** – This file should be used as the first input to the program when prompted to input an Epic excel filename
- **Sample Feature Data.xlsx** – This file should be used as the second input to the program when prompted to input a Feature excel filename
- **Sample Dependency Data.xlsx** – This file should be used as the third input to the program when prompted to input a Dependency excel filename
- **No Block Epic Data.xlsx** – This file is an alternative input file to be used as the first input to the program when prompted to input an Epic excel filename. Data differs from the Sample Epic Data as it contains no blocking Epics and will output a slightly different report
- **No Block Feature Data.xlsx** – This file is an alternative input file to be used as the second input to the program when prompted to input a Feature excel filename. Data differs from the Sample Feature Data as it contains no blocking Features and will output a slightly different report
- **No Block or Critical_High Dependency Data.xlsx** – This file is an alternative input file to be used as the third input to the program when prompted to input a Dependency excel filename. Data differs from the Sample Dependency Data as it contains no blocking Dependencies and no Critical or High Dependencies and will output a slightly different report

To run the program, run the TERM PROJECT – *Jira Analysis.py file* and use either *Sample Epic Data.xlsx* or *No Block Epic Data.xlsx* as the first input file, then use either *Sample Feature Data.xlsx* or *No Block Feature Data.xlsx* as the second input file, and finally use either *Sample Dependency Data.xlsx* or *No Block or Critical_High Dependency Data.xlsx* as the final input file. Once run, you will see a “Sample Report – MM_DD_YYYY.txt” output to your current directory. This sample file will contain summary statistics about the 3 input files. 
