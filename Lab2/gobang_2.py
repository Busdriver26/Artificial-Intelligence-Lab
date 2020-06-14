import pygame 
import copy
import time

EMPTY = 0
BLACK = 1
WHITE = 2
ROW = COL = 15
black_color = [0,0,0]
white_color = [255,255,255]

class RenjuBoard(object):

    def __init__(self):
        # self._board = [[EMPTY] * 15 for _ in range(15)]
        # self._board = [[None] * 15 ] * 15
        self._board = [[]] * 15
        self.jdg = 0
        self.reset()

    def reset(self):
        for row in range(len(self._board)):
            self._board[row] = [EMPTY] * 15

    def had(self, row ,col):
        if self._board[row][col]==EMPTY:
            return False
        return True

    def move(self, row, col, is_black):
        if self._board[row][col] == EMPTY:
            self._board[row][col] = BLACK if is_black else WHITE
            return True
        return False

    def draw(self, screen):
        # 画棋盘线
        for i in range(1, 16):
            pygame.draw.line(screen, black_color, [40, 40 * i], [600, 40 * i], 1)
            pygame.draw.line(screen, black_color, [40 * i, 40], [40 * i, 600], 1)
        # 画点
        pygame.draw.rect(screen, black_color, [36, 36, 568, 568], 4)  # [起点横坐标，起点纵坐标，宽，高]
        pygame.draw.circle(screen, black_color, [320, 320], 5, 0)  # 5表示半径 最后一个参数为0 表示实心线条
        pygame.draw.circle(screen, black_color, [160, 160], 5, 0)
        pygame.draw.circle(screen, black_color, [480, 480], 5, 0)
        pygame.draw.circle(screen, black_color, [480, 160], 5, 0)
        pygame.draw.circle(screen, black_color, [160, 480], 5, 0)
        # 显示棋子
        for row in range(len(self._board)):
            for col in range(len(self._board[row])):
                if self._board[row][col] != EMPTY:
                    ccolor = black_color if self._board[row][col] == BLACK else white_color
                    pos = [40 * (col + 1), 40 * (row + 1)]
                    pygame.draw.circle(screen, ccolor, pos, 20, 0)
    def is_win(self,board,row,col):
        count = 0 # 判断是否大于5
        winflag = 1 # 同种棋子计数，第一个棋子不算
        cur = self._board[row][col] # 记录当前所下的棋

        # 水平方向判断
        # 往左读5个点，col不变，row--
        i = row - 1
        j = col
        while i >= 0 and count < 5:
            if self._board[i][j] == cur:
                winflag += 1
                count += 1
                i -= 1
            else:
                break
        count *= 0
        #往右读取5个点，y不变，x++

        i = row + 1
        j = col
        while i < ROW and count < 5:
            if self._board[i][j] == cur:
                winflag += 1
                count += 1
                i += 1
            else:
                break

        count *= 0
        # 水平方向读取完毕，判断输赢，赢返回True
        if winflag >= 5:
            return True
        else:
            winflag //= winflag

        # 垂直判断
        # 往下判断，x不变，y++
        i = row
        j = col + 1
        while j < COL and count < 5:
            if self._board[i][j] == cur:
                winflag += 1
                count += 1
                j += 1
            else:
                break
        count *= 0
        # 垂直判断
        # 往上判断，x不变，y--
        i = row
        j = col - 1
        while j >= 0 and count < 5:
            if self._board[i][j] == cur:
                winflag += 1
                count += 1
                j -= 1
            else:
                break
        count *= 0
        # 水平方向读取完毕，判断输赢，赢返回True
        if winflag >= 5:
            return True
        else:
            winflag //= winflag

        # 主对角线方向判断
        # 往右下方向 x++ y++
        i = row + 1
        j = col + 1
        while i < ROW and j < COL and count < 5:
            if self._board[i][j] == cur:
                winflag += 1
                count += 1
                j += 1
                i += 1
            else:
                break
        count *= 0

        # 往左上方向 x-- y--
        i = row - 1
        j = col - 1
        while i >= 0 and j >= 0 and count < 5:
            if self._board[i][j] == cur:
                winflag += 1
                count += 1
                j -= 1
                i -= 1
            else:
                break
        count *= 0
        # 主对角线方向读取完毕，判断输赢，赢返回True
        if winflag >= 5:
            return True
        else:
            winflag //= winflag

        # 斜对角线方向判断
        # 往右上方向 x++ y--
        i = row + 1
        j = col - 1
        while i < ROW and j >= 0 and count < 5:
            if self._board[i][j] == cur:
                winflag += 1
                count += 1
                j -= 1
                i += 1
            else:
                break
        count *= 0

        # 往左下方向 x-- y++
        i = row - 1
        j = col + 1
        while i >= 0 and j < COL and count < 5:
            if self._board[i][j] == cur:
                winflag += 1
                count += 1
                j += 1
                i -= 1
            else:
                break
        count *= 0
        # 斜对角线方向读取完毕，判断输赢，赢返回True
        if winflag >= 5:
            return True
        else:
            winflag //= winflag

        # 所有方向判断完毕，没出现胜负
        return False

