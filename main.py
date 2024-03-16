from db import database


def main():
    db = database()
    db.get_leaderboard('johndoe')

    # d = db.get_leaderboard('johndoe', 1)
    # print(d)
    # db.get_min_score('johndoe')
    # health_data = db.get_health_data(1)
    # interest_data = db.get_interests(1)

    # ranked = recommend(health_data, interest_data, db.activity_weights)

    # print(ranked)


if __name__ == "__main__":
    main()
