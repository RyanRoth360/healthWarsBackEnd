from db import database


def main():
    db = database()
    x = db.get_recomendations('johndoe')
    print(x)


if __name__ == "__main__":
    main()
