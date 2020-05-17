import click 
from enum import Enum
from functools import total_ordering
from random import shuffle as rand_shuffle

INPUT_MAPPING = {
	'a':0,
	's':1,
	'd':2,
	'f':3,
	'g':4,
	'h':5,
	'j':6,
	'k':7,
}
INV_INPUT_MAPPING = {v: k for k, v in INPUT_MAPPING.items()}

class IllegalMove(Exception): 
	pass

def put_safety_check(cur_played, want_to_play): 
	if len(cur_played) == 0: return
	latest_card_put_down = cur_played[-1]
	if want_to_play.rank == 'X': 
		if latest_card_put_down.rank != 'X': 
			raise IllegalMove
		else: 
			return
	if  latest_card_put_down.rank == 'X':
		return
	if latest_card_put_down.rank > want_to_play.rank or (
		latest_card_put_down.color != want_to_play.color): 
		raise IllegalMove

@total_ordering
class Color(Enum): 
	BLUE = 'B'
	GREEN = 'G'
	RED = 'R'
	WHITE = 'W'
	YELLOW = 'Y'

	def __le__(self, other): 
		return self.value <= other.value

	def __str__(self): 
		return self.value

@total_ordering
class Card: 
	def __init__(self, rank, color): 
		self.rank = rank
		self.color = color

	def __str__(self): 
		return self.color.value + str(self.rank)

	def __repr__(self): 
		return self.color.value + str(self.rank)

	def __le__(self, other):
		if self.rank != other.rank: 
			if self.rank == 'X':
				return False
			if other.rank == 'X':
				return True

			return self.rank  < other.rank
		else: 
			return self.color.value <= self.color.value 

class Deck: 
	def __init__(self): 
		self.cards = []
		for color in Color: 
			for rank in (list(range(2,11)) + ['X','X','X']): 
				self.cards.append(Card(rank, color))
		self.shuffle()

	def shuffle(self): 
		rand_shuffle(self.cards)

	def draw(self): 
		return self.cards.pop()

	def remaining(self): 
		return len(self.cards)

	def __repr__(self): 
		return str(self.cards)

class Player: 
	def __init__(self, hand, name): 
		self.hand = hand
		self.name = name
		self.sort_hand()

	def play_card(self, user_input): 
		card_pos = INPUT_MAPPING[user_input]
		return self.hand.pop(card_pos)

	def _sort_rank(self, x):
		if x == 'X': 
			return 0
		else:
			return int(x)

	def sort_hand(self): 
		self.hand = sorted(self.hand, key = lambda x: (x.color, self._sort_rank(x.rank)))

	def repr_hand(self): 
		for i in range(8): 
			print(INV_INPUT_MAPPING[i] + ' : ' + str(self.hand[i]))

	def add_to_hand(self, card): 
		self.hand.append(card)
		self.sort_hand()

	def __repr__(self): 
		return self.name

def score_stack(played_cards):
	score = 0
	if played_cards:
		stack_rank = [1,0]
		for card in played_cards:
			if card.rank == 'X':
				stack_rank[0] += 1
			else:
				stack_rank[1] += card.rank
		if len(played_cards) >= 8: 
			score += 20 
		score += stack_rank[0] * (stack_rank[1] - 20)
	return score

class gameBoard: 
	def __init__(self, p1, p2):
		self.p1 = p1.name
		self.p2 = p2.name
		self.p1_played = {c.value:[] for c in Color}
		self.p2_played = {c.value:[] for c in Color}
		self.communal = {c.value:[] for c in Color}

	def scoring(self): 
		def score_individual(player_board): 
			score = 0
			for _, played_cards in player_board.items(): 
				score += score_stack(played_cards)
			return score
		return {self.p1: score_individual(self.p1_played), self.p2: score_individual(self.p2_played)}

	def put_player(self, player, card): 
		col = card.color.value
		if player.name == self.p1: 
			cur_board = self.p1_played
		else: 
			cur_board = self.p2_played
		put_safety_check(cur_board[col], card)
		cur_board[col].append(card)
		
	def put_communal(self, card): 
		col = card.color.value
		self.communal[col].insert(0, card)
		self.communal = self.communal

	def draw_communal(self, color): 
		assert color in ('R','G','B','Y','W')
		comm_stack = self.communal[color]
		if not comm_stack: 
			raise IllegalMove
		return comm_stack.pop(0)

	def repr_communal(self):
		print("First element is the top-most that you will draw")
		print(self.communal)

	def repr_board(self): 
		click.secho("\n-- " + self.p1 + " --", fg='red')
		click.secho(str(self.p1_played), fg='red')
		print("\n-- COMMUNAL --")
		print(self.communal)
		click.secho("\n-- " + self.p2 + " --", fg='blue')
		click.secho(str(self.p2_played), fg='blue')
