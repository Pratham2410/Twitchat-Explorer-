import sys
import functions
import load_json


def main_menu():
    print("Welcome to your twitchat homepage! What would you like to do?: ")
    print("1. Search tweets")
    print("2. Search users")
    print("3. List top tweets")
    print("4. List most followed users")
    print("5. Compose a tweet")
    print("6. Exit")

    while True:
        option = input("> ")
        if option.isdigit() and 1 <= int(option) <= 6:
            break
        else:
            print("Invalid option selected! Please enter a number between 1 and 6.")
    return int(option)


def correct_input(usr_input: str, a: int, b: int):
    uinput = 0
    if usr_input.isdigit():
        uinput = int(usr_input)
    else:
        return 0

    if (a <= uinput <= b) or uinput == 0:
        return 1
    return 0


def display_tweets(keywords: tuple, db: str, port: int):
    tweets = functions.search_tweets(keywords, db, port)
    tweets = list(tweets)
    i = 0
    for tweet in tweets:
        i += 1
        tweet_id = tweet.get('id')
        tweet_date = tweet.get('date')
        tweet_username = tweet.get('user', {}).get('username')
        tweet_content = tweet.get('content')

        if tweet_id is not None:
            print(
                f'{i}. ID: {tweet_id}, Date: {tweet_date}, Username: {tweet_username}\nTweet Content: {tweet_content}')
        else:
            print(f'{i}. ID: NULL, Date: {tweet_date}, Username: {tweet_username}\nTweet Content: {tweet_content}')

    # If there is at least one tweet that matches the keywords, give the user the option to select one
    if i != 0:
        answer = input("Select a tweet to see more info about it or enter 0 to return to main menu: ")
        while correct_input(answer, 1, i) != 1:
            answer = input(f"Please enter a number between 0 and {i}: ")

        answer = int(answer)
        # Print all fields
        if answer != 0:
            j = 1
            for tweet in tweets:
                if answer == j:
                    for key, value in tweet.items():
                        print(f"{key}: {value}")
                    print(" ")
                    return
                j += 1
    else:
        print("No such tweets")
    return


def display_users(keyword: str, db: str, port: int):
    users = functions.search_users(keyword, db, port)
    users = list(users)
    i = 0
    for user in users:
        i += 1
        print(f'{i}. Username: {user["username"]}, Display name: {user["displayname"]}, Location: {user["location"]}')

    # If there is at least one user that matches the keyword, give the option to select them
    if i != 0:
        answer = input("Select a user to see more info on them or enter 0 to return to main menu: ")
        while correct_input(answer, 1, i) != 1:
            answer = input(f"Please enter a number between 0 and {i}: ")

        answer = int(answer)
        # Print all fields
        if answer != 0:
            for j, user in enumerate(users, start=1):
                if answer == j:
                    for key, value in user.items():
                        print(f"{key}: {value}")
                    print(" ")
                    return
    else:
        print("No such user")

    return


def display_top_tweets(n: int, count: str, db: str, port: int):
    tweets = functions.top_tweets(n, count, db, port)
    i = 0
    for tweet in tweets:
        i += 1
        print(
            f'{i}. ID: {tweet["id"]}, Date: {tweet["date"]}, Username: {tweet["user"]["username"]}\nTweet Content: {tweet["content"]}')

    if i != 0:
        answer = input("Select a tweet to see more info or enter 0 to go back to the main screen: ")
        while (correct_input(answer, 1, i) != 1):
            print("Invalid input")
            answer = input("Select a tweet to see more info or enter 0 to go back to the main screen: ")

        answer = int(answer)
        # Print all fields
        if answer != 0:
            for j, tweet in enumerate(tweets, start=1):
                if answer == j:
                    for key, value in tweet.items():
                        print(f"{key}: {value}")
                    print(" ")
                    return
    else:
        print("No such tweets")

    return


def display_top_users(n: int, db: str, port: int):
    users = functions.top_users(n, db, port)
    users = list(users)
    if len(users) == 0:
        print("No such users")
        return

    i = 1
    for user in users:
        print(
            f'{i}. Username: {user["username"]}, Display name: {user["displayname"]}, Followers Count: {user["followersCount"]}')
        i += 1
    answer = input("Select a user to see more info or enter 0 to go back to the main screen: ")
    while (correct_input(answer, 1, i) != 1):
        print("Invalid input")
        answer = input("Select a user to see more info or enter 0 to go back to the main screen: ")

    answer = int(answer)
    # Print all fields
    if answer != 0:
        for j, user in enumerate(users, start=1):
            if answer == j:
                for key, value in user.items():
                    print(f"{key}: {value}")
                print(" ")
                return

    return


def main():
    port = int(sys.argv[1])
    db = "291db"
    command = main_menu()
    while (command):
        if command == 1:
            keywords = input("Enter keywords to search for in tweets: ")
            # Check that the input is not whitespace or empty
            while not any(char.isalpha() or char.isdigit() for char in keywords):
                keywords = input("Enter keywords to search for in tweets: ")
            keywords = keywords.split(" ")

            # Display the tweets that match at least one of the keywords
            display_tweets(tuple(keywords), db, port)
        elif command == 2:
            keyword = input("Enter a keyword to search for in users: ")
            # Check that the input is not empty or whitespaces
            while not any(char.isalpha() or char.isdigit() for char in keyword):
                keyword = input("Enter a keyword to search for in users: ")

            # Display users that match the key word
            display_users(keyword, db, port)
        elif command == 3:
            n = input("Enter the Top 'n' tweets you wish to see: ")
            # Check that the input is not whitespace or empty
            while not n.isdigit() and int(n) < 1:
                n = input("Enter the Top 'n' tweets you wish to see: ")
            n = int(n)

            print(f"Do you wish to see the top {n} tweets based on retweetCount, likeCount, or quoteCount?")
            count = input("Enter r, l, or q for retweet, like, or quote counts respectively: ")
            while count.lower() not in ["r", "l", "q"]:
                count = input("Enter r, l, or q for retweet, like, or quote counts respectively: ")

            # Display the tweets that match at least one of the keywords
            display_top_tweets(n, count, db, port)
        elif command == 4:
            n = input("Enter the Top 'n' users you wish to see: ")
            # Check that the input is not whitespace or empty
            while not n.isdigit() and int(n) < 1:
                n = input("Enter the Top 'n' users you wish to see: ")
            n = int(n)

            display_top_users(n, db, port)
        elif command == 5:
            text = input("Please enter the text of your tweet: ")
            try:
                functions.compose_tweet(text, db, port)
                print("You've posted a tweet.\n")
            except:
                print("Something went wrong while adding tweet to db")
        else:
            break
        command = main_menu()
    print("Exiting...\n")
    return 0


if __name__ == "__main__":
    main()
