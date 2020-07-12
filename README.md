# 56
56 is a card game, hosted using AWS at [56.roartec.com](56.roartec.com)

# Get started
* Clone the repository / download the files. Open your terminal and navigate to this directory
* Install the required modules using `pip install -r requirements.txt`
* Run `application.py` by typing `python3  application.py`
* Open your handy-dandy browser and go to `localhost:5000`

# Files
* application.py - The main driver of the program. Uses [Flask](https://flask.palletsprojects.com/en/1.1.x/)
* templates/form.html - When you first navigate to the url, this is the first page you see. Select your name and hit submit.
* templates/56.html - Where everything happens

# How to play
* Corral a group of four of your pals
* Nominate one (1) person to be the admin (basically the chief clicker)
* Change the `teams` variable in `application.py` (Line 15) to your own names 
* Open your terminal and run `ifconfig` or `ipconfig` to find the IP address of your machine
* Run `application.py` and tell your gang of misfits to go open their browser and type in your IP address, followed by `:5000`
* Each person selects their own name and hits submit
* Each person should now see their hand of 8 cards
* Bidding and trump selection is done offline (may or may not be a feature added soon)
* Once you've sorted that out, the player who has to play first clicks on his card. This card should pop up on everybody else's screen in 5 seconds
* Keep going in order until all players have played a card
* Once all players have played, the admin clicks on the button corresponding to the team that won the round. This will update the score in the top-right
* Then they should click `Clear` one (1) time to end the round
* Once 8 rounds have been played, and `Clear` has been clicked 8 times, look at the final scores in the top right of the page
* Refresh the webpage and you will see new hands dealt for a new round
