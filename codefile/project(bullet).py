import pygame
import random
import threading
import time
import sys
import math
pygame.init()

BLACK= (  0,   0,  0)
WHITE= (255, 255,255)
BLUE = (  0,   0,255)
GREEN= (  0, 255,  0)
RED  = (255,   0,  0)

size  = [400,300] # 화면 크기
screen= pygame.display.set_mode(size) # 화면 생성
pygame.display.set_caption("총알 피하기 게임") # 제목

done= False # 무한 루프를 사용하기 위한 변수
clock= pygame.time.Clock() # 화면 표시를 사용하기위한 객체 생성
playerImg = pygame.image.load('player.png') # 플레이어 이미지 로드
bulletImg = pygame.image.load('bullet.png') # 총알 이미지 로드

def scorescreen(score):
    # 점수를 받아서 점수화면 출력
    fontObj4 = pygame.font.Font('NanumSquareR.ttf', 32)                
    textSurfaceObj4 = fontObj4.render('점수 :'+str(math.floor(score)), True, BLACK)   
    textRectObj4 = textSurfaceObj4.get_rect();                      
    textRectObj4.center = (200, 118)                               

    fontObj5 = pygame.font.Font('NanumSquareR.ttf', 32)                
    textSurfaceObj5 = fontObj5.render('게임종료 ESC', True, BLACK)   
    textRectObj5 = textSurfaceObj5.get_rect();                      
    textRectObj5.center = (200, 150)

    screen.fill(WHITE)
    screen.blit(textSurfaceObj4, textRectObj4)
    screen.blit(textSurfaceObj5, textRectObj5)

class Player():
    # 사용자 클래스 정의
    x = 0
    y = 0
    width = 20
    height = 30
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.life = 1
    def update(self, move):
        # 위치이동
        self.x += move
        if self.x < -20 :
            self.x = -20
        if self.x > 360 :
            self.x = 360
        screen.blit(playerImg,(self.x,self.y))
    def rectangle(self):
        # 객체의 충돌을 위한 충돌인식 상자 추가
        return pygame.Rect(self.x,self.y, self.width, self.height)
    def crash(self):
        # 총알과의 충돌 시 생명 감소
        self.life -= 1
        screen.fill(WHITE)
        screen.blit(playerImg,(self.x,self.y))
    def getplayerlife(self):
        # 생명 값 확인 get 메서드
        return self.life

class bullet():
    # 총알 클래스 정의
    x=0
    y=0
    width = 10
    height = 15
    over_limit = False
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def update(self,move):
        # 총알 위치 이동
        self.y += move
        screen.blit(bulletImg,(self.x,self.y))
    def rectangle(self):
        # 충돌 인식을 위한 충돌인식 상자 추가
        return pygame.Rect(self.x, self.y, self.width, self.height)

def bulletplus():
    # 총알 추가 함수
    bullet_list.append(bullet(6*random.randint(0,65)+1,0))
    
def bulletdowm():
    # 총알 낙하 함수
    for bullets in bullet_list:
        bullets.update(10)
        if bullets.rectangle().colliderect(playerlist[0].rectangle()):
            playerlist[0].crash()
    


bullet_list = [] # 총알을 하나씩 낙하시키기위해서 리스트사용
# 시작화면
fontObj1 = pygame.font.Font('NanumSquareR.ttf', 32) # 글씨(font)가져오기       
textSurfaceObj1 = fontObj1.render('게임을 시작하려면', True, BLACK)   # 글 내용 정의
textRectObj1 = textSurfaceObj1.get_rect(); # 글 내용 박스에 담기
textRectObj1.center = (200, 118) # 박스 위치                               

fontObj2 = pygame.font.Font('NanumSquareR.ttf', 32)                
textSurfaceObj2 = fontObj2.render('SPACE버튼을 눌러주세요.', True, BLACK)   
textRectObj2 = textSurfaceObj2.get_rect();                      
textRectObj2.center = (200, 150)

screen.fill(WHITE) # 화면 흰색으로 초기화
screen.blit(textSurfaceObj1, textRectObj1) # 박스에 담긴 글씨와 글 내용과 함께 화면에 출력 
screen.blit(textSurfaceObj2, textRectObj2)

playerlist = [] # 사용자 객체를 담기위한 리스트
playerlist.append(Player(190,270)) # 객체 리스트에 추가
start = 0

while not done:
    clock.tick(10) # 화면표시 프레임을 10으로 설정
    for event in pygame.event.get(): # 이벤트 발생시의 모든 이벤트를 수집
        if event.type == pygame.QUIT: # 창의 x버튼 클릭시 수행하여 게임 종료
            done = True
        if event.type== pygame.KEYDOWN: # 키를 눌렀을때의 이벤트 종류
            if event.key==pygame.K_SPACE: # SPACE 버튼을 눌렀을시 게임시작. 조건문 실행
                screen.fill(WHITE) 
                playerlist.append(Player(190,270))
                playerlist[0].update(0) # 플레이어 위치 중간으로 생성
                start = 1 # 게임 시작했을때만 총알 생성을 위한 변수
                t = time.time() # 시간에 따른 점수를 주기위한것으로 게임 시작시 시간을 변수에 할당 
            if event.key==pygame.K_RIGHT: # 오른쪽 화살표 자판을 눌렀을 시 플레이어 오른쪽으로 이동
                try : 
                    playerlist[0].update(10)
                except NameError:
                    continue
            if event.key==pygame.K_LEFT: # 왼쪽 화살표 자판을 눌렀을 시 플레이어 왼쪽으로 이동
                try:
                    playerlist[0].update(-10)
                except NameError:
                    continue
            if event.key == pygame.K_ESCAPE: # ESC버튼 눌렀을 시 게임 종료
                done = True
    if start :
        # 게임 시작시 총알 생성과 하락
        threading.Timer(5,bulletplus).start() # 총알을 5초후부터 생성하는 것을 수행
        threading.Timer(1,bulletdowm).start() # 총알을 1초마다 낙하시킴
    
    if playerlist[0].getplayerlife() == 0: # 충돌하여 목숨이 없어졌을 때 수행
        finish_time = time.time() # 게임이 끝난 시간
        score = finish_time - t # 게임시작과 게임 종료시의 차이만큼의 시간을 점수로 취급
        playerlist.pop(0) # 죽은 플레이어를 리스트에서 제거
        start = 0 # 총알 생성을 막기위해서 0으로 변환
        time.sleep(3) # 잠시 멈추기위해서 사용
        scorescreen(score) # 점수를 받아서 점수화면 출력
        playerlist.append(Player(190,270)) # 다시 플레이어 객체 추가
    
    pygame.display.flip()
