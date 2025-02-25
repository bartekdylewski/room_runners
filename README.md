# room_runners
A script created for my discrete maths project.
I added my own **generator of inputs** to test and optimize my code.
The problem is described in Polish in the* **.pdf**

A more sophisticated method is to use number theory to find something like congruences of the kids, and then solve the Chineese Reminder Theorem to find the iteration in which the kids are in specified rooms.

To run the automatic script, make sure you installed git.
```sh
sudo apt-get install git
```
\
Then you can open the respsitory folder in git bash and run:

```sh
bash auto.sh
```
^ for automated **generating, testing and saving** important files, or
```sh
bash auto_single.sh
```
^ for single test
\
\
You can edit the constatnts of **deciding if a file is important** or not in rooms.py
```py
# Constants
PRINT_ALL = False # print all additional info
INPUT_NAME = "generated.txt" # input file name
DURATION_FOR_SAVE_TAK = 2 # in ms
DURATION_FOR_SAVE_NIE = 100 # in ms
```

^ you can also turn on additional prints to see what is happening under the hood
\
\
You can change generation settings in generator.py file
```py
# you can change the max values of theese constants in generator.py
n = 500
k = 100
X = 20
Y = 10
```
\
Other things to improve it .....
- [X] Make code faster
- [X] Clean up prints
- [ ] Update comments
- [ ] Simplify code
- [ ] Add cli flags to python script
- [ ] Try and launch both files in main.py
- [ ] Test saving history in ordered tuples
