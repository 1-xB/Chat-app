import random
from tkinter import Tk, Frame, Scrollbar, Label, Listbox, Entry, Button, messagebox, Text
import socket
import threading
import datetime
import pyodbc


def database():
    def login_t():
        login()

    def login():
        username = username_entry.get()
        password = password_entry.get()
        login_button.config(text="Logowanie...", bg='grey', state='disabled')
        base.update()
        try:
            conn = pyodbc.connect('Driver={SQL SERVER};' +
                                  'Server=192.168.0.131,1433;' +
                                  'Database=app;' +
                                  'Trusted_Connection=no;')
            conn.autocommit = True
            cursor = conn.cursor()
            cursor.execute(
                f"SELECT * FROM users WHERE Username = '{username}' AND PasswordHash COLLATE Latin1_General_CS_AS = '{password}'")

            if cursor.fetchone():

                messagebox.showinfo("Success", "Zalogowano pomyślnie!")
                base.destroy()
                main()

            else:
                messagebox.showerror("Error", "Błędny login lub hasło!")
                login_button.config(text="Zaloguj", bg="#4CAF50", state='normal')

            cursor.close()
            conn.close()
        except Exception as e:
            print(e)

    base = Tk()
    base.title("Login")
    base.geometry("400x250")
    base.configure(bg="#f0f0f0")

    title_label = Label(base, text="Logowanie", font=("Arial", 24), bg="#f0f0f0")
    title_label.pack(pady=10)

    # Pole na nazwę użytkownika
    username_frame = Frame(base, bg="#f0f0f0")
    username_frame.pack(pady=5)
    Label(username_frame, text="Login:", bg="#f0f0f0", font=("Arial", 12)).pack(side='left')
    username_entry = Entry(username_frame, font=("Arial", 12))
    username_entry.pack(side='right')

    # Pole na hasło
    password_frame = Frame(base, bg="#f0f0f0")
    password_frame.pack(pady=5)
    Label(password_frame, text="Hasło:", bg="#f0f0f0", font=("Arial", 12)).pack(side='left')
    password_entry = Entry(password_frame, show="*", font=("Arial", 12))
    password_entry.pack(side='right')

    # Przycisk logowania
    login_button = Button(base, text="Zaloguj", font=("Arial", 12), command=login_t, bg="#4CAF50", fg="white", padx=20,
                          pady=5)
    login_button.pack(pady=10)

    # Pole do wyświetlania statusu logowania
    login_status = Label(base, text="", font=("Arial", 12), bg="#f0f0f0")
    login_status.pack()

    base.mainloop()


