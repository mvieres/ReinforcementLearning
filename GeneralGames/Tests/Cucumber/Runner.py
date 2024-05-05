from behave.__main__ import main as behave_main


def run_tests():
    behave_main("setStartingPosition.feature")


if __name__ == '__main__':
    run_tests()
