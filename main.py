from db import database


def main():
    db = database()
    # db.insert_health_data(2, 2342, 2, 6.3)
    # db.insert_health_data(3, 5893, 5.4, 10.2)
    # db.insert_health_data(4, 7386, 9.1, 8)

    db.get_leaderboard('johndoe', 1)


if __name__ == '__main__':
    main()
