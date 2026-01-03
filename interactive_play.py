from baip import Baip


def get_move(high):
    if high == 1:
        return 0
    while True:
        try:
            num = int(input("Choose a move: "))
            if num >= 0 and num < high:
                return num
        except ValueError:
            pass
        print("invalid move")


def main():
    b = Baip()
    b.print_state()

    turn = 0
    while True:
        print()
        print(f"player {b.player} turn {turn // 2}")

        placements = b.get_legal_placements()
        print("Choose a move")
        for i, place in enumerate(placements):
            piece = "kit" if place.piece == Baip.PieceType.KIT else "cat"
            print(f"{i}. {piece} at {(place.x, place.y)}")
        num = get_move(len(placements))
        place = placements[num]
        b = b.apply_placement(place)
        b.print_state()

        if b.is_terminal():
            print(f"Player {b.player} wins!")
            break

        removes = b.get_legal_removes()
        promotions = b.get_legal_promotions()
        if len(removes) > 0 or len(promotions) > 0:
            count = 0
            for rem in removes:
                print(f"{count}. remove {rem}")
                count += 1
            for prom in promotions:
                x, y, dx, dy = prom
                print(f"{count}. promote {(x, y)}, {(x+dx, y+dy)}, {(x+2*dx, y+2*dy)}")
                count += 1
            num = get_move(len(promotions) + len(removes))
            if num < len(removes):
                rem = removes[num]
                b = b.apply_remove(*rem)
            else:
                num -= len(removes)
                prom = promotions[num]
                b = b.apply_promotion(*prom)

            b.print_state()

        b = b.next_turn()

        print("----------------------")
        turn += 1


if __name__ == "__main__":
    main()
