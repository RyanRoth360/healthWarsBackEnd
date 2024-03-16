from db import database


def main():
    db = database()
    # x = db.get_userid('Helo123')
    x = db.select('users', ['user_id', 'password'], {'user_name': 'Testing6969'})
    print(x[0])
    # d = db.get_leaderboard('johndoe', 1)
    # print(d)
    # db.get_min_score('johndoe')
    # health_data = db.get_health_data(1)
    # interest_data = db.get_interests(1)

    # ranked = recommend(health_data, interest_data, db.activity_weights)

    # print(ranked)


if __name__ == "__main__":
    main()