def main():
    global client_socket, is_Connected
    is_Connected = False
    users_color = {}
    colors = ["#000000", "#ff4125", "#ff11ac", "#3c51ff", "#6f2aff", "#ff886a",
              "#00ff00", "#ff00ff", "#00ffff", "#800080", "#008000",
              "#0000ff", "#ff0000", "#008080", "#800000", "#808000", "#808080",
              "#c0c0c0", "#808080", "#ff7f00", "#dda0dd", "#b0e0e6",
              "#ff1493", "#48d1cc", "#1e90ff", "#add8e6", "#20b2aa", "#87ceeb",
              "#191970", "#dc143c", "#8b0000", "#5f9ea0", "#32cd32", "#00ff7f",
              "#ff4500", "#8a2be2", "#4b0082", "#d2691e", "#ff8c00", "#d2b48c",
              "#ff6347", "#800000", "#2e8b57", "#ff69b4", "#4682b4", "#00ced1",
              "#663399", "#da70d6", "#ff00ff", "#800080", "#ffb6c1", "#b0c4de",
              "#00FF00", "#228B22", "#006400", "#ADFF2F", "#7FFF00", "#00FF7F",
              "#FF0000", "#00FFFF", "#FF00FF", "#FFA500", "#FFD700", "#8A2BE2",
              "#FF6347", "#1E90FF", "#FF4500", "#800000", "#8B0000", "#B22222",
              "#FF69B4", "#FFC0CB", "#FF7F50", "#FF8C00", "#FFD700", "#DAA520",
              "#B8860B", "#32CD32", "#008000", "#228B22", "#006400", "#ADFF2F",
              "#7FFF00", "#00FF7F", "#00FF00", "#FFA500", "#FFD700",
              "#8A2BE2", "#FF6347", "#1E90FF", "#FF4500", "#800000", "#8B0000",
              "#B22222", "#FF0000", "#DC143C", "#FF69B4", "#FFC0CB", "#FF7F50",
              "#FF8C00", "#FFD700", "#DAA520", "#B8860B", "#32CD32", "#008000",
              "#228B22", "#006400", "#ADFF2F", "#7FFF00", "#00FF7F"
              ]

    def on_closing():
        try:
            client_socket.close()
            root.destroy()
        except:
            root.destroy()

    def time_():
        czas = datetime.datetime.now()
        time_label.config(text=czas.strftime("%H:%M"))
        root.after(1000, time_)

    def disconnect():
        global is_Connected, client_socket
        print('disconnecting')
        if is_Connected:
            chat_listbox.delete(0, 'end')
            usernames_listbox.config(state='normal')
            usernames_listbox.delete(1.0, 'end')
            usernames_listbox.config(state='disabled')
            user_listbox.delete(0, 'end')

            client_socket.close()
            connection_info.config(text="DISCONNECTED", fg="red")
            username_entry.config(state='normal')
            messagebox.showinfo("Disconnected from server", "You have been disconnected from the server")

        else:
            messagebox.showerror("Error", "Please connect first!")

    def send(event=None):
        global client_socket, is_Connected
        if is_Connected:
            message = f"{username_entry.get()}: {message_entry.get()}"
            if not message_entry.get().isspace() and message_entry.get():
                #chat_listbox.insert('end', f"{username_entry.get()}: {message}")
                client_socket.send(message.encode('utf-8'))
                message_entry.delete(0, 'end')
            else:
                messagebox.showinfo("Error", "Type Something!")
        else:
            messagebox.showerror("Error", "Please connect first!")

    def connect_th():
        chat_listbox.delete(0, 'end')
        threading.Thread(target=connect).start()

    def connect():
        global is_Connected, client_socket
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            host = '192.168.0.139'
            port = 12345
            if username_entry.get():
                users_color[username_entry.get()] = random.choice(colors)

                connection_info.config(text="CONNECTING...", fg="gray")
                client_socket.connect((host, port))
                client_socket.send(username_entry.get().encode())
                user_listbox.insert('end', f"{username_entry.get()}")
                is_Connected = True

                connection_info.config(text="CONNECTED", fg="green")
                messagebox.showinfo("Connected to server", "You have been connected to the server")

                messages_th(client_socket)
                username_entry.config(state='disabled')
            else:
                messagebox.showerror("Error", "Please enter a username!")
                connection_info.config(text="NOT CONNECTED", fg="red")
        except Exception as e:
            connection_info.config(text="NOT CONNECTED", fg="red")
            messagebox.showerror("Error", "Something went wrong. Please try again later. \n Error:" + str(e))


    def messages_th(client_socket):
        receive_thread = threading.Thread(target=receive_message, args=(client_socket,))
        receive_thread.start()

    def receive_message(client_socket):
        while True:
            try:
                received_data = client_socket.recv(1024)
                data = received_data.decode()
                if ':' in data:
                    data = data.split(':', 1)
                    usernames_listbox.config(state='normal')
                    usernames_listbox.tag_configure(users_color[data[0]], foreground=users_color[data[0]])
                    usernames_listbox.insert('end', data[0] + ":" + '\n', users_color[data[0]])
                    print(users_color[data[0]])
                    usernames_listbox.config(state='disabled')
                    if len(data[1]) > 30:
                        times = len(data[1]) // 48
                        for i in range(times):
                            chat_listbox.insert('end', data[1][i * 48:(i + 1) * 48] + '\n')
                            usernames_listbox.config(state='normal')
                            usernames_listbox.insert('end', '\n')
                            usernames_listbox.config(state='disabled')
                    else:
                        chat_listbox.insert('end', data[1])

                else:
                    if '-delete-' not in data:

                        for i in data.split(','):
                            if i != username_entry.get() and i not in user_listbox.get(0, 'end'):
                                users_color[i] = random.choice(colors)
                                user_listbox.insert('end', i)
                    if '-delete-' in data:
                        print('usuwam!')
                        print(data[8:])
                        user_listbox.delete(user_listbox.get(0, 'end').index(data[9:]))
            except Exception as e:
                print("Błąd:", e)
                break

    global sock, chat_listbox, message_entry, username_entry

    root = Tk()
    root.title("Chat App")
    root.resizable(False, False)
    root.geometry("900x500")

    bg_color = "#f0f0f0"
    button_color = "#4CAF50"
    button_text_color = "white"

    root.configure(bg=bg_color)

    frame_menu = Frame(root, bg=bg_color, bd=10)
    frame_menu.pack(side='left', fill='y')

    frame_chat = Frame(root, bg=bg_color, bd=10)
    frame_chat.pack(expand=True, fill='both')

    frame_notes = Frame(root, bg=bg_color, bd=10)
    frame_notes.pack(side='right', fill='y')

    Label(frame_menu, text="Connection Menu:", bg=bg_color, fg="blue", font=("Arial", 12, "bold")).pack(side='top',
                                                                                                        padx=5, pady=5)
    connect_button = Button(frame_menu, text="Connect", command=connect_th, bg=button_color, fg=button_text_color,
                            font=("Arial", 10, "bold"))
    connect_button.pack(padx=5, pady=5)
    disconnect_button = Button(frame_menu, text="Disconnect", command=disconnect, bg=button_color, fg=button_text_color,
                               font=("Arial", 10, "bold"))
    disconnect_button.pack(padx=5, pady=5)
    Label(frame_menu, text="Username:", bg=bg_color, fg="blue", font=("Arial", 12, "bold")).pack(padx=5, pady=5)
    username_entry = Entry(frame_menu, width=20)
    username_entry.pack(padx=5, pady=5)

    Label(frame_chat, text="Chat:", bg=bg_color, fg="blue", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=5, )

    chat = Frame(frame_chat, bg=bg_color, bd=10)
    chat.grid(row=1, column=0)
    usernames_listbox = Text(chat, height=19, width=16,font=("Arial", 12), state='disabled')
    usernames_listbox.grid(row=0, column=0, padx=(5, 0), sticky='e')
    #usernames_listbox = ttk.Treeview(chat, height=16)
    #usernames_listbox.grid(row=0, column=0, padx=(5, 0), sticky='e')
    #usernames_listbox.column("#0", width=110)

    chat_listbox = Listbox(chat, height=18, width=40, font=("Arial", 12))
    chat_listbox.grid(row=0, column=1, padx=(0, 5), sticky='w')

    scrollbar = Scrollbar(chat, command=lambda *args: (chat_listbox.yview(*args), usernames_listbox.yview(*args)))
    scrollbar.grid(row=0, column=2, sticky='ns')
    chat_listbox.config(yscrollcommand=scrollbar.set)
    usernames_listbox.config(yscrollcommand=scrollbar.set)

    Label(frame_chat, text="Message:", bg=bg_color, fg="blue", font=("Arial", 12, "bold")).grid(row=2, column=0, padx=5,
                                                                                                pady=5, sticky="w")
    message_entry = Entry(frame_chat, width=60)
    message_entry.grid(row=3, column=0, padx=5, sticky="w")
    send_button = Button(frame_chat, text="Send", command=send, bg=button_color, fg=button_text_color,
                         font=("Arial", 10, "bold"))
    send_button.place(x=400, y=420)

    message_entry.bind("<Return>", send)

    connection_info = Label(frame_chat, text="NOT CONNECTED", fg="red", font=("Arial", 20, "bold"))
    connection_info.place(x=140, y=1)

    time_label = Label(frame_chat, text="Time", font=("Arial", 20))
    time_label.place(x=560, y=1)

    user_listbox = Listbox(frame_chat, height=18, width=12, font=("Arial", 12))
    user_listbox.place(x=550, y=35)

    time_()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


if __name__ == "__main__":
    database()
