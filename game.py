import pygame
import random
import time
import sys
import io  # io 모듈 추가
from card import Card
from utils import fetch_pokemon_characters, load_image  # 함수 이름 변경

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 100, 255)
GREEN = (50, 200, 50)

class MemoryGame:
    def __init__(self, grid_size=6):
        self.grid_size = grid_size
        self.cards = []
        self.board = []
        self.pairs_found = 0
        self.total_pairs = (grid_size * grid_size) // 2
        self.moves = 0
        self.first_card = None
        self.second_card = None
        self.waiting = False
        self.wait_time = 0
        self.game_over = False
        
        # 화면 설정
        self.card_width = 100
        self.card_height = 140
        self.margin = 10
        self.screen_width = self.grid_size * (self.card_width + self.margin) + self.margin
        self.screen_height = self.grid_size * (self.card_height + self.margin) + self.margin + 60  # 상단 상태 표시줄 공간
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        
        # 폰트 설정
        pygame.font.init()
        self.font = pygame.font.SysFont('Arial', 24)
        self.small_font = pygame.font.SysFont('Arial', 16)
        
        # 게임 시계 설정
        self.clock = pygame.time.Clock()
        
        # 게임 초기화
        self.setup_game()
    
    def setup_game(self):
        # 포켓몬 데이터 가져오기
        characters = fetch_pokemon_characters()
        
        # 필요한 캐릭터 수 계산
        needed_characters = (self.grid_size * self.grid_size) // 2
        
        # 캐릭터 충분한지 확인
        if len(characters) < needed_characters:
            print(f"캐릭터가 부족합니다. 더 작은 그리드를 사용합니다.")
            self.grid_size = min(4, int((len(characters) * 2) ** 0.5))
            needed_characters = (self.grid_size * self.grid_size) // 2
            
            # 화면 크기 재조정
            self.screen_width = self.grid_size * (self.card_width + self.margin) + self.margin
            self.screen_height = self.grid_size * (self.card_height + self.margin) + self.margin + 60
            self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        
        # 필요한 캐릭터만 선택
        selected_characters = random.sample(characters, needed_characters)
        
        # 각 캐릭터에 대해 카드 2장씩 생성 (짝)
        card_pairs = []
        for char in selected_characters:
            # 캐릭터 이미지 로드
            image_url = char.get("image", "")
            
            # 두 장의 카드 생성 (같은 ID로)
            card1 = Card(char["id"], char["name"], image_url)
            card2 = Card(char["id"], char["name"], image_url)
            card_pairs.extend([card1, card2])
        
        # 카드 섞기
        random.shuffle(card_pairs)
        
        # 2D 보드에 카드 배치
        self.board = []
        for i in range(self.grid_size):
            row = []
            for j in range(self.grid_size):
                if card_pairs:
                    row.append(card_pairs.pop(0))
            self.board.append(row)
    
    def display_board(self):
        self.screen.fill(WHITE)
        
        # 카드 그리기
        for i, row in enumerate(self.board):
            for j, card in enumerate(row):
                x = self.margin + j * (self.card_width + self.margin)
                y = self.margin + i * (self.card_height + self.margin)
                self.draw_card(card, x, y)
        
        # 상태 표시줄 그리기
        status_text = f"Pairs Found: {self.pairs_found}/{self.total_pairs} - Moves: {self.moves}"
        status_surface = self.font.render(status_text, True, BLACK)
        self.screen.blit(status_surface, (self.margin, self.screen_height - 50))
        
        pygame.display.flip()
    
    def draw_card(self, card, x, y):
        # 카드 배경 그리기
        card_rect = pygame.Rect(x, y, self.card_width, self.card_height)
        
        if card.is_matched:
            # 매치된 카드 - 초록색 배경
            pygame.draw.rect(self.screen, GREEN, card_rect)
            pygame.draw.rect(self.screen, BLACK, card_rect, 2)  # 테두리
            
            # 이미지 표시
            if card.image:
                self.screen.blit(card.image, (x + 5, y + 5))
            
            # 이름 표시
            name_surf = self.small_font.render(card.name[:12], True, BLACK)
            self.screen.blit(name_surf, (x + 5, y + self.card_height - 25))
        
        elif card.is_flipped:
            # 뒤집힌 카드 - 파란색 배경
            pygame.draw.rect(self.screen, BLUE, card_rect)
            pygame.draw.rect(self.screen, BLACK, card_rect, 2)  # 테두리
            
            # 이미지 표시
            if card.image:
                self.screen.blit(card.image, (x + 5, y + 5))
            
            # 이름 표시
            name_surf = self.small_font.render(card.name[:12], True, BLACK)
            self.screen.blit(name_surf, (x + 5, y + self.card_height - 25))
        
        else:
            # 뒤집히지 않은 카드 - 회색 배경
            pygame.draw.rect(self.screen, GRAY, card_rect)
            pygame.draw.rect(self.screen, BLACK, card_rect, 2)  # 테두리
            
            # 카드 뒷면 표시
            back_text = self.font.render("PK", True, BLACK)  # "SW"에서 "PK"로 변경
            text_rect = back_text.get_rect(center=(x + self.card_width//2, y + self.card_height//2))
            self.screen.blit(back_text, text_rect)
    
    def get_card_position(self, pos):
        x, y = pos
        for i, row in enumerate(self.board):
            for j, card in enumerate(row):
                card_x = self.margin + j * (self.card_width + self.margin)
                card_y = self.margin + i * (self.card_height + self.margin)
                if card_x <= x <= card_x + self.card_width and card_y <= y <= card_y + self.card_height:
                    return i, j
        return None, None
    
    def run(self):
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and not self.waiting:
                    pos = pygame.mouse.get_pos()
                    row, col = self.get_card_position(pos)
                    if row is not None and col is not None:
                        card = self.board[row][col]
                        if not card.is_flipped and not card.is_matched:
                            card.flip()
                            if self.first_card is None:
                                self.first_card = card
                            elif self.second_card is None:
                                self.second_card = card
                                self.moves += 1
                                self.waiting = True
                                self.wait_time = time.time()
            
            if self.waiting and time.time() - self.wait_time > 1:
                if self.first_card == self.second_card:
                    self.first_card.match()
                    self.second_card.match()
                    self.pairs_found += 1
                    if self.pairs_found == self.total_pairs:
                        self.game_over = True
                else:
                    self.first_card.flip()
                    self.second_card.flip()
                self.first_card = None
                self.second_card = None
                self.waiting = False
            
            self.display_board()
            self.clock.tick(30)
        
        # 게임 종료 메시지
        self.display_board()
        game_over_text = f"Congratulations! You've found all {self.total_pairs} pairs in {self.moves} moves!"
        game_over_surface = self.font.render(game_over_text, True, BLACK)
        self.screen.blit(game_over_surface, (self.margin, self.screen_height - 30))
        pygame.display.flip()
        
        # 게임 종료 후 잠시 대기
        waiting_for_exit = True
        while waiting_for_exit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                    waiting_for_exit = False
            self.clock.tick(30)