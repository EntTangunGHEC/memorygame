import pygame
import sys
from game import MemoryGame

def main():
    # 초기화
    pygame.init()
    pygame.display.set_caption("Pokemon Memory Game")  # 게임 제목 변경
    
    # 게임 인스턴스 생성
    game = MemoryGame(grid_size=6)
    game.run()
    
    # 종료
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()