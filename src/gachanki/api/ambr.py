from dataclasses import dataclass
import json
import urllib3

data_url = "https://gi.yatta.moe/api/v2/en/{}"
image_url = "https://gi.yatta.moe/assets/UI/{}.png"

http = urllib3.PoolManager()

# === General Utility ===
def _request_data(api_endpoint) -> dict:
    response = http.request("GET", data_url.format(api_endpoint))
    response_json = json.loads(response.data.decode("utf-8"))

    return response_json['data']

def sort_by_rarity(items):
    sorted = {
        1: [],
        2: [],
        3: [],
        4: [],
        5: [],
    }

    for value in items.values():
        sorted[value.rarity].append(value)

    return sorted

# === Characters ===
@dataclass
class Character:
    id: str
    name: str
    rarity: int
    icon: str
    gacha: str
    party: str

def get_characters() -> dict:
    response = _request_data("avatar")

    characters = {}

    for id, data in response['items'].items():
        characters[str(id)] = Character(id = str(data['id']),
                                        name = data['name'],
                                        rarity = data['rank'],
                                        icon = image_url.format(data['icon']),
                                        gacha = image_url.format(data['icon']).replace('AvatarIcon', 'Gacha_AvatarImg'),
                                        party = ''
                                        )

    return characters

def get_character_details(id):
    return _request_data("avatar/{}".format(id))

# === Weapons ===
@dataclass
class Weapon:
    id: str
    name: str
    rarity: int
    icon: str

def get_weapons() -> dict:
    response = _request_data("weapon")

    weapons = {}

    for id, data in response['items'].items():
        weapons[id] = Weapon(id = data['id'],
                             name = data['name'],
                             rarity = data['rank'],
                             icon = image_url.format(data['icon']),
                             )

    return weapons

def get_weapon_details(id):
    return _request_data("weapon/{}".format(id))
