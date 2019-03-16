'''
- add user
- update user privilege
- remove user privilege
'''

from Tkinter import *

master = Tk()
master.title("Master Reader")

frame = Frame(master, height = 1000, width = 1000)
frame.pack()

def add_user():
	global frame
	print("Adding user")
	frame.destroy()
	frame2 = Frame(master, height = 1000, width = 1000)
	frame2.pack()

	cancle_button = Button(frame2, text = "Cancle", command = master.destroy())
	cancle_button.pack()

def update_user_privilege():
	print("Updating user privilege")

def remove_user_privilege():
	print("Removing user privilege")

def cancle():
	master.destroy()

add_user_button = Button(frame, text = "Add user", command = add_user)
add_user_button.pack()

update_user_privilege_button = Button(frame, text = "Update user privilege", command = update_user_privilege)
update_user_privilege_button.pack()

remove_user_privilege_button = Button(frame, text = "Remove user privilege", command = remove_user_privilege)
remove_user_privilege_button.pack()

cancle_button = Button(frame, text = "Cancle", command = cancle)
cancle_button.pack()

master.mainloop()
