from baip import Baip
import random


def main():
    b = Baip()
    b.print_state()

    turn = 0
    while True:
        print()
        print(f"player {b.player} turn {turn // 2}")

        placements = b.get_legal_placements()
        place = random.choice(placements)
        piece = "kit" if place.piece == Baip.PieceType.KIT else "cat"
        print(f" place {piece} at {(place.x, place.y)}")
        b = b.apply_placement(place)
        b.print_state()

        if b.is_terminal():
            print(f"Player {b.player} wins!")
            break

        removes = b.get_legal_removes()
        promotions = b.get_legal_promotions()
        if len(removes) > 0 or len(promotions) > 0:
            print()
            if len(removes) > 0 and len(promotions) > 0:
                if random.choice((0, 1)) == 1:
                    print(" choosing promotions")
                    removes = []
                else:
                    print(" choosing removes")
                    promotions = []
            if len(removes) > 0:
                rem = random.choice(removes)
                print(f" Removing {rem}")
                b = b.apply_remove(*rem)
            if len(promotions) > 0:
                prom = random.choice(promotions)
                print(f" Promotion {prom}")
                b = b.apply_promotion(*prom)

            b.print_state()

        b = b.next_turn()

        print("----------------------")
        turn += 1


if __name__ == "__main__":
    main()
