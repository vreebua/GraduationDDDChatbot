# py for the user interface

#from logging import basicConfig
#from stat import FILE_ATTRIBUTE_REPARSE_POINT
# imports everthing from tkinter with star
from tkinter import *
#from turtle import width
from chat import get_response, bot_name

import random
import time

bottle_count = 0
active = False

jug_count = 0
active2 = False

knowledge_count = 0
social_count = 0

list = ["What motivates you to properly dispose of your plastic?", "Before meeting me, what was the main thing preventing you from properly disposing of plastic?"]


# defining of some colours
BG_GRAY = "#0CD096"
BG_COLOR = "#C4E8D9"
TEXT_COLOR = "#414A3C"

# and fonts
FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"

# create application
class ChatApplication:

    def __init__(self):

        # just the top level widget
        self.window = Tk()        
        # create the layout
        self._setup_main_window()

    # for running the application
    def run(self):
        # must call this in tk inter to start the application
        self.window.mainloop()

    # the helper function, that sets up main window
    def _setup_main_window(self):
        self.window.title("Plastibot")
        # do not want window to be resizeable
        self.window.resizable(width=False, height=False)
        # helps with giving widgets different attributes, bg is background
        self.window.configure(width=470, height=550, bg=BG_COLOR)

            
        # define layout
        # head label, from tk inter, fg is foreground colour
        head_label = Label(self.window, bg=BG_COLOR, fg=TEXT_COLOR,
                            text="Laura the chatbot", font=FONT_BOLD, pady=10)
        # must be between 0 and 1
        head_label.place(relwidth=1)

        # tiny divider, 450 gives some spacing
        line = Label(self.window, width=450, bg=BG_GRAY)
        line.place(relwidth=1, rely=0.07, relheight=0.012)

        # text widget, display text, also with tk inter
        # every text will display 20 characters in 1 line, two lines for it, and padding around
        # self is being used cause it needs to be used for later also
        self.text_widget = Text(self.window, width=20, height=2, bg=BG_COLOR, fg=TEXT_COLOR,
                                font=FONT, padx=5, pady=5)

        # 0.745 means it will take a huge chunk from the application, 75%, and whole width is used
        self.text_widget.place(relheight=0.745, relwidth=1, rely=0.08)

        # make a cursor, from tk library
        self.text_widget.configure(cursor="arrow", state=DISABLED)


        # scroll bar, also tk
        scrollbar = Scrollbar(self.text_widget)
        # take whole height of widget, 0.974 means it is at the right
        scrollbar.place(relheight=1, relx=0.974)
        # when scrollbar is used, it will change y position of the text widget
        scrollbar.configure(command=self.text_widget.yview)


        # bottom label
        bottom_label = Label(self.window, bg=BG_GRAY, height=80)
        bottom_label.place(relwidth=1, rely=0.825)


        # message entry box, also tk, instead of self use bottom_label as parent widget
        self.msg_entry = Entry(bottom_label, bg="#FFFFFF", fg=TEXT_COLOR, font=FONT)
        self.msg_entry.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)
        # whenever application starts, this is already in focus, so typing can begin
        self.msg_entry.focus()
        # whenever enter is hit, send text
        self.msg_entry.bind("<Return>", self._on_enter_pressed)


        # send button
        send_button = Button(bottom_label, text="Send", font=FONT_BOLD, width=20, bg=BG_GRAY,
                                # connect text to widget when when button is pressed
                                command=lambda: self._on_enter_pressed(None))
        # place the button
        send_button.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)


        # first text above
        msg3 = f"{bot_name}: ""Hi! Good to see you! What kind of plastic item would you like to discard? Please mention the name and amount" "\n\n"
            #msg3 = f"{bot_name}: {get_response(msg)}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg3)
        self.text_widget.configure(state=DISABLED)







    # define on enter pressed from above
    def _on_enter_pressed(self, event):
        # will get input text as a string
        msg = self.msg_entry.get()

        # call insert message
        self._insert_message(msg, "You")


    def _insert_message(self, msg, sender):
        # for if enter is pressed without text in it
        if not msg:
            return

        # delete text from entry box, when send
        self.msg_entry.delete(0, END)
        # message that want to display, \n means empty line below text message
        msg1 = f"{sender}: {msg}\n\n"
        # put it in the correct widget, self.text widget
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg1)
        # after inserting message, make field again disabled
        self.text_widget.configure(state=DISABLED)


        # make it so the chatbot respond
        # copy paste from above and adjust to chatbot, bot_name, get_response from other py files
        msg2 = f"{bot_name}: {get_response(msg)}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg2)
        self.text_widget.configure(state=DISABLED)

        # function to help remember what items the user had
        # only worked out with the items "plastic bottle" and "milk jug", to give as example
        def anouk(word, amount, number):
            if word in msg:
                global bottle_count
                global jug_count
                global active
                global active2

                if word == "bottle" or word == "bottles":
                    if amount in msg:
                        # if bottle is mentioned, look at the count, and add that number to count variable made above
                        bottle_count = bottle_count + number

                        msg5 = f"{bot_name}: ""Plastic bottles can also be returned for a deposit to supermarkets." "\n\n"
                        self.text_widget.configure(state=NORMAL)
                        self.text_widget.insert(END, msg5)
                        self.text_widget.configure(state=DISABLED)
                
                        print("bottle count:", bottle_count)

                        # if count goes over a specific number, it unlocks the "plastic bottle" button for faster process
                        if bottle_count > 10 and active == False and bottle_count > jug_count:
                            # send message to user about the new function
                            msg3 = f"{bot_name}: ""For the plastic bottle, a button has been activated. To complete the process quickly, simply click this button *type button* for as many plastic bottles as you have." "\n\n"
                            #msg3 = f"{bot_name}: {get_response(msg)}\n\n"
                            self.text_widget.configure(state=NORMAL)
                            self.text_widget.insert(END, msg3)
                            self.text_widget.configure(state=DISABLED)
                            active = True
                            active2 = False
                
                # repeat with other word
                if word == "jug" or word == "jugs":
                    if amount in msg:
                        jug_count = jug_count + number
                
                        print("jug count:", jug_count)

                        # only the biggest counts can buttons, so if jugs becomes bigger it will replace the other
                        if jug_count > 10 and active2 == False and jug_count > bottle_count:
                            msg3 = f"{bot_name}: ""You have unlocked fast travel for the milk jugs. Simply press this button as many times as the items you have, or type button2, to quickly go through the process" "\n\n"
                            self.text_widget.configure(state=NORMAL)
                            self.text_widget.insert(END, msg3)
                            self.text_widget.configure(state=DISABLED)
                            active2 = True
                            active = False

        # examples of what the user could say                
        anouk("bottle", "1", 1)
        anouk("bottle", "one", 1)
        anouk("bottles", "2", 2)
        anouk("bottles", "two", 2)
        anouk("bottles", "3", 3)
        anouk("bottles", "three", 3)
        anouk("bottles", "4", 4)
        anouk("bottles", "four", 4)
        anouk("bottles", "5", 5)
        anouk("bottles", "five", 5)
        anouk("button", "button", 1)
        anouk("bottles", "6", 6)
        anouk("bottle", "six", 6)
        anouk("jug", "1", 1)
        anouk("jug", "one", 1)
        anouk("jugs", "2", 2)
        anouk("jugs", "two", 2)
        anouk("jugs", "3", 3)
        anouk("jugs", "three", 3)
        anouk("jugs", "4", 4)
        anouk("jugs", "four", 4)
        anouk("jugs", "5", 5)
        anouk("jugs", "five", 5)
        anouk("button2", "button2", 1)
        


        # if statement that detects if disposing session is over
        # should be more goodbye words, see intents
        if "bye" in msg1 or "that was all" in msg1 or "adios" in msg1 or "Byeee!" in msg1:

            # after some time has passed, the chatbot will want to ask the user something personal            
            msg4 = f"{bot_name}: ""**after some time has passed, a notificaton arises a personal question**" "\n\n"
            self.text_widget.configure(state=NORMAL)
            self.text_widget.insert(END, msg4)
            self.text_widget.configure(state=DISABLED)

            # a random personal question will be chosen
            chosen_one = random.choice(list)

            msg2 = f"{bot_name}: {chosen_one}\n\n"
            self.text_widget.configure(state=NORMAL)
            self.text_widget.insert(END, msg2)
            self.text_widget.configure(state=DISABLED)

            def anouk2(whatquestion, addquestion):
            
                # question will be replaced when asked
                if chosen_one == whatquestion:
                    list.remove(whatquestion)
                    list.append(addquestion)
                    print(list)

            # first question, replaced question
            anouk2("What motivates you to properly dispose of your plastic?", "Have you developed any new motivations to help dispose of your plastic?")
            anouk2("Before meeting me, what was the main thing preventing you from properly disposing of plastic?", "Do you recall any further limiting factors in the past that kept you from recycling?")

        
        # function for gamification methods
        def anouk2(word):
            # if the user mentions a word that can be related to a TPB element, this function will activate
            if word in msg:
                global knowledge_count
                global social_count
                
                # for instance, the word knowledge
                if word == "knowledge":
                    knowledge_count = knowledge_count + 1

                    # for this example, narrative will be the first gamification, therefore set as 1
                    if knowledge_count == 1:
                        # tell the user about the change
                        msg3 = f"{bot_name}: ""I have activated the badges gamification method on your homepage!" "\n\n"
                        self.text_widget.configure(state=NORMAL)
                        self.text_widget.insert(END, msg3)
                        self.text_widget.configure(state=DISABLED)
                        knowledge_count = knowledge_count + 1

                if word == "social":
                    social_count = social_count + 1

                    # normally gamification activates after some answers have been given
                    if social_count == 3:
                        msg3 = f"{bot_name}: ""I have activated the teams gamification method on your homepage!" "\n\n"
                        self.text_widget.configure(state=NORMAL)
                        self.text_widget.insert(END, msg3)
                        self.text_widget.configure(state=DISABLED)
                        social_count = social_count + 1

        anouk2("knowledge")
        anouk2("social")



        # it will always scroll to the end, so last message can always be seen
        self.text_widget.see(END)






# creating of app / screen, and letting it run
if __name__ == "__main__":
    app = ChatApplication()
    app.run()