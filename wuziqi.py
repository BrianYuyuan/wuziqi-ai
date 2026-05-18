import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import threading

import ai_player
import ai_commentator

class WuziqiGUI:
    '''
    创建和管理棋游戏的图形用户界面。使用tkinter库来绘制游戏板、处理用户输入，并显示游戏状态和结果。
    '''

    # 定义颜色映射和界面布局常量
    color_map = {
    0: "",
    1: "White",
    2: "Black"
    }
    
    MARGIN = 40

    def __init__(self, game):
        '''
        初始化TicTacToeGUI类，设置游戏实例，并创建主窗口。
         - 参数：
              - game: TicTacToeGame实例，包含游戏逻辑和状态。
        '''
        self.game = game
        self.root = tk.Tk()
        self.root.title("棋")
        self.root.withdraw()  # 隐藏主窗口，直到玩家选择角色

        # if self.game.mode == "PvE":
        #     self.commentator = ai_commentator.AICommentator(
        #         model="qwen2.5:7b",
        #         system_prompt="你是一个自大的五子棋选手，每次落子后用一两句话简单解释你的选择。"  
        #     )

    def create_board(self):
        '''
        创建游戏棋盘。
        '''
        # 创建游戏棋盘，绘制网格线
        grid_end = self.MARGIN + (self.game.size - 1) * 40
        canvas_size = grid_end + self.MARGIN
        self.canvas = tk.Canvas(self.root, width=canvas_size, height=canvas_size, bg="burlywood")
        self.canvas.grid(row=0, column=0)
        for i in range(self.game.size):
            self.canvas.create_line(self.MARGIN, i * 40 + self.MARGIN, grid_end, i * 40 + self.MARGIN)
        for j in range(self.game.size):
            self.canvas.create_line(j * 40 + self.MARGIN, self.MARGIN, j * 40 + self.MARGIN, grid_end)

        # 绑定鼠标点击事件到棋盘
        self.canvas.bind("<Button-1>", self.on_click)

        # 创建状态标签
        self.status = tk.Label(self.root, text="Current Player: White", font=("Arial", 14), width=20)
        self.status.grid(row=1, column=0)

        # 创建评论员框
        self.commentator_label = tk.LabelFrame(self.root, text="AI Player", labelanchor = "n")
        self.commentator_label.grid(row=0, column=1)

        self.commentator_box = tk.Text(self.commentator_label, font=("Arial", 12), width=25, height=20, wrap="word")
        self.commentator_box.grid(row=0, column=1, padx=10)
        self.commentator_box.config(state="disabled")

        # self.restart_button = tk.Button(self.root, text="Restart", font=("Arial", 12), command=self.restart_game)
        # self.restart_button.grid(row=2, column=0, pady=10)

    def on_click(self, event):
        '''
        处理鼠标点击事件，计算点击位置对应的棋盘格，并尝试进行下一步棋。
        - 参数：
             - event: 鼠标点击事件对象，包含点击位置的坐标。
        '''
        # 处理鼠标点击事件，计算点击位置对应的棋盘格
        col = round((event.x - self.MARGIN) / 40)
        row = round((event.y - self.MARGIN) / 40)
        if row < 0 or row >= self.game.size or col < 0 or col >= self.game.size:
            return
        result = self.game.play_next_move(row, col)
    
        if result == "INVALID":
            return
        
        self.draw_pieces(row, col)

        if result == "WIN":
            self.show_winner()
            self.root.quit() # Need to change this to reset the game instead of quitting
            return
        elif result == "TIE":
            self.show_tie()
            self.root.quit() # Need to change this to reset the game instead of quitting
            return

        self.root.update()

        # 如果是PvE模式，并且当前玩家是AI，则让AI进行下一步棋
        if self.game.mode == "PvE" and self.game.current_player == self.game.this_ai_player:
            ai_row, ai_col = self.game.AIPlayer.choose_move()
            ai_result = self.game.play_next_move(ai_row, ai_col)
            if ai_result == "INVALID":
                return
            
            self.commentator_box.config(state="normal")
            self.commentator_box.delete('1.0', 'end')
            self.commentator_box.insert('1.0', "AI is thinking...")
            self.commentator_box.config(state="disabled")
            self.root.update()

            self.draw_pieces(ai_row, ai_col)
            self.show_commentary(self.game.board, ai_row, ai_col, self.game.this_ai_player)

            if ai_result == "WIN":
                self.show_winner()
                self.root.quit() # Need to change this to reset the game instead of quitting
                return
            elif ai_result == "TIE":
                self.show_tie()
                self.root.quit() # Need to change this to reset the game instead of quitting
                return
            
    def show_commentary(self, board, ai_row, ai_column, this_ai_player):
        '''
        显示关于当前棋盘状态和当前玩家的评论。
        - 参数：
             - board: 当前棋盘状态
             - ai_row: AI玩家的行位置
             - ai_column: AI玩家的列位置
             - ai_player: AI玩家的标识（1或2）
        '''
        def background_task():
            commentary = self.commentator.generate_commentary(board, ai_row, ai_column, this_ai_player)
            print(commentary)  # Debug: 输出生成的评论
            self.commentator_box.config(state="normal")
            self.commentator_box.delete('1.0', 'end')
            self.root.after(0, lambda: self.commentator_box.insert('1.0', commentary))
            self.commentator_box.config(state="disabled")

        threading.Thread(target=background_task).start()

        # commentary = self.ai_commentator.generate_commentary(board, ai_row, ai_column, this_ai_player)
        # print(commentary)
        # self.commentator_box.config(state="normal")
        # self.commentator_box.delete('1.0', 'end')
        # self.commentator_box.insert('1.0', commentary)
        # self.commentator_box.config(state="disabled")

    def draw_pieces(self, row, col):
        '''
        在指定位置绘制棋子，并更新游戏状态显示。
        - 参数：
             - row: 棋子所在的行
             - col: 棋子所在的列
        '''
        cx = self.MARGIN + col * 40
        cy = self.MARGIN + row * 40
        r = 16
        if color := self.color_map[self.game.board[row][col]]:
            outline = "#555" if color == "White" else "#000"
            self.canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill=color, outline=outline, width=2)
        self.update_status()

    def update_status(self):
        '''
        更新当前玩家的显示状态。
        '''
        color = self.color_map[self.game.current_player]
        self.status.config(text=f"Current Player: {color}")  

    def show_winner(self):
        '''
        显示获胜玩家的消息框。
        '''
        winner = self.color_map[self.game.current_player]
        tk.messagebox.showinfo("Game Over", f"Player {winner} wins!")
    
    def show_tie(self):
        '''
        显示平局的消息框。
        '''
        tk.messagebox.showinfo("Game Over", "It's a tie!")
    
    def show_mode_selection(self):
        '''
        显示游戏模式选择窗口，允许玩家选择PvP或PvE模式。
        '''
        self.selection_window = tk.Toplevel(self.root)
        self.selection_window.title("Choose Your Side")
        
        notebook = ttk.Notebook(self.selection_window)
        notebook.pack(pady=40, padx=50)

        frame1 = ttk.Frame(notebook)
        frame2 = ttk.Frame(notebook)

        label1 = ttk.Label(frame1, text = "PvP", font = ("Arial", 12))
        label1.pack(pady=40)
        button1 = ttk.Button(frame1, text = "Play", command=lambda: self.set_player(PLAYER1, "PvP"))
        button1.pack(pady=10)

        label2 = ttk.Label(frame2, text = "PvE", font = ("Arial", 12))
        label2.pack(pady=40)
        button2 = ttk.Button(frame2, text="Play as White", command=lambda: self.set_player(PLAYER1, "PvE"))
        button3 = ttk.Button(frame2, text="Play as Black", command=lambda: self.set_player(PLAYER2, "PvE"))
        button2.pack(pady=10)
        button3.pack(pady=10)

        notebook.add(frame1, text="Player vs Player")
        notebook.add(frame2, text="Player vs AI")

        self.selection_window.wait_window()  # Ensure the window stays open until closed
    
    def set_player(self, player, mode):
        '''
        设置玩家选择，并开始游戏。
        - 参数：
             - player: 玩家选择的棋子（PLAYER1或PLAYER2）
             - mode: 游戏模式
        '''
        self.game.mode = mode
        self.game.current_player = PLAYER1
        if mode == "PvE":
            self.game.AIPlayer = ai_player.AIPlayer(self.game)
            self.game.this_ai_player = PLAYER2 if player == PLAYER1 else PLAYER1
            self.commentator = ai_commentator.AICommentator(
                model="qwen2.5:7b",
                system_prompt="你是一个自大的五子棋选手，每次落子后用一两句话简单解释你的选择。"  
            )
        self.selection_window.destroy()
        self.root.deiconify()
        self.start_game()

    def start_game(self):
        '''
        开始游戏，创建棋盘并处理AI的第一步棋（如果AI先手）。
        '''
        self.create_board()
        if self.game.mode == "PvE" and self.game.this_ai_player == PLAYER1:
            ai_row, ai_col = self.game.AIPlayer.choose_move()
            self.game.play_next_move(ai_row, ai_col)
            self.draw_pieces(ai_row, ai_col)
        self.root.mainloop()

    def start(self):
        '''
        显示玩家选择窗口并开始游戏。
        '''
        self.show_mode_selection()


