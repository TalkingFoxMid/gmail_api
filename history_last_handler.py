def read_history_last():
    with open("history_last.log", "r") as f:
        return str(f.read())


def write_history_last(history):
    with open("history_last.log", "w") as f:
        f.write(f'{history}')