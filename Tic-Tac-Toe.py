import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.title("Tic-Tac-Toe")

player = "X"
board = ["", "", "", "", "", "", "", "", ""]
player_moves = {"X": 0, "O": 0}  
selected_index = None  

# Fungsi untuk memeriksa pemenang
def check_winner():
    win_conditions = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Horizontal
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Vertikal
        (0, 4, 8), (2, 4, 6)              # Diagonal
    ]
    for condition in win_conditions:
        if board[condition[0]] == board[condition[1]] == board[condition[2]] and board[condition[0]] != "":
            return True
    return False

def reset_game():
    global player, board, player_moves, selected_index
    player = "X"
    board = ["", "", "", "", "", "", "", "", ""]
    player_moves = {"X": 0, "O": 0}
    selected_index = None
    for button in buttons:
        button.config(text="", state=tk.NORMAL)

def move_piece(idx):
    global selected_index, player
    if selected_index is not None:
        if board[idx] == "" and abs(idx - selected_index) in [1, 3]:  # Validasi gerakan
            buttons[selected_index].config(text="")
            board[selected_index] = ""
            buttons[idx].config(text=player)
            board[idx] = player
            selected_index = None
            if check_winner():
                messagebox.showinfo("Tic-Tac-Toe", f"Pemain {player} menang!")
                reset_game()
            else:
                player = "O" if player == "X" else "X"
        else:
            messagebox.showinfo("Tic-Tac-Toe", "Gerakan tidak valid!")
            selected_index = None

def button_click(idx):
    global player, player_moves, selected_index
    if player_moves[player] < 3:  
        if board[idx] == "":
            buttons[idx].config(text=player)
            board[idx] = player
            player_moves[player] += 1
            if check_winner():
                messagebox.showinfo("Tic-Tac-Toe", f"Pemain {player} menang!")
                reset_game()
            else:
                player = "O" if player == "X" else "X"
        else:
            messagebox.showinfo("Tic-Tac-Toe", "Kotak sudah terisi!")
    else:  # Memindahkan bidak
        if board[idx] == player:  # Memilih bidak untuk dipindahkan
            selected_index = idx
        elif selected_index is not None:  # Memindahkan bidak
            move_piece(idx)

buttons = []
for i in range(9):
    button = tk.Button(root, text="", font=("Helvetica", 20), width=5, height=2, command=lambda i=i: button_click(i))
    button.grid(row=i//3, column=i%3)
    buttons.append(button)

root.mainloop()
