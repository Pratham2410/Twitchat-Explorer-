from pymongo import MongoClient
from datetime import datetime


def search_tweets(keywords: tuple, db: str, port: int):
    # Connecting to MongoDB
    client = MongoClient('localhost', port)
    db = client[db]
    collection = db['tweets']

    # Matching tweets containing all keywords as separate words
    query = {'$and': [{'content': {'$regex': f'\\b{keyword}\\b', '$options': 'i'}}
                      for keyword in keywords
                      ]}

    results = collection.find(query)
    results = list(results)

    return results


def search_users(keyword: str, db: str, port: int):
    # Connect to MongoDB
    client = MongoClient('localhost', port)
    db = client[db]
    collection = db['tweets']

    # Create a query that matches users whose displayname or location contains the keyword
    query = {'$or': [{'user.displayname': {'$regex': '\\b' + keyword + '\\b', '$options': 'i'}},
                     {'user.location': {'$regex': '\\b' + keyword + '\\b', '$options': 'i'}}]}

    # Execute the query
    results = collection.find(query)

    # Creating a list of users
    userList = []
    for tweet in results:
        user = tweet['user']
        # Checking if the user is already in the list
        if not any(u['username'] == user['username'] for u in userList):
            # Adding the user to the list
            userList.append(user)

    return userList


def top_tweets(n: int, count: str, db: str, port: int):
    # Connecting to MongoDB
    client = MongoClient('localhost', port)
    db = client[db]
    collection = db['tweets']

    # Retrieving the top n tweets based on the specified field
    if count == "r":
        query = collection.find().sort([('retweetCount', -1)]).limit(n)
    elif count == "l":
        query = collection.find().sort([('likeCount', -1)]).limit(n)
    else:
        query = collection.find().sort([('quoteCount', -1)]).limit(n)

    query = list(query)
    return query


def top_users(n: int, db: str, port: int):
    # Connect to MongoDB
    client = MongoClient('localhost', port)
    db = client[db]
    collection = db['tweets']
    collection2 = db['tweets']

    # Aggregating tweets based on username and get the maximum followersCount for each user
    ag_pipeline = [
        {'$group': {
            '_id': '$user.id',
            'user': {'$first': '$user'}
        }},
        {'$sort': {'user.followersCount': -1}},
        {'$limit': n}
    ]

    # Execute the aggregation pipeline
    results = collection.aggregate(ag_pipeline)

    users = [user['user'] for user in results]

    # Get all fields for these users
    complete_users = [
        collection2.find_one({'user.id': user['id'], 'user.followersCount': user['followersCount']})['user'] for user in
        users]

    return complete_users


def compose_tweet(content: str, db: str, port: int):
    # Connect to MongoDB
    client = MongoClient('localhost', port)
    db = client[db]
    collection = db['tweets']

    # Create a new tweet
    tweet = {
        'content': content,
        'date': datetime.now(),
        'user': {
            'username': '291user',
            # Setting the other fields to null
            'displayname': None,
            'id': None,
            'description': None,
            'followersCount': None,
            'friendsCount': None,
            'statusesCount': None,
            'favouritesCount': None,
            'listedCount': None,
            'mediaCount': None,
            'location': None,
            'protected': None,
            'linkUrl': None,
            'linkTcourl': None,
            'profileImageUrl': None,
            'profileBannerUrl': None,
            'url': None
        },
        # Setting the other fields to null
        'url': None,
        'renderedContent': None,
        'replyCount': None,
        'retweetCount': None,
        'likeCount': None,
        'quoteCount': None,
        'conversationId': None,
        'lang': None,
        'source': None,
        'sourceUrl': None,
        'sourceLabel': None,
        'media': None,
        'retweetedTweet': None,
        'quotedTweet': None,
        'mentionedUsers': None
    }

    # Inserting the tweet into the database
    collection.insert_one(tweet)
