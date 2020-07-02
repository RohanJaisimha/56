import random
from flask import Flask, render_template, request
import json
import random

application = Flask(__name__)
_deck = None
cards_played = ["&nbsp;" * 2] * 4
players = ["Rohan", "Rahul", "Dad", "Mom"]
scores = [0, 0]
new_deck = []
rounds = 0


class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.sorting_rubric = [
            ["d", "b", "a", "c"].index(self.suit),
            ["b", "9", "1", "a", "c", "d"].index(self.rank),
        ]

    def __str__(self):
        return (
            "<span style='color: "
            + ("red" if self.suit in ["b", "c"] else "black")
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
    def __init__(self, num_players=4, cards=None):
        if not cards:
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

    def cut(self):
        randnum = random.randrange(len(self.deck) // 4, 3 * len(self.deck) // 4)
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
    global rounds
    global players

    rounds += 1
    if rounds == 8:
        _deck = Deck(cards=new_deck)
        new_deck = []
        rounds = 0
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
