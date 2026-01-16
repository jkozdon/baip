import baip
import random


def main():
    state = baip.initial_state()
    baip.print_state(state)

    while state.phase != baip.Phase.TERMINAL:
        actions = baip.get_legal_actions(state)
        action = random.choice(actions)
        state = baip.apply_action(state, action)
        print()
        baip.print_state(state)

    if state.active_player == 0:
        print("player A won!")
    else:
        print("player B won!")

    return baip.get_result(state)


if __name__ == "__main__":
    main()
