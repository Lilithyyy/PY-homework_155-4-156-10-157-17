#IMPORT LIBS
import tkinter as tk 
import random

#initialize a file to record moves
record_moves = open("NIMgame_record.txt", "w")
record_moves.write("")
record_moves.close()

#setup startup window to configure the game
def SETUP(): 
    global matches_entry, root, c, START_button, matches_entry, players, current_player
    players = (1, 2)
    current_player = random.choice(players)

    w = 400
    h = 200

    #set window properties
    root = tk.Tk()
    root.title("SETUP")
    root.resizable(False, False)
    root.geometry(f"{w}x{h}")

    c = tk.Canvas(root, width=w, height=h, bg="#c3b1db")
    c.pack()

    c.create_text(w//2, 40, text="How many matches do you want to play with?", fill = "black", font="Arial 10 bold", anchor="center")

    #create entries and buttons for confirmation
    matches_entry = tk.Entry(c, width = 50)
    matches_entry.place(x=w//2, y=60, anchor="n")

    START_button = tk.Button(c, text="START", width=20, height=2, bg="#7e5c8d", fg="white", font=("Arial", 10, "bold"), command=lambda: StartGame())
    START_button.place(x=w//2, y=100, anchor="n")

def StartGame():
    global root, amount, w, h, TURN_Button, matches, gap, box_width, moves_left, first_time

    #error handling for non-int inputs and resetting the setup if so
    try:
        amount = int(matches_entry.get())
        
    except ValueError:
        SETUP()
        return
    
    #destroy previous widgets for a clean start
    c.delete("all")
    matches_entry.destroy()
    START_button.destroy()

    gap = 5
    box_width = 20
    w = amount * box_width + (amount * gap * 2)
    h = 200
    matches = amount * [1, ]
    moves_left = 3
    first_time = True

    #change window properties
    root.title("NIM")
    root.protocol("WM_DELETE_WINDOW", on_close) #prevents any errors after closing the window
    root.resizable(False, False)
    root.geometry(f"{w}x{h}")
    c.config(width = w, height = h)

    #draw matches
    for i in range(amount):
        x = i * (box_width + gap * 2) + gap + box_width // 2
        y = h // 2
        
        if matches[i] == 1:
            DrawMatch(x, y, f"match{i}")
    
    #set initial turn
    SwitchTurns()
    first_time = False

    #make an end turn button so the player can end their turn even before using all their moves
    TURN_Button = tk.Button(c, text="END TURN", width=20, bg = "#7e5c8d", fg="white", font=("Arial", 10, "bold"), command=lambda: SwitchTurns())
    TURN_Button.place(x=w//2, y=h-40, anchor="center")

#define function for drawing matches and binding them to a click event
def DrawMatch(x, y, matchtag):
    c.create_rectangle(x-2, y-15, x+2, y+15, fill="#AC8E76", outline="black", tag = matchtag)
    c.create_oval(x-5, y-15, x+5, y-5, fill="#8B5E3C", outline="black", tag = matchtag)
    c.tag_bind(matchtag, "<Button-1>", on_match_click)

#define function for when a match is clicked (using the tagging system)
def on_match_click(event):
    global moves_left
    matchtag = c.gettags("current")[0]  # Get the tag of the clicked item
    print(f"Player {current_player} clicked on {matchtag}")

    #take care of turn logic
    if moves_left > 0:

        #remove match from canvas
        c.delete(matchtag) 
        moves_left -= 1

        #update matches list to show that the match has been taken
        matches[int(matchtag.replace("match", ""))] = 0

        amount_left = sum(matches)

        record_moves = open("NIMgame_record.txt", "a")
        #add who made the move on every other line
        record_moves.write(str(current_player) + "\n")

        #record moves in the text files
        record_moves.write(str(matches) + "\n")

        if amount_left == 0:
            end_game(current_player)
            record_moves.close()
            return

    else:
        print("No moves left this turn!")

#define function for switching turns
def SwitchTurns():
    global current_player, moves_left

    if moves_left < 3: #prevents the player from switching turns without making a move
        c.delete("turn")

        moves_left = 3
        current_player += 1

        if current_player > players[len(players)-1]:
            current_player = players[0]

        c.create_text(w//2, 20, text = f"It's Player {current_player}'s turn!", fill="black", font="Arial 10 bold", anchor="center", tag="turn")

    elif first_time: #prevents the warning from showing on start
        c.create_text(w//2, 20, text = f"It's Player {current_player}'s turn!", fill="black", font="Arial 10 bold", anchor="center", tag="turn")
        
    else:
        c.create_text(w//2, h-65, text = "you need to make a move first!", fill="red", font = "Arial 10", anchor="center", tag="move_warning")
        c.after(1000, lambda: c.delete("move_warning"))

def on_close(): #prevents errors on closing the window
    root.destroy()

#final screen for an option to replay
def end_game(loser):
    global REPLAY_button

    c.delete("all")
    TURN_Button.destroy()
    c.create_text(w//2, h//2, text = f"Player {loser} loses!", fill="#642D2D", font="Arial 15 bold", anchor="center")

    c.create_text(w//2, h//2 + 30, text = "Would you like to watch a replay?", fill="black", font="Arial 10 bold", anchor="center")

    REPLAY_button = tk.Button(c, text="REPLAY", width=20, bg = "#7e5c8d", fg="white", font=("Arial", 10, "bold"), command=lambda: replay())
    REPLAY_button.place(x=w//2, y=h//2 + 60, anchor="center")

#replay function to watch how the game went
def replay():

    #destroys replay button
    REPLAY_button.destroy()

    #first, puts the text into a single string, then splits the lines upon meeting a \n in the text
    record_moves = open("NIMgame_record.txt", "r").read().splitlines()

    moves=[]

    #2 step - every other item in record_moves 
    for i in range(0, len(record_moves), 2):

        #retrieves the player from record_moves
        player = record_moves[i]

        #picks up the second line from record_moves that the 2 step doesn't touch and adds the steps to matches_state
        matches_state = [int(x) for x in record_moves[i+1].strip('[]').split(", ")]

        #inserts the information into a clean list
        moves.append((player, matches_state))

        #if step equals more than the moves list has items, stop the code
        def replay_step(step=0):
            if step >= len(moves):

                c.delete('all')
                c.create_text(w//2, h//2, text = "Replay is finished!", fill = "black", font= "Arial 25 bold", anchor="center")

                return
            
            player, matchmove = moves[step]

            c.delete('all') 

            for i in range(len(matchmove)):

                if matchmove[i] == 1:
                    x = i * (box_width + gap * 2) + gap + box_width // 2
                    y = h//2
                    DrawMatch(x,y, f"match{i}")
            
            c.create_text(w//2, 20, text = f"Player {player}'s move", fill="black", font="Arial 10 bold")

            #adds value to step so the function doesn't repeat with the same number, delays 500ms
            c.after(500, replay_step, step+1)

        replay_step()

SETUP()
root.mainloop()