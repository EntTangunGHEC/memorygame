import requests
import random
import time
import os
import pygame
import io  # io 모듈 추가

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