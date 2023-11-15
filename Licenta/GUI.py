from tkinter import *
from Captura import *
from threading import *

lista_pachete = []
dictionar_final = {}
c = Captura()

def threading_manual():
    t1 = Thread(target=c.capture, args=(lista_pachete, dictionar_final, entry_nr_pachete.get(), entry_interfata.get(), entry_filtru.get()))
    t1.start()

def threading_automat():
    t2 = Thread(target=c.rulare_automata, args=(lista_pachete, dictionar_final, entry_nr_pachete.get(), entry_path.get(), entry_IP_server.get(), entry_user_ftp.get(), entry_parola_ftp.get(), entry_interfata.get(), entry_filtru.get()))
    t2.start()

root = Tk()
root.title("Proiect capturare de pachete și detecție de DoS")
root.geometry("450x510")

label_interfata = Label(text='Interfață',
              font=("Calibri Bold",12),
              bg="#F0F0F0",
              fg="black",
              width=14,
              height=1
              )
label_interfata.grid(row=0, column=0)

entry_interfata = Entry(bg='white', fg='black')
entry_interfata.grid(row=0, column=1)

label_filtru = Label(text='Filtru',
              font=("Calibri Bold", 12),
              bg="#F0F0F0",
              fg="black",
              width=14,
              height=1
              )
label_filtru.grid(row=1, column=0)

entry_filtru = Entry(bg='white',fg='black')
entry_filtru.grid(row=1, column=1)

label_nr_pachete = Label(text='Număr Pachete',
              font=("Calibri Bold", 12),
              bg="#F0F0F0",
              fg="black",
              width=14,
              height=1
              )

label_nr_pachete.grid(row=2, column=0)

entry_nr_pachete = Entry(bg='white',fg='black')
entry_nr_pachete.grid(row=2, column=1)


buton_captura = Button(root,
           command = threading_manual,
           text='Start captură',
           font=("Arial Bold",14),
           bg="#33C9FF",
           fg="black",
           width=17,
           height=2
           )
buton_captura.grid(row=3,column=1)

label_path = Label(text='Cale Director',
              font=("Calibri Bold", 12),
              bg="#F0F0F0",
              fg="black",
              width=14,
              height=1
              )
label_path.grid(row=5,column=0)

entry_path = Entry(bg='white', fg='black')
entry_path.grid(row=5,column=1)

buton_save = Button(root,
                command = lambda: c.save(lista_pachete, dictionar_final, entry_path.get()),
                text='Salvare date local',
                font=("Arial Bold",14),
                bg="yellow",
                fg="purple",
                width=17,
                height=2)
buton_save.grid(row=6,column=1)

buton_statistics = Button(root,
                command = lambda: c.show_stats(lista_pachete),
                text='Afișare statistici',
                font=("Arial Bold",14),
                bg="orange",
                fg="blue",
                width=17,
                height=2)
buton_statistics.grid(row=4,column=1)

######
label_IP_server = Label(text='IP Server',
              font=("Calibri Bold", 12),
              bg="#F0F0F0",
              fg="black",
              width=14,
              height=1
              )

label_IP_server.grid(row=7, column=0)

entry_IP_server = Entry(bg='white',fg='black')

entry_IP_server.insert(END, '192.168.8.128')

entry_IP_server.grid(row=7, column=1)

label_user_ftp = Label(text='Username FTP',
              font=("Calibri Bold", 12),
              bg="#F0F0F0",
              fg="black",
              width=14,
              height=1
              )

label_user_ftp.grid(row=8, column=0)

entry_user_ftp = Entry(bg='white',fg='black')

entry_user_ftp.insert(END, 'Eduard')

entry_user_ftp.grid(row=8, column=1)

label_parola_ftp = Label(text='Parolă FTP',
              font=("Calibri Bold", 12),
              bg="#F0F0F0",
              fg="black",
              width=14,
              height=1
              )

label_parola_ftp.grid(row=9, column=0)

entry_parola_ftp = Entry(show="*", bg='white', fg='black')

entry_parola_ftp.insert(END, 'Licenta12!')

entry_parola_ftp.grid(row=9, column=1)

buton_ftp = Button(root,
                command = lambda: c.ftp_transfer(entry_IP_server.get(), entry_user_ftp.get(), entry_parola_ftp.get(), entry_path.get()),
                text='Transfer FTP',
                font=("Arial Bold",14),
                bg="pink",
                fg="green",
                width=17,
                height=2)

buton_ftp.grid(row=10, column=1)

buton_all = Button(root,
                command=threading_automat,
                text='Rulare automata',
                font=("Arial Bold",14),
                bg="brown",
                fg="white",
                width=17,
                height=2)

buton_all.grid(row=11, column=1)

buton_start = Button(root, command=c.pornire_rulare, text="Start")
buton_start.grid(row=12, column=0)

buton_stop = Button(root, command=c.oprire_rulare, text="Stop")
buton_stop.grid(row=12, column=1)

buton_test = Button(root, command=c.test_DoS, text="Test DoS")
buton_test.grid(row=12, column=2)

root.mainloop()
