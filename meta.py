import sys


if __name__ == "__main__":
    with open("baseline_marl/_version.py", mode='w') as f:
        f.write(f'__version__ = "{sys.argv[1]}"\n')

