import requests, json
from django.shortcuts import render, HttpResponse

def index(request, user):
    url = "https://www.instagram.com/" + user + "?__a=1"
    response = requests.get(url)
    if response.status_code != 200: return HttpResponse('{"error":"Invalid query"}')
    data = json.loads(response.text)
    items = data["graphql"]
    user_data = items["user"]
    #followers
    followed = user_data["edge_followed_by"]["count"]
    #follows
    follows = user_data["edge_follow"]["count"]
    #num. piosts
    media = user_data["edge_owner_to_timeline_media"]
    media_count = media["count"]
    #private
    private = user_data["is_private"]
    #bio
    bio = user_data["biography"]
    #avg likes / 6
    if not private: engagement = getLikes(media["edges"], followed)
    else: engagement = "-"
    instagram_data = {
        "followers" : followed,
        "follows" : follows,
        "bio" : bio,
        "posts" : media_count,
        "private" : private,
        "engagement" : engagement
    }
    return HttpResponse(json.dumps(instagram_data))

def getLikes(pictures, followers):
    likes = 0
    c = 0
    for picture in pictures:
        if c == 6: break
        print(picture)
        likes += picture["node"]["edge_liked_by"]["count"]
        c+=1
    if c > 0: return likes / c / followers
    return c