###AI算法区域：
###用到的变量：全局变量ROW_AI COL_AI是计算出的结果
#
ROW_AI = 5
COL_AI = 5
MAX = 10000000000000 #白棋AI胜利,5个白棋
MIN = -10000000000000 #黑棋玩家胜利,5个黑棋
H5 = MAX
H4 = 9995000 
C4 = 10000
H3 = 10000
C3 = 500
H2 = 500
turn = WHITE

def scr(st):
    #st是一个一维数组
    ret = [0,0,0]
    l=len(st)
    b = BLACK
    w = WHITE
    e = EMPTY
    if(l>=5):
        for i in range(l-5):
            if(st[i:i+5]==[w,w,w,w,w]):
                ret = [0,MIN,MAX]
                return ret
            elif (st[i:i+5]==[b,b,b,b,b]):
                ret = [0,MAX,MIN]
                return ret
            elif (st[i:i+5]==[b,b,e,b,b]):
                ret[b]+=C4
            elif (st[i:i+5]==[w,w,e,w,w]):
                ret[w]+=C4
    if(l>=6):
        for i in range(l-6):
            if(st[i:i+6]==[e,b,b,b,b,e]):
                ret[BLACK]+=H4
                if turn == w:
                    ret[b]+=MAX
            elif(st[i:i+6]==[e,w,w,w,w,e]):
                ret[WHITE]+=H4
                if turn == b:
                    ret[w]+=MAX
            elif(st[i:i+6]==[e,w,w,w,w,b] or st[i:i+6]==[b,w,w,w,w,e]):
                ret[WHITE]+=C4
                if turn == b:
                    ret[w]+=MAX
            elif(st[i:i+6]==[e,b,b,b,b,w] or st[i:i+6]==[w,b,b,b,b,e]):
                ret[BLACK]+=C4
                if turn == w:
                    ret[BLACK]+=MAX   
    if(l>=5):
        for i in range(l-5):
            if(st[i:i+5]==[e,w,w,w,e]):
                ret[WHITE]+=H3
                if turn == b:
                    ret[w]+=MAX
            if(st[i:i+5]==[e,b,b,b,e]):
                ret[BLACK]+=H3
                if turn == w:
                    ret[BLACK]+=MAX
    if(l>=4):
        for i in range(l-6):
            if(st[i:i+4]==[e,w,w,e]):
                ret[WHITE]+=H2
            if(st[i:i+4]==[e,b,b,e]):
                ret[BLACK]+=H2
    if(l>=6):
        for i in range(l-6):
            if(st[i:i+6]==[e,b,b,e,b,e]  or st[i:i+6]==[e,b,e,b,b,e]):
                ret[BLACK]+=H4
                if turn == w:
                    ret[BLACK]+=MAX
            if(st[i:i+6]==[e,w,w,e,w,e]):
                ret[w]+=H4
                if turn == b:
                    ret[w]+=MAX
            if(st[i:i+6]==[e,w,e,w,w,e]):
                ret[w]+=H4
                if turn == b:
                    ret[w]+=MAX
    return ret


