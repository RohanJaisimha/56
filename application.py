import random
from flask import Flask, render_template, request
import json
import random
import numpy as np

application = Flask(__name__)
_deck = None
cards_played = ["&nbsp;" * 2] * 4
teams = [["Rohan", "Dad"], ["Rahul", "Mom"]]
players = list(np.array(list(zip(*teams))).flatten())
scores = [0, 0]
new_deck = []
num_rounds = 0


class Card:
    def __init__(self, rank, suit):
        # suit: d - Clubs, b - Hearts, a - Spades, c - Diamonds
        # rank: b - Jack, 9 - 9, 1 - Ace, a - 10, c - King, d - Queen
        self.rank = rank
        self.suit = suit
        self.sorting_rubric = [
            ["d", "b", "a", "c"].index(self.suit),
            ["b", "9", "1", "a", "c", "d"].index(self.rank),
        ]
        self.color = "red" if suit in ["b", "c"] else "black"

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
        self.hands = {
            players[i // 8]: sorted(self.deck[i : i + 8])
            for i in range(0, len(self.deck), 8)
        }

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
        return render_template("form.html")
    else:
        return render_template(
            "cards.html",
            hand=_deck.hands[request.args["name"]],
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

    cards_played[players.index(request.form["user"])] = request.form["card"]
    idx = 9
    for i, card in enumerate(_deck.hands[request.form["user"]]):
        if card.rank == request.form["rank"] and card.suit == request.form["suit"]:
            idx = i
            break
    _deck.hands[request.form["user"]].pop(idx)
    new_deck.append(Card(request.form["rank"], request.form["suit"]))
    return json.dumps(cards_played)


@application.route("/refresh", methods=["POST"])
def refresh():
    global cards_played
    global scores

    return json.dumps(cards_played + scores)


@application.route("/clear_table", methods=["POST"])
def clear_table():
    global cards_played
    global _deck
    global new_deck
    global num_rounds
    global players
    global scores

    num_rounds += 1
    if num_rounds == 8:
        _deck = Deck(cards=new_deck)
        new_deck = []
        scores = [0, 0]
        num_rounds = 0
        for i in range(random.randrange(2, 6)):
            _deck.cut()
        _deck.deal(players)
    cards_played = ["&nbsp;" * 2] * 4
    return ""


@application.route("/update_scores", methods=["POST"])
def update_scores():
    global scores

    scores = json.loads(request.form["scores"])
    return ""


def main():
    application.run(host="0.0.0.0", port=5000, debug=True)


if __name__ == "__main__":
    main()
