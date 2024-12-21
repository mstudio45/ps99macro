import datetime

def Timer(table: list):
    start_time = datetime.datetime.now()
    try:
        yield
    finally:
        table.append(datetime.datetime.now() - start_time)