def judge(board):
    global turn
    d = board._board
    turn = board.turn
    ret = [0,0,0]
    #score返回的应该是一个List[3] list[BLACK]是BLACK分数，black==1
    #横向15行：
    for i in range(15):
        st = board._board[i][0:15]
        score = scr(st)
        ret[0]+=score[0]
        ret[1]+=score[1]
        ret[2]+=score[2]
    #纵向15列：
    for i in range(15):
        st = [d[j][i] for j in range(15)]
        score = scr(st)
        ret[0]+=score[0]
        ret[1]+=score[1]
        ret[2]+=score[2]
    #斜向
    temp1 = []
    temp2 = []
    temp3 = []
    temp4 = []
    for i in range(1,16):
        for j in range(i):
            temp1.append(d[j][i-j-1])
            temp2.append(d[i-j-1][j])
            temp3.append(d[14-j][i-j-1])
            temp4.append(d[i-j-1][14-j])
        score1 = scr(temp1)
        ret[0]+=score1[0]
        ret[1]+=score1[1]
        ret[2]+=score1[2]
        score2 = scr(temp2)
        ret[0]+=score2[0]
        ret[1]+=score2[1]
        ret[2]+=score2[2]
        score3 = scr(temp3)
        ret[0]+=score3[0]
        ret[1]+=score3[1]
        ret[2]+=score3[2]
        score4 = scr(temp4)
        ret[0]+=score4[0]
        ret[1]+=score4[1]
        ret[2]+=score4[2]
        temp1.clear()
        temp2.clear()
        temp3.clear()
        temp4.clear()
    if(ret!=[0,0,0]):
        print(ret)
    return -ret[BLACK]+ret[WHITE]
    


def srd(board,i,j):
    if i==0 and j==0:
        return board.had(0,1) or board.had(1,0) or board.had(1,1)
    elif i==0 and j==14:
        return board.had(0,13) or board.had(1,13) or board.had(1,14)
    elif i==14 and j==0:
        return board.had(13,0) or board.had(13,1) or board.had(14,1)
    elif i==14 and j==14:
        return board.had(13,13) or board.had(13,14) or board.had(14,13)
    elif i==0:
        return (board.had(i,j-1) or board.had(i+1,j-1)
             or board.had(i+1,j)
             or board.had(i,j+1) or board.had(i+1,j+1))
    elif i==14:
        return (board.had(i-1,j-1) or board.had(i,j-1)
            or board.had(i-1,j) 
            or board.had(i-1,j+1) or board.had(i,j+1))
    elif j==0:
        return (board.had(i-1,j)  or board.had(i+1,j)
            or board.had(i-1,j+1) or board.had(i,j+1) or board.had(i+1,j+1))
    elif j==14:
        return (board.had(i-1,j-1) or board.had(i,j-1) or board.had(i+1,j-1)
            or board.had(i-1,j)  or board.had(i+1,j))
    return (board.had(i-1,j-1) or board.had(i,j-1) or board.had(i+1,j-1)
            or board.had(i-1,j)  or board.had(i+1,j)
            or board.had(i-1,j+1) or board.had(i,j+1) or board.had(i+1,j+1))

def ai(board):
    temp = RenjuBoard()
    stc1 = [] #Max层
    stc2 = [] #Min层
    stc3 = [] #Max层
    #stc4 = [] #Min层
    global ROW_AI
    global COL_AI
    
    #第一步：第一次添加下层变量
    for i in range(15):
        for j in range(15):
            if(board._board[i][j]==EMPTY and srd(board,i,j)):
                #为了不过多判断，只添加周围有子的点
                temp = copy.deepcopy(board)
                temp._board[i][j] = WHITE
                temp.jdg = MAX
                temp.addi=i
                temp.addj=j
                if(temp.is_win(temp,i,j)):
                    ROW_AI=i
                    COL_AI=j
                    return
                temp.zhizhen = board
                temp.turn = WHITE
                stc1.append(temp)
    #第二次循环添加下层变量：
    for bd in stc1:
        for i in range(15):
            for j in range(15):
                if(bd._board[i][j]==EMPTY and srd(bd,i,j)):
                    #为了不过多判断，只添加周围有子的点
                    temp = copy.deepcopy(bd)
                    temp._board[i][j] = BLACK
                    temp.jdg = MIN
                    temp.turn = BLACK
                    temp.addi=i
                    temp.addj=j
                    temp.zhizhen = bd
                    stc2.append(temp)
    
    for bd in stc2: #第2层是最小层，上层是最大层，根据alpha剪枝，要大于上层结点曾经有过的alpha才考虑
        bd.jdg = judge(bd)
        up = bd.zhizhen
        if(bd.jdg>up.jdg):
            stc2.remove(bd)
        else:
            up.jdg = bd.jdg
    
    M = -99999999999999999
    for bd in stc1:
        print("BDF:",end="")
        print(bd.jdg,bd.addi,bd.addj,bd.had(bd.addi,bd.addj))
        if bd.jdg>M:
            M = bd.jdg
            ROW_AI=bd.addi
            COL_AI=bd.addj
    print(MIN,MAX)
    print(M,ROW_AI,COL_AI)

