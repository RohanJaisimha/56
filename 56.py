import random
from flask import Flask, render_template, request
import json

app = Flask(__name__)
_deck = None
cards_played = ["&nbsp;" * 2] * 4
players = ["Rohan", "Rahul", "Dad", "Mom"]
scores = [0, 0]


class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.sorting_rubric = [
            ["D", "B", "A", "C"].index(self.suit),
            ["B", "9", "1", "A"].index(self.rank),
        ]

    def __str__(self):
        return (
            "<span style='color: "
            + ("red" if self.suit in ["B", "C"] else "black")
            + "' onclick='playCard(this); this.outerHTML= \"\";'>&#x1F0"
            + self.suit
            + self.rank
            + ";</span>"
        )

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
    def __init__(self, num_players=4):
        self.deck = [
            Card(rank, suit)
            for rank in ["1", "9", "A", "B"]
            for suit in ["A", "B", "C", "D"]
            for i in range(2)
        ]
        self.hands = None

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self, players):
        self.hands = {
            players[i // 8]: sorted(self.deck[i : i + 8])
            for i in range(0, len(self.deck), 8)
        }

    def __str__(self):
        return repr(self)


@app.route("/")
def home():
    global _deck
    global cards_played
    global players
    global scores

    if not _deck:
        _deck = Deck(4)
        _deck.shuffle()
        _deck.deal(players)

    if not request.args.get("name"):
        return render_template("form.html")
    else:
        return render_template(
            "cards.html",
            hand=_deck.hands[request.args["name"]],
            cards_played=cards_played,
            players=players,
            scores=scores
        )


@app.route("/playCard", methods=["POST"])
def playCard():
    global cards_played
    cards_played[players.index(request.form["user"])] = request.form["card"]
    return json.dumps(cards_played)


@app.route("/refresh", methods=["POST"])
def refresh():
    global cards_played
    global scores
    return json.dumps(cards_played + scores)


@app.route("/clear_table", methods=["POST"])
def clear_table():
    global cards_played
    cards_played = ["&nbsp;" * 2] * 4
    return ""


@app.route("/update_scores", methods=["POST"])
def update_scores():
    global scores
    scores = json.loads(request.form["scores"])
    return ""


def main():
    app.run(host="0.0.0.0", port=5000, debug=True)


if __name__ == "__main__":
    main()
