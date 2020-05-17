from defs import Color, put_safety_check, IllegalMove, score_stack
# Assume default computer player is p2

def evaluate_position(comp_played, hand): 
	def value_add(stack, card):
		try: 
			put_safety_check(stack, card)
		except IllegalMove: 
			raise IllegalMove
		return card.rank
	# short_term_info: (value add for a card, previous card) for the immediate next turn
	short_term_info = {c.value:(0,None) for c in Color}
	# long_term_info: (value add for a color, number of cards in color) for the long game
	long_term_info = {c.value:[0,0] for c in Color}
	# This iteration will definitely go in sorted hand order
	trash_cards = []
	for card in hand:
		col = card.color.value
		stack = comp_played[col]
		try: 
			va = value_add(stack, card)
		except IllegalMove:
			trash_cards.append(card)
			continue
		if short_term_info[col][0] == 0: 
			short_term_info[col] = (card.rank, stack[-1] if stack else None)
		stack.append(card)
		long_term_info[col][0] = score_stack(stack)
		long_term_info[col][1] = long_term_info[col][1] + 1
	return short_term_info, long_term_info, trash_cards



def make_move_v0(board, hand, remaining): 
	# type: (gameBoard, List[Card], int) -> (str, Card)
	# Only make a move based on card info and # of turns left 
	# Output will be  tuple of (['draw','dump'], Card)
	pass