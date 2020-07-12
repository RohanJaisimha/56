import random
from flask import Flask, render_template, request
import json
import random
import numpy as np

application = Flask(__name__)

_deck = None
cards_played = ["&nbsp;" * 2] * 4
scores = [0, 0]
new_deck = []
num_rounds = 0

# Change this if your names aren't Rohan, Rahul, Mom, and Dad
teams = [["Rohan", "Dad"], ["Rahul", "Mom"]]

# Puts the players into playing order, i.e, alternate teammates
players = list(np.array(list(zip(*teams))).flatten())


class Card:
    def __init__(self, rank, suit):
        # suit: d - Clubs, b - Hearts, a - Spades, c - Diamonds
        # rank: b - Jack, 9 - 9, 1 - Ace, a - 10, c - King, d - Queen
        self.rank = rank
        self.suit = suit
        self.color = "red" if suit in ["b", "c"] else "black"

        # sort by suit, and then rank
        self.sorting_rubric = [
            ["d", "b", "a", "c"].index(self.suit),
            ["b", "9", "1", "a", "c", "d"].index(self.rank),
        ]

    def __str__(self):
        return "&#x1F0" + self.suit + self.rank + ";"

    def __repr__(self):
        return str(self)

    def __gt__(self, other):
        return self.sorting_rubric > other.sorting_rubric

    def __lt__(self, other):
        return self.sorting_rubric < other.sorting_rubric

    def __ge__(self, other):
        return not self.__lt__(other)

    def __le__(self, other):
        return not self.__gt__(other)


class Deck:
    def __init__(self, num_players=4, cards=None):
        if not cards:
            # suit: d - Clubs, b - Hearts, a - Spades, c - Diamonds
            # rank: b - Jack, 9 - 9, 1 - Ace, a - 10, c - King, d - Queen
            self.deck = [
                Card(rank, suit)
                for rank in ["1", "9", "a", "b", "c", "d"][:num_players]
                for suit in ["a", "b", "c", "d"]
                for i in range(2)
            ]
        else:
            self.deck = cards
        self.hands = None

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self, players):
        self.hands = {player: [] for player in players}
        for i in range(0, len(self.deck), 4):
            self.hands[players[(i // 4) % 4]].extend(self.deck[i : i + 4])

        # sort each hand
        for player in players:
            self.hands[player].sort()

    def riffle_shuffle(self):
        halves = [self.deck[: len(self.deck) // 2], self.deck[len(self.deck) // 2 :]]
        self.deck = list(np.array(list(zip(*halves))).flatten())

    def cut(self):
        randnum = random.randrange(0, len(self.deck))
        self.deck = self.deck[randnum:] + self.deck[:randnum]

    def __str__(self):
        return str(self.hands)


@application.route("/")
def home():
    global _deck
    global cards_played
    global players
    global scores

    if not _deck:
        _deck = Deck(4)
        _deck.shuffle()
        for i in range(random.randrange(2, 6)):
            _deck.cut()
        _deck.deal(players)

    if not request.args.get("name"):
        # if the query string doesn't have 'name' in it, then the user hasn't filled out the form, so direct them to the form
        return render_template("form.html", players=players)
    else:
        user = request.args["name"]
        return render_template(
            "56.html",
            hand=_deck.hands[user],
            cards_played=cards_played,
            players=players,
            scores=scores,
        )


@application.route("/playCard", methods=["POST"])
def playCard():
    global cards_played
    global players
    global _deck
    global new_deck

    # When a card is played, we have to do four things:

    # 1) Add the card to cards_played
    user = request.form["user"]
    cards_played[players.index(user)] = request.form["card"]

    # 2) Remove the card from the players hand
    idx = 0
    for i, card in enumerate(_deck.hands[user]):
        if card.rank == request.form["rank"] and card.suit == request.form["suit"]:
            idx = i
            break
    _deck.hands[user].pop(idx)

    # 3) Add the card to new_deck so that we know the order in which cards were played
    new_deck.append(Card(request.form["rank"], request.form["suit"]))

    # 4) Return a JSONified version of cards_played so that we can update the webpage
    return json.dumps(cards_played)


@application.route("/refresh", methods=["POST"])
def refresh():
    global cards_played
    global scores

    # Every five seconds, the webpage auto-refreshes, asking for an update on the cards that have been played so far in that round, as well as the scores
    return json.dumps(cards_played + scores)


@application.route("/clear_table", methods=["POST"])
def clear_table():
    global cards_played
    global _deck
    global new_deck
    global num_rounds
    global players
    global scores

    # The table is cleared iff a round is complete
    num_rounds += 1

    if num_rounds == 8:
        # Each game is only 8 rounds long, so when 8 rounds have been played:
        # 1) Reset the scores back to 0
        scores = [0, 0]

        # 2) Reset the counter for number of rounds played to 0
        num_rounds = 0

        # 3) Set the deck to the new_deck, cut, and deal
        _deck = Deck(cards=new_deck)
        new_deck = []
        num_rounds = 0
        for i in range(random.randrange(2, 6)):
            _deck.cut()
        _deck.deal(players)

    # reset the cards_played to blank
    cards_played = ["&nbsp;" * 2] * 4

    # We have to return something so return an empty string
    return ""


@application.route("/update_scores", methods=["POST"])
def update_scores():
    global scores

    scores = json.loads(request.form["scores"])

    # We have to return something so return an empty string
    return ""


def main():
    application.run(host="0.0.0.0", port=5000, debug=True)


if __name__ == "__main__":
    main()
