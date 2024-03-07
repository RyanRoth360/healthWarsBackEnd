from db import database


def recommend(health_data, interest_data):

    step_set = set()
    sleep_set = set()
    screen_set = set()

    # Check which interests are viable

    # Check minimum of the data points
    print(health_data)
    print(interest_data)
    # Do something with the min_value

    # Recommend interests that fulfill the data point


def main():
    db = database()

    health_data = db.get_health_data(1)
    interest_data = db.get_interests(1)

    recommend(health_data, interest_data)


if __name__ == "__main__":
    main()
