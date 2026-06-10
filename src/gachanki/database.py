import json
import urllib3

from .api import ambr

class Database:

    base_url = 'https://gachanki.pockethost.io/'
    token = ''
    profile = {}

    http = urllib3.PoolManager()

    def __init__(self):
        self.account_load()
        
        # Load characters and weapons
        self.characters = ambr.get_characters()
        self.weapons = ambr.get_weapons()

    def is_logged_in(self):
        return self.token != ''

    def account_signup(self, username, password):
        url = self.base_url + '/api/collections/users/records'

        payload = {
            'username': username,
            'password': password,
            'passwordConfirm': password,
            # Initial account defaults to 0
            'gacha_points': 0,
            'lifetime_rolls': 0,
            'pity_4_star': 0,
            'pity_5_star': 0,
        }

        headers = {
            "Content-Type": "application/json"
        }

        response = self.http.request(
            'POST',
            url,
            body=json.dumps(payload),
            headers=headers
        )
        
        if response.status == 200:
            # Pocketbase requires separate auth after creating user
            self.account_login(username, password)
        else:
            response_data = json.loads(response.data.decode('utf-8'))
            print(f"{response.status}: {response_data['message']}.")
            
        return response.status

    def account_login(self, username, password):
        url = self.base_url + '/api/collections/users/auth-with-password'

        payload = {
            "identity": username,
            "password": password,
        }
        headers = {
            "Content-Type": "application/json",
        }

        response = self.http.request(
            'POST',
            url,
            body=json.dumps(payload),
            headers=headers
        )
        
        if response.status == 200:
            response_json = json.loads(response.data.decode('utf-8'))
            self.token = response_json['token']
            self.profile = response_json['record']
            
            self.account_load()
        else:
            response_data = json.loads(response.data.decode('utf-8'))
            print(f"{response.status}: {response_data['message']}")
            
        return response.status

    def account_signout(self):
        self.token = ''
        self.profile = {}
        
        self.gacha_points = 0
        self.lifetime_rolls = 0
        self.pity_4_star = 0
        self.pity_5_star = 0

    def account_load(self):
        if self.is_logged_in():
            self.gacha_points = self.profile['gachaPoints']
            self.lifetime_rolls = self.profile['lifetimeRolls']
            self.pity_4_star = self.profile['pity4Star']
            self.pity_5_star = self.profile['pity5Star']

    def get_owned_characters(self, franchise):
        character_list = []
    
        if self.is_logged_in():
            url = self.base_url + '/api/collections/character_inventory/records'
            http = urllib3.PoolManager()
            
            def fetch_page(page=1):
                querystring = {
                    "filter": f"(user='{self.profile['id']}' && franchise='{franchise}')",
                    "page": page
                }
                response = http.request(
                    'GET',
                    url,
                    fields=querystring
                )
                if response.status == 200:
                    return json.loads(response.data.decode('utf-8'))
                else:
                    print(f"{response.status}: {json.loads(response.data.decode('utf-8'))['message']}.")
                    return None
        
            # Fetch first page
            response_json = fetch_page()
            if response_json:
                character_list.extend(response_json['items'])
                
                # Fetch remaining pages if any
                for page in range(2, response_json['totalPages'] + 1):
                    response_json = fetch_page(page)
                    if response_json:
                        character_list.extend(response_json['items'])
                    else:
                        break
    
        return character_list

    def add_owned_character(self, character, franchise) -> None:
        if self.is_logged_in():
            url = self.base_url + '/api/collections/character_inventory/records'

            payload = {
                "user": self.profile['id'],
                "lookup_id": character.id,
                "franchise": franchise,
                "icon_url": character.icon,
                "quantity": 1,
                "xp": 0,
            }
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": self.token,
            }
            
            response = self.http.request(
                'POST',
                url,
                body=json.dumps(payload),
                headers=headers
            )
            
            if response.status == 200:
                pass  # Operation successful, no further action required

    def save(self):
        if self.is_logged_in():
            url = self.base_url + f"/api/collections/users/records/{self.profile['id']}"

            payload = {
                "gachaPoints": self.gacha_points,
                "lifetimeRolls": self.lifetime_rolls,
                "pity4Star": self.pity_4_star,
                "pity5Star": self.pity_5_star,
            }
            headers = {
                "Content-Type": "application/json",
                "Authorization": self.token,
            }

            response = self.http.request(
                'PATCH',
                url,
                body=json.dumps(payload),
                headers=headers
            )
            
            if response.status == 200:
                pass  # Operation successful

