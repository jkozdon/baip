from baip import Baip
import random


def main():
    b = Baip()
    b.print_state()

    while b.pieces[0].Kit > 0 and b.pieces[1].Kit > 0:
        print()
        placements = b.get_legal_placements()
        b = b.apply_placement(random.choice(placements))
        b.print_state()


if __name__ == "__main__":
    main()
