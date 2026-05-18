import requests

class AICommentator:

    def __init__(self, model, system_prompt):
        '''
        初始化AICommentator类，接受系统提示和语言模型作为参数。
        - 参数：
            - system_prompt: 用于指导语言模型生成评论的系统提示文本
            - model: 语言模型实例，具有generate方法用于生成文本
        '''
        self.model = model
        self.system_prompt = system_prompt

    def board_to_string(self, board):
        '''
        将棋盘状态转换为字符串格式，便于语言模型理解和生成评论。
        - 参数：
            - board: 当前棋盘状态
        - 返回值：
            - board_str: 棋盘状态的字符串表示
        '''
        board_str = ""
        for row in board:
            for cell in row:
                if cell == 0:
                    board_str += ". "
                elif cell == 1:
                    board_str += "O "
                elif cell == 2:
                    board_str += "X "
            board_str += "\n"
        return board_str.strip()
    
    def write_prompt(self, board, ai_row, ai_column, ai_player):
        '''
        根据当前棋盘状态和当前玩家，构建用于语言模型生成评论的提示文本。
        - 参数：
            - board: 当前棋盘状态
            - ai_row: AI玩家的行位置
            - ai_column: AI玩家的列位置
            - ai_player: AI玩家的标识（1或2）
        - 返回值：
            - prompt: 用于语言模型生成评论的完整提示文本
        '''
        board_str = self.board_to_string(board)
        prompt = f"当前棋盘：\n{board_str}\n你是{'白棋（O）' if ai_player == 1 else '黑棋（X）'}，对手是{'黑棋（X）' if ai_player == 1 else '白棋（O）'}。你刚刚落子在：({ai_row}, {ai_column})\n请评论你的这步棋，注意有没有连线、有没有威胁、以及对手刚刚的动向。"
        return prompt

    def generate_commentary(self, board, ai_row, ai_column, ai_player):
        '''
        生成关于当前棋盘状态和当前玩家的评论。
        - 参数：
            - board: 当前棋盘状态
            - ai_row: AI玩家的行位置
            - ai_column: AI玩家的列位置
            - ai_player: AI玩家的标识（1或2）
        - 返回值：
            - response: 语言模型生成的评论文本
        '''
        prompt = self.write_prompt(board, ai_row, ai_column, ai_player)
        print(prompt)  # Debug: 输出生成评论的提示文本

        response = requests.post("http://localhost:11434/api/generate", json={
            "model": self.model,
            "system": self.system_prompt,
            "prompt": prompt,
            "stream": False
        })
        return response.json()["response"]
        