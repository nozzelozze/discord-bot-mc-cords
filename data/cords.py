from json import load, dump

PATH = "data/cords.json"

def get():
    with open(PATH, "r") as file:
        cords = load(file)
    return cords

def add_cord(guild_id, user_id, x, y, z, info):
    add_cord = {"x": x, "y": y, "z": z, "info": info}
    with open(PATH, "r") as file:
        cords = load(file)
    user_id = str(user_id)
    guild_id = str(guild_id)
    if user_id in cords[guild_id]:
        cords[guild_id][user_id].append(add_cord)
    else: 
        cords[guild_id][user_id] = [add_cord]
    with open(PATH, "w") as file:
        dump(cords, file)

def remove(guild_id, user_id, info):
    with open(PATH, "r") as file:
        cords = load(file)
    user_id = str(user_id)
    guild_id = str(guild_id)
    copy = next(cord for cord in cords[guild_id][user_id] if cord["info"] == info)
    cords[guild_id][user_id] = list(filter(lambda cord: cord["info"] != info, cords[guild_id][user_id]))
    if cords[guild_id][user_id] == []:
        del cords[guild_id][user_id]
    with open(PATH, "w") as file:
        dump(cords, file)
    return copy

def add_server(guild_id):
    with open(PATH, "r") as file:
        cords = load(file)
    guild_id = str(guild_id)
    cords[guild_id] = {}
    with open(PATH, "w") as file:
        dump(cords, file)