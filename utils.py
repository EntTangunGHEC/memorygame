import requests
import random
import time
import os
import pygame

def fetch_pokemon_characters():
    """포켓몬 정보를 API에서 가져옵니다."""
    try:
        # 포켓몬 수 (151 = 1세대 포켓몬)
        total_pokemon = 151
        pokemons = []
        
        # 각 포켓몬에 대한 정보 가져오기
        for i in range(1, total_pokemon + 1):
            response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{i}")
            if response.status_code == 200:
                data = response.json()
                pokemon = {
                    "id": data["id"],
                    "name": data["name"].capitalize(),
                    "image": data["sprites"]["other"]["official-artwork"]["front_default"]
                }
                pokemons.append(pokemon)
            else:
                print(f"포켓몬 {i} 데이터 가져오기 오류: {response.status_code}")
        
        if len(pokemons) < 18:  # 최소 18개 필요 (6x6 그리드)
            print("API에서 충분한 포켓몬을 가져오지 못했습니다. 대체 데이터를 사용합니다.")
            return get_fallback_pokemon()
            
        return pokemons
    except Exception as e:
        print(f"데이터 가져오기 예외 발생: {e}")
        return get_fallback_pokemon()

def get_fallback_pokemon():
    """API 요청 실패 시 기본 포켓몬 정보를 제공합니다."""
    return [
        {"id": 1, "name": "Bulbasaur", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/1.png"},
        {"id": 4, "name": "Charmander", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/4.png"},
        {"id": 7, "name": "Squirtle", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/7.png"},
        {"id": 25, "name": "Pikachu", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/25.png"},
        {"id": 39, "name": "Jigglypuff", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/39.png"},
        {"id": 54, "name": "Psyduck", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/54.png"},
        {"id": 94, "name": "Gengar", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/94.png"},
        {"id": 129, "name": "Magikarp", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/129.png"},
        {"id": 132, "name": "Ditto", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/132.png"},
        {"id": 143, "name": "Snorlax", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/143.png"},
        {"id": 150, "name": "Mewtwo", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/150.png"},
        {"id": 151, "name": "Mew", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/151.png"},
        {"id": 133, "name": "Eevee", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/133.png"},
        {"id": 12, "name": "Butterfree", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/12.png"},
        {"id": 16, "name": "Pidgey", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/16.png"},
        {"id": 92, "name": "Gastly", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/92.png"},
        {"id": 104, "name": "Cubone", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/104.png"},
        {"id": 124, "name": "Jynx", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/124.png"}
    ]

def load_image(url):
    """URL에서 이미지를 로드하고 적절한 크기로 조정합니다."""
    try:
        if not url:
            # 기본 이미지 반환
            surf = pygame.Surface((90, 105))
            surf.fill((200, 200, 200))
            return surf
            
        response = requests.get(url)
        if response.status_code == 200:
            image_data = io.BytesIO(response.content)
            image = pygame.image.load(image_data)
            # 카드 크기에 맞게 이미지 크기 조정
            return pygame.transform.scale(image, (90, 105))
        else:
            # 이미지 로드 실패 시 기본 이미지 반환
            surf = pygame.Surface((90, 105))
            surf.fill((200, 200, 200))
            return surf
    except Exception as e:
        print(f"이미지 로드 오류: {e}")
        # 오류 발생 시 기본 이미지 반환
        surf = pygame.Surface((90, 105))
        surf.fill((200, 200, 200))
        return surf