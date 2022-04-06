import pygame
import random
import sys

## 함수
# @기능 2-5 : 매개변수로 받은 객체를 화면에 그리는 함수를 선언한다.
def paintEntiry(entity, x, y) :
    monitor.blit(entity, (x, y))

# @기능 5-4 : 점수를 화면에 쓰는 함수를 선언한다.
def writeScore(score) :
    myfont = pygame.font.Font('NanumGothic.ttf', 20) #한글 폰트
    txt = myfont.render(u'파괴한 괴물의 수 : ' + str(score), True, (255-r, 255-g, 255-b))
    monitor.blit(txt, (10, sheight - 40))

def playGame() :
    global monitor

    r = random.randrange(0, 256)
    g = random.randrange(0, 256)
    b = random.randrange(0, 256)

    # @기능 2-2 : 우주선의 초기 위치 키보드를 눌렀을 때 이동량을 저장할 변수를 선언한다.
    shipX = (swidth / 2) - 25 # 우주선의 위치
    shipY = sheight * 0.8
    dx, dy = 0, 0 # 키보드를 누를 때, 우주선의 이동량을 측정하기 위한 변수방

    # @기능 3-2 : 우주괴물을 무작위로 추출하고 크기와 위치를 설정한다.
    monster = pygame.image.load(random.choice(monsterImage))
    monsterSize = monster.get_rect().size # 우주괴물 크기
    monsterX = 0
    monsterY = random.randrange(0, int(swidth*0.3)) # 상위 30%까지
    monsterSpeed = random.randrange(1, 5)

    # @기능 4-2 : 미사일 좌표를 초기화한다.
    missileX, missileY = None, None

    # @기능 5-1 : 맞힌 우주괴물 숫자를 저장할 변수를 선언한다.
    fireCount = 0

    # 무한 반복
    while True :
        (pygame.time.Clock()).tick(50) # 게임 진행을 늦춰 줌(10 ~ 100 정도가 적당, 숫자가 클수록 속도 빠름)
        monitor.fill((r, g, b)) # 화면 배경색 칠하기

        # 키보드나 마우스 이벤트가 들어오는 것을 체크하는 코드
        for e in pygame.event.get() :
            if e.type in [pygame.QUIT] : # (상단 오른쪽)<x>버튼을 누르면 종료되는  타입
                pygame.quit() # 게임종료
                sys.exit() # 메모리 소멸

            # @기능 2-3 : 방향키에 따라 우주선이 움직이게 한다.
            if e.type in [pygame.KEYDOWN] :
                if e.key == pygame.K_LEFT : dx = -5
                elif e.key == pygame.K_RIGHT : dx = +5
                elif e.key == pygame.K_UP : dy = -5
                elif e.key == pygame.K_DOWN : dy = +5

            # @기능 4-3 : 스페이스바를 누르면 미사일을 발사한다.
                elif e.key == pygame.K_SPACE :
                    if missileX == None :
                        missileX = shipX + shipSize[0] / 2
                        missileY = shipY

            # 방향키를 떼면 우주선이 안 움직임
            if e.type in [pygame.KEYUP] :
                if e.key == pygame.K_LEFT or e.key == pygame.K_RIGHT or e.key == pygame.K_DOWN or e.key == pygame.K_UP :
                    dx, dy = 0, 0

        # @기능 2-4 : 우주선이 화면 안에서만 움직이게 한다.
        if (0 < shipX + dx and shipX + dx <= swidth - shipSize[0]) \
            and (sheight / 2 < shipY + dy and shipY + dy <= sheight - shipSize[1]) :  # 화면의 중앙까지만
            shipX += dx
            shipY += dy
        paintEntiry(ship, shipX, shipY) # 우주선 이미지를 뿌린다
        # @기능 3-3 : 우주괴물이 자동으로 나타나 왼쪽에서 오른쪽으로 움직인다.
        monsterX += monsterSpeed
        if monsterX > swidth :
            monsterX = 0
            monsterY = random.randrange(0, int(swidth * 0.3))
            # 우주괴물 랜덤하게 선택하여 등장
            monster = pygame.image.load(random.choice(monsterImage))
            monsterSize = monster.get_rect().size # 우주괴물 크기
            monsterSpeed = random.randrange(1, 5)

        paintEntiry(monster, monsterX, monsterY)

        # @기능 4-4 : 미사일을 화면에 표시한다.
        if missileX != None :
            missileY -= 10
            if missileY < 0 :
                missileX, missileY = None, None # 미사일을 쏘지 않은 상태
        if missileX != None :
            paintEntiry(missile, missileX, missileY)

            # @기능 5-2 : 우주괴물이 미사일에 맞았는지 체크한다.
            if (monsterX < missileX and missileX < monsterX + monsterSize[0]) and \
                   (monsterY < missileY and missileY < monsterY + monsterSize[1]) :
                fireCount += 1

                # 우주괴물 초기화
                monster = pygame.image.load(random.choice(monsterImage))
                monsterSize = monster.get_rect().size
                monsterX = 0
                monsterY =random.randrange(0, int(swidth * 0.3))
                monsterSpeed = random.randrange(1, 5)

                # 미사일을 초기화한다.
                missileX, missileY= None, None   # 총알이 사라진다.



        # @기능 5-3 : 점수를 화면에 쓰는 함수를 호출한다.
        writeScore(fireCount)

        # 화면을 업데이트 한다
        pygame.display.update() # 게임 진행 실시간 업데이트 하기
        print("~", end = '') # 게임 진행 확인코

## 전역
r, g, b = [0] * 3 # 게임 배경색 색의 속성 3요소 가상 혼합, 즉(색조, 채도, 명도)
swidth, sheight = 500, 700 # 화면 크기
monitor = None # 게임 화면

# @기능 3-1 : 무작위로 사용 할 우주괴물이 이미지 10개를 준비한다.
monsterImage = ['monster01.png', 'monster02.png', 'monster03.png', 'monster04.png', 'monster05.png', 'monster06.png', 'monster07.png', 'monster08.png', 'monster09.png', 'monster10.png']
monster = None

## 메인
pygame.init()
monitor = pygame.display.set_mode((swidth, sheight))
pygame.display.set_caption('우주괴물 무찌르기')

# @기능 2-1 : 우주선 이미지를 준비하고 크기를 구한다.
ship = pygame.image.load('ship02.png')
shipSize = ship.get_rect().size

# @기능 4-1 : 미사일 이미지를 추가한다.
missile = pygame.image.load('missile.png')

playGame()