###

def main(): # 单一职责原则
    # 初始化
    global ROW_AI
    global COL_AI
    board = RenjuBoard()
    pygame.init()
    #构造游戏窗口
    pygame.display.set_caption("AI EXP2")  # 创建标题
    screen = pygame.display.set_mode([640,640]) # [600,600] 屏幕的大小，以像素为单位
    screen.fill([200,200,169])
    board.draw(screen)
    pygame.display.flip() # 刷新窗口
    running = True
    is_black = True
    flag = 1
    while running:
        # 顺序处理每轮循环中的事件库中的事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # 窗口关闭时间
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and \
                    event.button == 1 and flag == 1: # 1 表示点击鼠标左键
                x, y = event.pos #鼠标的位置
                col = round((x - 40) / 40) # round : 四舍五入
                row = round((y - 40) / 40)
                if (40 <= x <= 600 and 40 <= y <= 600) == False:
                    continue
                if board.move(row, col, is_black):
                    if board.is_win(board, row, col):
                        # running = False
                        screen.fill([0,0,0])
                        #board.draw(screen)
                        pygame.display.flip()  # 更新窗口
                        ZiTiDuiXiang = pygame.font.SysFont('Times New Roman', 32)
                        WenBenKuangDuiXiang = ZiTiDuiXiang.render("Black win!" if is_black else
                                                                  "White win!", True, [200,200,169])
                        KuangDuiXiang = WenBenKuangDuiXiang.get_rect()
                        KuangDuiXiang.center = (300, 300)
                        screen.blit(WenBenKuangDuiXiang, KuangDuiXiang)
                        pygame.display.update()
                        flag = 0
                    else:
                        screen.fill([200,200,169])
                        board.draw(screen)
                        pygame.display.flip() # 更新窗口
                        #显示calculating
                        ZiTiDuiXiang = pygame.font.SysFont('Times New Roman', 32)
                        WenBenKuangDuiXiang = ZiTiDuiXiang.render("Calculating...", True, [0,0,0])
                        KuangDuiXiang = WenBenKuangDuiXiang.get_rect()
                        KuangDuiXiang.center = (215, 15)
                        screen.blit(WenBenKuangDuiXiang, KuangDuiXiang)
                        pygame.display.update()
                        #
                        ai(board) #接入AI计算行列
                        board.move(ROW_AI,COL_AI,0)
                        screen.fill([200,200,169])
                        board.draw(screen)
                        pygame.display.update()
                        if board.is_win(board, ROW_AI, COL_AI):
                            board.draw(screen)
                            pygame.display.flip()  # 更新窗口
                            time.sleep(3)
                            screen.fill([0,0,0])
                            ZiTiDuiXiang = pygame.font.SysFont('Times New Roman', 32)
                            WenBenKuangDuiXiang = ZiTiDuiXiang.render("White win!", True, [200,200,169])
                            KuangDuiXiang = WenBenKuangDuiXiang.get_rect()
                            KuangDuiXiang.center = (300, 300)
                            screen.blit(WenBenKuangDuiXiang, KuangDuiXiang)
                            pygame.display.update()
                            flag = 0

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    running=False
                    '''
                    flag = 1
                    is_black = True
                    board.reset()
                    screen.fill([200,200,169])
                    board.draw(screen)
                    pygame.display.flip()  # 更新窗口
                    '''
                else:
                    running = False
    # 退出
    pygame.quit()

if __name__ == '__main__':
    main()