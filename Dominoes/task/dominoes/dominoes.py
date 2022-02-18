import random
from typing import List

dominos: List[list] = [[x, y] for x in range(7) for y in range(x, 7)]
snake: List[list] = [[0, 0]]
status: str = ''


def generate_hands() -> tuple:
    global dominos
    dominos_clone: list = list(dominos)

    player_list: list = []
    computer_list: list = []

    for _ in range(7):
        piece1: List[int] = random.choice(dominos_clone)
        dominos_clone.remove(piece1)
        player_list.append(piece1)
        piece2: List[int] = random.choice(dominos_clone)
        dominos_clone.remove(piece2)
        computer_list.append(piece2)

    return player_list, computer_list, dominos_clone


def print_hand() -> None:
    for number, item in enumerate(player_hand):
        print(f"{number + 1}:{item}")


while True:

    player_hand, computer_hand, stock = generate_hands()

    if not any(filter(lambda x: x[0] == x[1], player_hand)) and not any(filter(lambda x: x[0] == x[1], computer_hand)):
        continue

    break


for player, computer in zip(player_hand, computer_hand):
    if sum(player) > sum(snake[0]):
        snake = [player]
        status = 'computer'
    if sum(computer) > sum(snake[0]):
        snake = [computer]
        status = 'player'


if status == 'player':
    computer_hand.remove(snake[0])
elif status == 'computer':
    player_hand.remove(snake[0])


while True:

    print("======================================================================")
    print(f"Stock size: {len(stock)}")
    print(f"Computer pieces: {len(computer_hand)}\n")
    if len(snake) <= 6:
        print(*snake)
    else:
        print(*snake[:3], '...', *snake[-3:], sep='')
    print("\nYour pieces:")
    print_hand()

    if status == 'player':
        status = 'computer'
        print("\nStatus: It's your turn to make a move. Enter your command.")
        while True:
            try:
                move = int(input())
            except ValueError:
                print("Invalid input. Please try again.")
                continue
            finally:
                if abs(move) > len(player_hand):
                    print("Invalid input. Please try again.")
                    continue
            if move == 0:
                if stock:
                    piece = random.choice(stock)
                    player_hand.append(piece)
                    stock.remove(piece)
            elif move > 0:
                move -= 1
                piece = player_hand[move]
                if snake[-1][-1] not in piece:
                    print("Illegal move. Please try again.")
                    continue
                elif piece[1] == snake[-1][-1] and piece[0] != snake[-1][-1]:
                    snake.append([piece[1], piece[0]])
                else:
                    snake.append(piece)
                player_hand.remove(piece)
            elif move < 0:
                move = abs(move) - 1
                piece = player_hand[move]
                if snake[0][0] not in piece:
                    print("Illegal move. Please try again.")
                    continue
                elif piece[0] == snake[0][0] and piece[1] != snake[0][0]:
                    snake.insert(0, [piece[1], piece[0]])
                else:
                    snake.insert(0, piece)
                player_hand.remove(piece)

            break
    elif status == 'computer':
        status = 'player'
        input("\nStatus: Computer is about to make a move. Press Enter to continue...\n")
        attempts = 0
        counts = {}

        for domino in computer_hand:
            for num in domino:
                counts[num] = counts.get(num, 0) + 1

        for domino in snake:
            for num in domino:
                counts[num] = counts.get(num, 0) + 1

        top_picks = {tuple(key): counts[key[0]] + counts[key[1]] for key in computer_hand}
        top_picks = sorted(top_picks, key=lambda x: top_picks[x], reverse=True)

        while True:

            move = list(top_picks[attempts])
            attempts += 1

            if len(top_picks) == attempts:
                if stock:
                    piece = random.choice(stock)
                    computer_hand.append(piece)
                    stock.remove(piece)
            elif snake[0][0] in move:
                if move[0] == snake[0][0] and move[1] != snake[0][0]:
                    snake.insert(0, [move[1], move[1]])
                    computer_hand.remove(move)
                else:
                    snake.insert(0, move)
                    computer_hand.remove(move)
            elif snake[-1][-1] in move:
                if move[1] == snake[-1][-1] and move[0] != snake[-1][-1]:
                    snake.append([move[1], move[0]])
                    computer_hand.remove(move)
                else:
                    snake.append(move)
                    computer_hand.remove(move)
            else:
                continue

            break

        if not player_hand:
            print("Status: The game is over. You won!")
            break

        if not computer_hand:
            print("Status: The game is over. The computer won!")
            break

        if snake[0][0] == snake[-1][-1]:
            end_piece = snake[0][0]
            end_count = len([inner for outer in snake for inner in outer if inner == end_piece])
            if end_count >= 8:
                if status == 'player':
                    print("Status: The game is over. The computer won!")
                    break
                elif status == 'computer':
                    print("Status: The game is over. You won!")
                    break
            elif end_count >= 6:
                print("Status: The game is over. It's a draw!")
                break

        score = {}

        for domino in snake:
            for num in domino:
                score[num] = score.get(num, 0) + 1

        if max(score.values()) >= 8:
            print("Status: The game is over. It's a draw!")
            break
