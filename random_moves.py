import baip
import random


def main():
    state = baip.initial_state()
    baip.print_state(state)

    while not baip.is_terminal(state):
        actions = baip.get_legal_actions(state)
        action = random.choice(actions)
        state = baip.apply_action(state, action)

    return baip.get_result(state)


if __name__ == "__main__":
    main()
