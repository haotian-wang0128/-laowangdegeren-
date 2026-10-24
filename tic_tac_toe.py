# -*- coding: utf-8 -*-
"""
井字棋（Tic-Tac-Toe）人机对战（PyCharm 直接运行版）
- 仅使用 Python 标准库，无第三方依赖
- 玩家执 X 先手，电脑执 O
- 横/竖/斜任意三子连线获胜；棋盘下满无人连线为平局
运行方式：在 PyCharm 中右键本文件 -> Run 'tic_tac_toe'
"""

import random

# 所有能获胜的直线：前三组是横线，中间三组是竖线，最后两组是对角线
WIN_LINES = (
    (0, 1, 2), (3, 4, 5), (6, 7, 8),   # 三行
    (0, 3, 6), (1, 4, 7), (2, 5, 8),   # 三列
    (0, 4, 8), (2, 4, 6),              # 两条对角线
)


def new_board():
    """返回一个空棋盘：长度为 9 的列表，索引 0~8 对应盘面编号 1~9。"""
    return [""] * 9


def winner(board):
    """判断局面：返回 'X'/'O' 表示胜者，'Draw' 平局，None 未结束。"""
    for a, b, c in WIN_LINES:                  # 逐条检查获胜直线
        if board[a] != "" and board[a] == board[b] == board[c]:
            return board[a]                    # 三子相同，分出胜负
    if all(board):                             # 棋盘已满仍无胜者
        return "Draw"
    return None


def print_board(board):
    """打印 3x3 棋盘；空位显示编号 1~9，方便玩家输入。"""
    cells = [board[i] if board[i] else str(i + 1) for i in range(9)]
    print()
    print(" {} | {} | {} ".format(cells[0], cells[1], cells[2]))
    print("---+---+---")
    print(" {} | {} | {} ".format(cells[3], cells[4], cells[5]))
    print("---+---+---")
    print(" {} | {} | {} ".format(cells[6], cells[7], cells[8]))
    print()


def empty_cells(board):
    """返回所有仍可落子的索引列表。"""
    return [i for i, value in enumerate(board) if value == ""]


def find_line_move(board, mark):
    """若某条获胜线上已有两个 mark 且剩一个空位，返回该空位索引，否则 None。"""
    for a, b, c in WIN_LINES:
        line = [board[a], board[b], board[c]]
        if line.count(mark) == 2 and line.count("") == 1:
            return (a, b, c)[line.index("")]
    return None


def computer_move(board):
    """电脑（O）落子策略，按优先级返回索引：
    1 自己能赢先赢；2 玩家将赢则封堵；3 抢中心；4 抢角；5 随机。
    """
    return (
        find_line_move(board, "O")                                 # 1 主动取胜
        or find_line_move(board, "X")                              # 2 防守封堵
        or (4 if board[4] == "" else None)                         # 3 抢占中心
        or next((i for i in (0, 2, 6, 8) if board[i] == ""), None) # 4 抢占空角
        or random.choice(empty_cells(board))                       # 5 随机兜底
    )


def player_move(board):
    """读取玩家落子；对非数字、越界、已占用等非法输入提示后要求重输。"""
    while True:
        raw = input("请输入落子位置(1-9): ").strip()
        if not raw.isdigit():                       # 非纯数字
            print("输入无效，请输入 1-9 的数字。")
            continue
        pos = int(raw) - 1                          # 编号 1-9 映射到索引 0-8
        if pos < 0 or pos > 8:                      # 越界保护
            print("数字超出范围，请输入 1-9。")
            continue
        if board[pos] != "":                        # 位置已被占用
            print("该位置已有棋子，请换一个。")
            continue
        return pos


def ask_play_again():
    """询问是否再来一局；输入 y/yes 继续，其它输入退出。"""
    ans = input("再来一局? (y/n): ").strip().lower()
    return ans in ("y", "yes")


def play_one_round():
    """进行单局游戏：玩家 X 先手，与电脑 O 轮流落子，直到分出结果。"""
    board = new_board()
    turn = "X"
    while True:
        print_board(board)
        if turn == "X":
            board[player_move(board)] = "X"
        else:
            idx = computer_move(board)
            board[idx] = "O"
            print("电脑落子: {}".format(idx + 1))

        result = winner(board)
        if result is not None:                      # 已有胜负或平局
            print_board(board)
            if result == "X":
                print("你赢了!")
            elif result == "O":
                print("电脑获胜。")
            else:
                print("平局。")
            return
        turn = "O" if turn == "X" else "X"          # 交换出手方


def main():
    """程序入口：循环进行多局，直到玩家选择退出。"""
    print("=== 井字棋 ===  你是 X，电脑是 O，你执先手。")
    while True:
        play_one_round()
        if not ask_play_again():
            print("感谢游玩，再见!")
            break


if __name__ == "__main__":
    main()  # 仅直接运行本文件时启动；被 import 时不会自动执行