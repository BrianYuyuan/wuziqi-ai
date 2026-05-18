import random

import wuziqi

class AIPlayer:
    '''
    负责评估棋盘状态并选择最佳下一步棋。
    '''

    # 定义胜利条件检查的方向向量
    DIRECTIONS = [
    (1, 0),   # vertical
    (0, 1),   # horizontal
    (1, 1),   # main diagonal
    (1, -1),  # anti diagonal
    ]
    
    def __init__(self, game):
        '''
        初始化AIPlayer类，接受一个wuziqi实例作为参数。
        - 参数：
             - game: wuziqi实例，包含当前游戏状态和规则
        '''
        self.game = game

    def evaluate_position(self):
        '''
        评估当前棋盘状态，计算每个空位的价值
        - 返回值：
             - position_values: 一个字典，键为空位的坐标（row, col），值为该位置的评估分数
        '''
        position_values = {}
        for row in range(self.game.size):
            for col in range(self.game.size):
                if not self.game.board[row][col] == wuziqi.EMPTY:
                    continue
                value = 0
                value += self.check_streak(row, col, 1)
                value += self.check_streak(row, col, 2)

                # 如果位置在靠中间的部分，增加额外的价值
                center = self.game.size // 2
                distance_from_center = abs(row - center) + abs(col - center)
                value += self.game.size - distance_from_center

                position_values[(row, col)] = value
        return position_values
    
    def check_streak(self, row, col, player):
        '''
        检查从指定位置开始，沿各个方向的连续棋子数量，并根据数量评估该位置的价值。
        - 参数：
             - row: 检查的行
             - col: 检查的列
             - player: 要检查的玩家（1或2）
        - 返回值：
             - total_value: 根据连续棋子数量计算的评估分数
        '''
        total_value = 0
        for dr, dc in self.DIRECTIONS:
            count = 1
            count += self.count_direction(row, col, dr, dc, player)
            count += self.count_direction(row, col, -dr, -dc, player)
            if count == self.game.win_length:
                total_value += 10000
            elif count == self.game.win_length-1:
                total_value += 1000
            elif count == self.game.win_length-2:
                total_value += 100
            elif count == self.game.win_length-3: # 注意这里相当于假设win_length不能低于4，否则会出现负数
                total_value += 10
            elif count == 0:
                total_value += 0
            else:
                total_value += 1
        return total_value

    def count_direction(self, row, col, dr, dc, player):
        '''
        沿指定方向计数连续棋子数量。
        - 参数：
             - row: 起始行
             - col: 起始列
             - dr: 行方向增量
             - dc: 列方向增量
             - player: 当前玩家的棋子类型
        - 返回值：
             - count: 连续棋子的数量
        '''
        count = 0
        row += dr
        col += dc
        while row >= 0 and row < len(self.game.board) and col >= 0 and col < len(self.game.board[0]):
            if self.game.board[row][col] == player:
                count += 1
            else:
                break
            row += dr
            col += dc
        return count
    
    def choose_move(self):
        '''
        选择最佳下一步棋。
        - 返回值：
             - best_move: 一个元组，包含最佳下一步棋的坐标（row, col）
        '''
        position_values = self.evaluate_position()
        # print("Position values:", position_values)  # Debugging line to print position values
        max_value = max(position_values.values())
        better_moves = [pos for pos, value in position_values.items() if value == max_value]
        # print("Better moves:", better_moves)  # Debugging line to print better moves
        move = random.choice(better_moves)
        return move
    
        # best_move = max(position_values, key=position_values.get)
        # return best_move
    
