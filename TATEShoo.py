import math
import random
import sys
import time

import pygame as pg
from pygame.sprite import AbstractGroup

WIDTH = 600
HEIGHT = 1000

def check_bound(obj: pg.Rect) -> tuple[bool, bool]:
    """
    オブジェクトが画面内か画面外かを判定し，真理値タプルを返す
    引数 obj：オブジェクト（爆弾，こうかとん，ビーム）SurfaceのRect
    戻り値：横方向，縦方向のはみ出し判定結果（画面内：True／画面外：False）
    """
    yoko, tate = True, True
    if obj.left < 0 or WIDTH < obj.right:  # 横方向のはみ出し判定
        yoko = False
    if obj.top < 0 or HEIGHT < obj.bottom:  # 縦方向のはみ出し判定
        tate = False
    return yoko, tate

class Player(pg.sprite.Sprite):
    """
    ゲームキャラクター（こうかとん）に関するクラス
    """
    delta = {  # 押下キーと移動量の辞書
        pg.K_UP: (0, -1),
        pg.K_DOWN: (0, +1),
        pg.K_LEFT: (-1, 0),
        pg.K_RIGHT: (+1, 0),
    }

    def __init__(self, xy: tuple[int, int]):
        """
        こうかとん画像Surfaceを生成する
        引数1 num：こうかとん画像ファイル名の番号
        引数2 xy：こうかとん画像の位置座標タプル
        """
        super().__init__()
        img0 = pg.transform.rotozoom(pg.image.load(f"ex05/fig/jiki.png"), 0, 0.05)  # 左向き，2倍
        self.img = img0
        self.rct = self.img.get_rect()
        self.rct.center = xy
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return 0
            else:
                self.speed = 7

    def update(self, key_lst: list[bool], screen: pg.Surface):
        """
        押下キーに応じてこうかとんを移動させる
        引数1 key_lst：押下キーの真理値リスト
        引数2 screen：画面Surface
        """
        sum_mv = [0, 0]
        for k, mv in __class__.delta.items():
            if key_lst[k]:
                self.rct.move_ip(+self.speed*mv[0], +self.speed*mv[1])
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        if check_bound(self.rct) != (True, True):
            for k, mv in __class__.delta.items():
                if key_lst[k]:
                    self.rct.move_ip(-self.speed*mv[0], -self.speed*mv[1])
        screen.blit(self.img, self.rct) 

class Enemy(pg.sprite.Sprite):
    lrCheese = [0, 900]

    def __init__(self):
        super().__init__()
        self.image = pg.transform.rotozoom(pg.image.load("ex05/fig/tekibig.png"), 0, 0.04)
        self.rect = self.image.get_rect()
        self.direction = random.randint(1,1000)
        if self.direction < 500:
            self.rect.centerx = 0
        else:
            self.rect.centerx = 600
        self.rect.centery = random.randint(0,300)
        self.dx = 2
        print("deta")
        print(self.rect)
    
    def update(self):
        if self.direction < 500 :
            self.rect.move_ip(2,2)
            if self.rect.left > 100:
                self.rect.move_ip(0, -2)
            if self.rect.left > 480:
                self.rect.move_ip(0, -2)
        else :
            self.rect.move_ip(-2, 2)
            if self.rect.left > 100:
                self.rect.move_ip(0, -2)
            if self.rect.left > 480:
                self.rect.move_ip(0, -2)
        if self.rect.right < 0:
            self.kill()
        if self.rect.left > 900:
            self.kill()

def main():
    pg.display.set_caption("はじめてのPygame")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock  = pg.time.Clock()
    bg_img = pg.image.load("ex05/fig/haikei.jpg")
    bg_img = pg.transform.rotozoom(bg_img, 0, 2)
    player = Player((300, 800))
    emys = pg.sprite.Group()
    tmr = 0
    clock = pg.time.Clock()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: return

        screen.blit(bg_img, [0,0])

        if tmr%200 == 0:  # 200フレームに1回，敵機を出現させる
            emys.add(Enemy())

        key_lst = pg.key.get_pressed()
        emys.update()
        emys.draw(screen)
        player.update(key_lst, screen)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()