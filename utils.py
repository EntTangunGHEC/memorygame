import requests
import pygame
import io
import os
import random

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def fetch_star_wars_characters():
    """스타워즈 캐릭터 정보를 API에서 가져옵니다."""
    try:
        response = requests.get("https://akabab.github.io/starwars-api/api/all.json")
        if response.status_code == 200:
            characters = response.json()
            # 필요한 데이터만 처리해서 반환
            return [
                {
                    "id": char.get("id", i),
                    "name": char.get("name", f"Character {i}"),
                    "image": char.get("image", "")
                }
                for i, char in enumerate(characters)
            ]
        else:
            print(f"데이터 가져오기 오류: {response.status_code}")
            return get_fallback_characters()
    except Exception as e:
        print(f"데이터 가져오기 예외 발생: {e}")
        return get_fallback_characters()

def get_fallback_characters():
    """API 요청 실패 시 기본 캐릭터 정보를 제공합니다."""
    return [
        {"id": 1, "name": "Luke Skywalker", "image": "https://starwars-visualguide.com/assets/img/characters/1.jpg"},
        {"id": 2, "name": "Darth Vader", "image": "https://starwars-visualguide.com/assets/img/characters/4.jpg"},
        {"id": 3, "name": "Leia Organa", "image": "https://starwars-visualguide.com/assets/img/characters/5.jpg"},
        {"id": 4, "name": "Han Solo", "image": "https://starwars-visualguide.com/assets/img/characters/14.jpg"},
        {"id": 5, "name": "Chewbacca", "image": "https://starwars-visualguide.com/assets/img/characters/13.jpg"},
        {"id": 6, "name": "R2-D2", "image": "https://starwars-visualguide.com/assets/img/characters/3.jpg"},
        {"id": 7, "name": "C-3PO", "image": "https://starwars-visualguide.com/assets/img/characters/2.jpg"},
        {"id": 8, "name": "Obi-Wan", "image": "https://starwars-visualguide.com/assets/img/characters/10.jpg"},
        {"id": 9, "name": "Yoda", "image": "https://starwars-visualguide.com/assets/img/characters/20.jpg"},
        {"id": 10, "name": "Palpatine", "image": "https://starwars-visualguide.com/assets/img/characters/21.jpg"},
        {"id": 11, "name": "Boba Fett", "image": "https://starwars-visualguide.com/assets/img/characters/22.jpg"},
        {"id": 12, "name": "Lando", "image": "https://starwars-visualguide.com/assets/img/characters/25.jpg"},
        {"id": 13, "name": "Anakin", "image": "https://starwars-visualguide.com/assets/img/characters/11.jpg"},
        {"id": 14, "name": "Padmé", "image": "https://starwars-visualguide.com/assets/img/characters/35.jpg"},
        {"id": 15, "name": "Mace Windu", "image": "https://starwars-visualguide.com/assets/img/characters/51.jpg"},
        {"id": 16, "name": "Qui-Gon Jinn", "image": "https://starwars-visualguide.com/assets/img/characters/32.jpg"},
        {"id": 17, "name": "Count Dooku", "image": "https://starwars-visualguide.com/assets/img/characters/67.jpg"},
        {"id": 18, "name": "General Grievous", "image": "https://starwars-visualguide.com/assets/img/characters/79.jpg"}
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