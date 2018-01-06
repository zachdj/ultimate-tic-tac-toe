# Ultimate Tic Tac Toe

Ultimate Tic-Tac-Toe is a modification of the traditional game of tic-tac-toe with a much more interesting ruleset.  A full description of the rules can be found [here](https://mathwithbaddrawings.com/2013/06/16/ultimate-tic-tac-toe/).

This project includes:

  - A game engine for Ultimate Tic-Tac-Toe
  - An implementation of Monte Carlo Tree Search to play the game
  - An implementation of a few bots that use minimax search with a-B pruning to play the game
  - A tool for testing bots against other bots or human players

### Installation

This project requires [Python 3.5+](https://www.python.org/downloads/), [pip](https://pip.pypa.io/en/stable/installing/).  It's easiest to get setup if python and pip are in the system path.

Clone the repository:
```sh
$ git clone https://github.com/zachdj/ultimate-tic-tac-toe.git
```

Environment variables are stored in the `settings.py` file.  Here you can set the path the a local SQLite database that can store the results of experiments.  The `USING_OSX` variable should be set to `True` if you're running the software on a Mac.  This prevents a platform-specific bug caused by resizable windows in pygame.

Dependencies are managed using [pipenv](https://github.com/kennethreitz/pipenv).  Use pip to install pipenv:

```sh
$ pip install pipenv
```

Then cd to the project directory and install dependencies:

```sh
$ cd path/to/ultimate-tic-tac-toe
$ pipenv install
```

This will create a virtual environment for the project and install any required dependencies inside the virtual environment.  Finally, activate the virtual environment and run the main.py file:

```sh
$ pipenv shell
$ python main.py
```

### Usage

##### Using the GUI

Interacting with the program's graphical interface is straightforward.  Games can be played/visualized by clicking the "Play Game" button from the main menu.  Experiments (multiple games between bots) can be run from the "Run Experiment" menu.  If the "Record Result" option is enabled, the board states and their win rates will be stored in a local database specified by the `DB_LOCATION` option in `settings.py`.

### Development

Much of this codebase was developed as part of a class project for the course "CSCI 6550 - Intro to AI" at the University of Georgia in Fall 2017.  If you're interested in contributing, you can contact me at zach.dean.jones@gmail.com.

We setup the gmail account cs4380.uttt@gmail.com to sign up for various services such as Dropbox.

License
----

MIT
