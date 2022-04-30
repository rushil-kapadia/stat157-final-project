# stat157-final-project
# Setup
Ensure that your python version is 3.7. Install the required packages as follows:
```
pip install requiremnts.txt
```
Then download the Stockfish binary. For Mac users:
```
brew install stockfish
```
For Windows users, download the binary from https://stockfishchess.org/download/.

Then change the path to Stockfish (line 32) in question_gen.py to reflect the path to the Stockfish binary on your device. 
# Running the App
The following sequence of commands will launch the web app at http://127.0.0.1:5000.
```
export FLASK_APP=chessMain
export FLASK_ENV=development
flask run
```

If the app errors or the UI does not seem to be updating, please refresh it. If that does not work, restart it. These will usually resolve the issues, which came up on some operating systems and browsers. The most stable version is on Mac/Chrome, though we were able to get it working on Windows/Firefox (lots of refreshing).
