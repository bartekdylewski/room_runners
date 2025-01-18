# room_runners
A script created for my discrete maths project.
I added my own **generator of inputs** to test and optimize my code.
The problem is described in Polish in the* **.pdf**
More documentation will be available *soon*.

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
You can edit the constatnts of **deciding if a file is important** or not in:
```py
def save_input_file(result, duration):
    duration_for_save_tak = 0.5 # duration [in ms] over which we will save the file if the game does end
    duration_for_save_nie = 100 # duration [in ms] over which we will save the file if the game loops around
```

```py
# you can change the max values of theese constants in generator.py
n = 1000
k = 100
X = 20
Y = 10
```

More documentation, and features coming soon.....