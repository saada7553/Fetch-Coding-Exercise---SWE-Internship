Requirements to run: 
	-Python
	-Pandas on python
If you do not have pandas, you can use "pip install pandas" in the terminal and it will 
install the necessary files

The main.py file takes 2 arguments, points to spend and the CSV. The location of the CSV must be in the 
current working directory. It is best to just keep the CSV and main.py in the same folder. 

To run, on windows, go to the terminal and navigate to the folder with the files. Then, type 

"python main.py (points) (name of CSV)"

For example, if I want to spend 5000 points, and the name of the file is "transactions", this would be
the command: 

python main.py 5000 transactions.csv

The output will be shown in the terminal as a JSON object. 
