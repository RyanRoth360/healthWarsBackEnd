from db import database


def recommend(health_data, interest_data, weights):

    # 0 = step
    # 1 = screen
    # 2 = sleep

    weakest_score = 100

    # Do something with the min_value

    for key, value in health_data[0].items():
        new_val = 100
        if key == "steps":
            new_val = value / 10000

        if key == "sleep":
            new_val = value / 8

        if key == "screen_time":
            new_val = (value / 24) - 1

        if new_val < weakest_score:
            weakest_key = key
            weakest_score = new_val

    print(weakest_key, " is the weakest link!", weakest_score)
    if weakest_key == "steps":
        index = 0
    if weakest_key == "screen_time":
        index = 1
    if weakest_key == "sleep":
        index = 2

    # Based on weakest link recommend the highest weight for that category
    # Create a set of interests with a value of 1
    interests_set = set()
    for interest, val in interest_data[0].items():
        if val == 1 and interest != "user_id":
            interests_set.add(interest)

    # Now use the wieghts of each activity and calculate which would be best
    best_score = 0

    temp_score = {}
    for interest in interests_set:
        temp_score[interest] = weights[interest][index]
    best_interest = max(temp_score, key=temp_score.get)
    print("Best interest:", best_interest)
    sorted(temp_score, key=lambda item: (item[0]), reverse=True)

    return temp_score


def main():
    db = database()
    db.check_login('johndoe1', 'password123')

    # db.get_leaderboard('johndoe', 1)

    # health_data = db.get_health_data(1)
    # interest_data = db.get_interests(1)

    # ranked = recommend(health_data, interest_data, db.activity_weights)

    # print(ranked)


if __name__ == "__main__":
    main()