class WuziqiGame:
    """
    管理五子棋游戏的核心逻辑，包括棋盘状态、玩家切换、胜利条件检查等。
    """

    # 定义胜利条件检查的方向向量
    DIRECTIONS = [
    (1, 0),   # vertical
    (0, 1),   # horizontal
    (1, 1),   # main diagonal
    (1, -1),  # anti diagonal
    ]

    def __init__(self, size, win_length):
        '''
        初始化WuziqiGame类，设置棋盘大小、胜利条件长度和游戏模式。
        - 参数：
             - size: 棋盘的大小（例如，15表示15x15的棋盘）
             - win_length: 获胜所需连续棋子的数量
             - mode: 游戏模式（例如，"PvP"表示玩家对玩家，"PvE"表示玩家对AI）
        '''
        # 初始化游戏参数
        self.size = size
        self.win_length = win_length
        self.mode = None

        # 根据游戏模式初始化图形界面和AI玩家
        self.gui = WuziqiGUI(self)

        # # 如果是PvE模式，初始化AI玩家
        # if self.mode == "PvE":
        #     self.AIPlayer = ai_player.AIPlayer(self)

        # 初始化棋盘状态和当前玩家
        self.board = [[EMPTY]*size for _ in range(size)]
        self.current_player = PLAYER1
        # self.this_ai_player = PLAYER2  # 默认AI为黑棋

    def play_next_move(self, row, col):
        '''
        处理玩家的下一步棋，更新棋盘状态，并检查游戏结果。
        - 参数：
             - row: 玩家选择的行
             - col: 玩家选择的列
        - 返回值：
             - "INVALID": 如果玩家选择的位置已经有棋子
             - "WIN": 如果玩家的这一步棋导致获胜
             - "TIE": 如果棋盘已满且没有获胜者
             - "OK": 如果棋局继续进行
        '''
        if not self.board[row][col] == EMPTY:
            return "INVALID"

        self.board[row][col] = self.current_player

        if self.check_win_from(row, col):
            return "WIN"
        
        elif self.check_full():
            return "TIE"

        self.switch_player()
        return "OK"
    
    def switch_player(self):
        '''
        切换当前玩家。
        '''
        self.current_player = PLAYER2 if self.current_player == PLAYER1 else PLAYER1

    def check_full(self):
        '''
        检查棋盘是否已满。
        - 返回值：
             - True: 如果棋盘已满
             - False: 如果棋盘还有空位
        '''
        return all(cell != EMPTY for row in self.board for cell in row)

    def check_win_from(self, row, col):
        '''
        检查从指定位置开始是否满足获胜条件。
        - 参数：
             - row: 检查的行
             - col: 检查的列
        - 返回值：
             - True: 如果满足获胜条件
             - False: 如果不满足获胜条件
        '''
        player = self.board[row][col]
        for dr, dc in self.DIRECTIONS:
            count = 1
            count += self.count_direction(row, col, dr, dc, player)
            count += self.count_direction(row, col, -dr, -dc, player)
            if count >= self.win_length:
                return True
        return False

    def count_direction(self, row, col, dr, dc, player):
        '''
        计算在指定方向上连续棋子的数量。
        - 参数：
             - row: 起始行
             - col: 起始列
             - dr: 行方向增量
             - dc: 列方向增量
             - player: 当前玩家的棋子类型
        - 返回值：
             - 连续棋子的数量
        '''
        count = 0
        row += dr
        col += dc
        while row >= 0 and row < len(self.board) and col >= 0 and col < len(self.board[0]):
            if self.board[row][col] == player:
                count += 1
            else:
                break
            row += dr
            col += dc
        return count

# 定义游戏常量
SIZE = 15
WIN_LENGTH = 5
EMPTY = 0
PLAYER1 = 1
PLAYER2 = 2

# 主程序入口，创建游戏实例并启动图形界面
if __name__ == "__main__":
    game = WuziqiGame(SIZE, WIN_LENGTH)
    game.gui.start()