import json, sys


def main():
    event = json.load(sys.stdin)
    with open("events.log", "a") as log:
        log.write(json.dumps(event) + "\n")


if __name__ == "__main__":
    main()
