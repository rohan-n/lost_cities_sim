import click
from defs import gameBoard, Player, Color, IllegalMove, Card, Deck
from lc_ai import evaluate_position
from pdb import set_trace

def main(): 
	print("--------------Welcome to Lost Cities, daring expeditioner--------------\n\n\n")
	deck = Deck()
	p1_hand = []
	p2_hand = []
	for i in range(8): 
		p1_hand.append(deck.draw())
		p2_hand.append(deck.draw())
	p1 = Player(p1_hand, 'Rohan')
	p2 = Player(p2_hand, 'Aneesh')
	board = gameBoard(p1, p2)
	PLAYER1_TURN = True
	while deck.remaining() > 0: 
		if PLAYER1_TURN: 
			cur_player = p1
		else: 
			cur_player = p2
			print("----- evaluate_position -----")
			ep = (evaluate_position(board.p2_played, p2.hand))
			print(ep[0])
			print(ep[1])
			print(ep[2])
			print("----- evaluate_position -----")
		click.secho("\n\nIt is {}'s turn!\n".format(cur_player.name), fg='red' if PLAYER1_TURN else 'blue')
		cur_player.repr_hand()
		print("Time to play a card!\n")
		card_idx = click.prompt("Play a card? (Hit enter to dump instead)", type=click.Choice(['a','s','d','f','g','h','j','k','']), 
			show_choices=False, default='')
		if card_idx == '': 
			dump_card_idx = click.prompt("Card to dump?", type=click.Choice(['a','s','d','f','g','h','j','k']), show_choices=False)
			card_to_play = cur_player.play_card(dump_card_idx)
			board.put_communal(card_to_play)
		else: 
			card_to_play = cur_player.play_card(card_idx)
			try: 
				board.put_player(cur_player, card_to_play)
			except IllegalMove: 
				click.echo("Illegal move! Cards need to be played in ascending rank order.")
				cur_player.add_to_hand(card_to_play)
				continue

		print("\nTime to draw a card!")
		end_of_turn = False
		while not end_of_turn: 
			draw_from = click.prompt("(D)eck or (C)ommunal?", type=click.Choice(['d','c']), show_choices=False)
			if draw_from == 'c': 
				board.repr_communal()
				draw_col = click.prompt("Which color stack?", type =click.Choice(['r','g','b','y','w']), show_choices=False)
				try: 
					card_drawn = board.draw_communal(draw_col.upper())
				except IllegalMove: 
					click.echo("That stack is empty!")
					continue
			else: 
				card_drawn = deck.draw()
			
			cur_player.add_to_hand(card_drawn)
			end_of_turn = True
		board.repr_board()
		print("End of Turn. Cards remaining: " + str(deck.remaining()))
		PLAYER1_TURN = not(PLAYER1_TURN)
	print(board.scoring())


main()