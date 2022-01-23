import pygame
#import trains.py

pygame.init()

screen = pygame.display.set_mode((649, 451))
pygame.display.set_caption("Please Don't Make Me Wait")

bg = pygame.image.load('background.png')
bg = pygame.transform.scale(bg, (649, 451))

font = pygame.font.Font('Manrope-Bold.ttf', 24)
#nice font

A = (110, 126)
B = (306, 126)
BC = (342, 194)
C = (505, 205)
US = (515, 377)

#function move
def move(origin,destination,current,time):
    (x1, y1) = origin
    (x2, y2) = destination
    (curx, cury) = current
    if curx > x2 or cury > y2:
        return destination
    return (curx + (x2 - x1) / time, cury + (y2 - y1) / time)

#trying to make a beautiful UI
def displayUI():
    clock = font.render('07:00', True, (0, 0, 0))
    traincount = font.render('L4: 4/4   L8: 12/12', True, (0, 0, 0))
    AvgWait = font.render('Average: 6.25 minutes', True, (0, 0, 0))
    AwaitingCount = font.render('1100', True, (0, 0, 0))
    BwaitingCount = font.render('1500', True, (0, 0, 0))
    CwaitingCount = font.render('2000', True, (0, 0, 0))
    TotalCount = font.render('0/4600', True, (0, 0, 0))
    US = font.render('Union Station', True, (0, 0, 0))

    clockR = clock.get_rect()
    traincountR = traincount.get_rect()
    AvgWaitR = AvgWait.get_rect()
    AWCR = AwaitingCount.get_rect()
    BWCR = BwaitingCount.get_rect()
    CWCR = CwaitingCount.get_rect()
    TCR = TotalCount.get_rect()
    USR = US.get_rect()

    clockR.center = (40, 436)
    traincountR.center = (100, 15)
    AvgWaitR.center = (500, 15)
    AWCR.center = (110, 155)
    BWCR.center = (306, 95)
    CWCR.center = (505, 180)
    TCR.center = (575, 436)
    USR.center = (565, 410)

    screen.blit(clock, clockR)
    screen.blit(traincount, traincountR)
    screen.blit(AvgWait, AvgWaitR)
    screen.blit(AwaitingCount, AWCR)
    screen.blit(BwaitingCount, BWCR)
    screen.blit(CwaitingCount, CWCR)
    screen.blit(TotalCount, TCR)
    screen.blit(US, USR)

#this is how the game moves
def game():
    trains = []  # (train, position, destination, wait)
    while True:
        screen.blit(bg, (0, 0))
        for t in trains:

            next = move(t[0].destination, t[0].destination, t[1], t[0].timetotravel)  # complete with train object
            if next == destination:
                if destination == A:
                    destination = B
                elif destination == B:
                    destination = BC
                elif destination == BC:
                    destination = C
                elif destination == C:
                    destination = US
                elif destination == US:
                    trains.remove(t)
                    continue
            t[1] = next
            pygame.draw.circle(screen, (0, 0, 0), next, 5)

        pygame.time.delay(100)
        displayUI()
        pygame.display.flip()


game()
