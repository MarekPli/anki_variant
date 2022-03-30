import copy
import sys
import ctypes
import tkinter as tk
import random
import re
dict_has = {}
was_has = []
SIZE = 20
MAX_BOX = 5
MAX_BOX_SEQUENCE = 1
list_index = -1
list_min = 0
count_max = 100
cycle = 0
sequence = False
idx_sequence = 0
trying = True
frame_idx = 0
list_has = []
code = 'cp1250'
fname_txt = 'ang_p.txt'  # 'u_ang_p.wyn'
fname_was = 'ang_w.txt'  # 'u_ang_p.yyy'
fname_zzz = 'ang_z.txt'  # 'u_ang_p.zzz'


def framedLabel(win, text="", font_size=18, height=4):
    fr = tk.Frame(win)
    fr.pack(fill='x')
    r = tk.Label(fr, font=("Times", font_size), height=height)
    if text:
        r.configure(text=text)
    r.pack(fill='x')
    return r


def framedText(win):
    answer = tk.Text(win, wrap='word', font=('Times', 18), height=10)
    tag_create(answer)
    answer.pack(fill='x')
    return answer


def font_delete():
    ctypes.windll.gdi32.RemoveFontResourceW('fonts_w.ttf')


def tag_create(text):
    ff = '#%02x%02x%02x'
    text.tag_configure('origin', font=('Times', 18),
                       foreground=ff % (0, 0, 0))
    text.tag_configure('f', font=('Times', 18), foreground=ff % (128, 0, 0))
    text.tag_configure('j', font=('Times', 18, 'italic'),
                       foreground=ff % (30, 30, 30))
    text.tag_configure('k', font=('Times', 18, 'italic'),
                       foreground=ff % (30, 30, 30))
    text.tag_configure('h', font=('Times', 18))
    # text.tag_configure('w', font=('WymowaAngielska', 16),
    #                    foreground=ff % (0, 100, 200))
    ww = 'WymowaAngielska'
    ww = 'Times'
    text.tag_configure('w', font=(ww, 16),
                       foreground=ff % (0, 100, 200))
    text.tag_configure('c', font=('Times', 18),
                       foreground=ff % (255, 255, 206))
    text.tag_configure('z', font=('Wingdings', 18),
                       foreground=ff % (0, 0, 128)
                       )
    text.tag_configure('small', font=('Times', 12),
                       )


def giveNext(q, a):

    q.configure(text="Naciśnięto")


def getHaslo(s):
    g = re.search('<h>(.+?)</h>', s)
    if not g:
        return None, None
    s = s[len(g.group())+1:]
    return g.group(1), s


def menu_get_list():
    getList()
    giveKeyExe()


def menu_get_list_f():
    global was_has, fname_was
    getList()
    appendToFile(fname_was)
    was_has = readFromFile(fname_was)
    giveKeyExe()


def giveKeyExe(seq=False):
    global question, answer, context, list_index, trying, cycle
    global sequence, idx_sequence
    sequence = seq
    list_index = -1
    trying = True
    cycle = 0
    giveKey('', question, answer, context)


def menu_kill_marked():
    global list_has, fname_zzz
    list_has = [x for x in list_has if x[1] == 0]
    appendToFile(fname_zzz, 'w')
    giveKeyExe()


def menu_get_list_all():
    global was_has, list_has
    list_has = copy.deepcopy(was_has)
    giveKeyExe()


def menu_all_sequence():
    global list_has, idx_sequence
    idx_sequence = 0
    list_has = getListPart()
    giveKeyExe(True)


def menu_last():
    global list_has, was_has, SIZE
    list_has = getListFromFile(was_has[-SIZE:], SIZE)
    giveKeyExe()


def menu_zzz():
    global list_has, fname_zzz
    list_has = readFromFile(fname_zzz)
    giveKeyExe()


def getList():
    global SIZE, dict_has, was_has, list_has
    list_has = []

    while len(list_has) < SIZE:
        has = random.choice(list(dict_has.keys()))

        if has and has not in list_has and [has, 0] not in was_has:
            list_has.append([has, 0])


def getListPart():
    global SIZE, was_has, idx_sequence, list_index
    idx = idx_sequence
    idx_sequence += SIZE
    list_index = 0
    return copy.deepcopy(was_has[idx:idx_sequence])


def getListFromFile(was_l, size):
    r = []
    if len(was_l) < size:
        size = len(was_l)
    for i in range(size):
        if was_l[i]:
            # if i in was_l:
            r.append(was_l[i])
    return r


def readFromFile(fname):
    fi2 = open(fname, 'r', encoding='utf8')
    text_file = fi2.read()
    fi2.close()
    listaX = text_file.split('\n')
    # list_has = list(map(lambda x: [x.split('|')[0], 0], listaX))
    return [[x.split('|')[0], 0] for x in listaX if x]


def appendToFile(fname, mode='a'):
    global list_has, was_has
    fo = open(fname, mode, encoding='utf8')
    for el in list_has:
        if el not in was_has or mode == 'w':
            fo.write(f"{el[0]}\n")
    fo.close()


def test_list(tab, i, min):
    # first elem if == min
    # pierwszy element równy min większy od i, czyli następny (bez już zrobionych)
    # lub pierwszy równy min (następny cykl)
    # lub -1 jeśli nie ma żadnego min
    r = -1
    for idx, t in enumerate(tab):
        if t[1] == min:
            if idx > i:
                return idx
            elif r < 0:
                r = idx
    return r


def giveKey(event, question, answer, context):
    global list_has, list_index, list_min, dict_has, trying, cycle
    global MAX_BOX, MAX_BOX_SEQUENCE
    global sequence, idx_sequence
    bkgfont = ('#eee', '#ddd', '#ccc', '#bbb', '#aaa', '#999')
    if type(event) == str:
        question.configure(text='')
        tagged(answer, '')
        trying = True
        return

    else:
        key = event.keysym.lower()
    if not trying and key == 't':
        return

    has = list_has[list_index][0]
    context.config(background=bkgfont[list_min])
    if trying:
        if key == 't':
            list_has[list_index][1] += 1
        list_idx_old = list_index
        # szukam pierwszego minimum po bieżącym (w cyklu)
        list_index = test_list(list_has, list_index, list_min)
        if list_idx_old >= list_index:  # next cycle
            cycle += 1
        if list_index < 0:  # nie ma już minimum na liście
            list_min = getListMin(list_has)
            if sequence and list_min == MAX_BOX_SEQUENCE:
                print("Przed zmianą", list_has)
                list_has = getListPart()
                list_min = 0
                print("Zmiana", list_has)
            else:
                random.shuffle(list_has)
                context.config(background=bkgfont[list_min])
                cycle = list_index = 0
                if list_min >= MAX_BOX:
                    context.configure(text='Koniec!')
                    list_min = MAX_BOX
                    return
        has = list_has[list_index][0]
        question.configure(text=has)
        tagged(answer, '')
        context.configure(text='')
    else:
        tagged(answer, dict_has[has])
        context.configure(
            text=f"Pudełko nr {list_min+1}. Jeśli znasz odpowiedź, naciśnij: t")

    trying = not trying
    question.focus_set()


def getListMin(list):
    r = list[0][1]
    for c in list:
        if r > c[1]:
            r = c[1]
    return r


def s_after_correct(txt):
    dict_w = {
        '~': chr(0xb8),
        '^': chr(0x283),
        '@': chr(0x259),
        '!': chr(0x25c),
        '#': chr(0xf0),
        '$': chr(0x3b8),
        '%': chr(0x19e),
        '&': chr(0x292),
        '*': f"({chr(0x36c)})",
        '0': chr(0x28c),
        '1': 'i',
        '2': chr(0x26a),
        '3': 'e',
        '4': chr(0xe6),
        '5': chr(0x251),
        '6': chr(0x251),
        '7': chr(0x254),
        '8': chr(0x28a),
        '9': 'u',

    }
    r = ''
    for c in txt:
        if c in dict_w:
            c = dict_w[c]
        r += c
    return r


def tagged(text, content):
    tag = 'origin'
    s = ''
    i = 0
    text.delete(1.0, 'end')

    while i < len(content):
        if content[i] == 'ž':
            # s += chr(ord(''))
            s += chr(61598)
            i += 1
            continue
        # if content[i:]
        if content[i:i+6] == "&#060;":
            text.insert('end', s, tag)
            text.insert('end', '<', 'small')
            s = ''
            i += 6
            continue
        if content[i:i+6] == "&#062;":
            text.insert('end', s, tag)
            text.insert('end', '>', 'small')
            s = ''
            i += 6
            continue

        if content[i] == '<':
            if tag == 'w':
                s = s_after_correct(s)
            text.insert('end', s, tag)
            s = ''
            if content[i+1] == '/':
                tag = 'origin'
                while content[i] != '>':
                    i += 1
            else:
                tag = ''
                i += 1
                while content[i] != '>':
                    tag += content[i]
                    i += 1
        else:
            s += content[i]
        i += 1
    if s:
        text.insert('end', s, 'origin')


def readAll():
    global fname_txt, code, dict_has
    dict_has = {}
    fi = open(fname_txt, 'r', encoding=code)
    text_file = fi.read()
    fi.close()
    lista = text_file.split('\n\n')
    for s in lista:
        q, a = getHaslo(s)
        dict_has[q] = a
    readAllZob()


def readAllZob():
    global dict_has
    count = 0
    for key, value in dict_has.items():
        if not value:
            continue
        g = re.search('zob.</j>', value)
        if g:
            m = g.end(0)
            g = re.search('<f>(.+?)</f>', value[m:])
            if g:
                zob = re.sub('<sup>', '^', g[1])
                zob = re.sub('<.+?>', '', zob)
                if zob in dict_has:
                    dict_has[key] += "\n\n===\n\n" + dict_has[zob]
                    count += 1
                # else:
                #     print(f"Brak: {key} {zob}")
    # print(f"Haseł typu zob: {count}")
    # print(len(dict_has.keys()))


def back_to_zero():
    global list_has
    for x in list_has:
        x[1] = 0
    giveKeyExe()


def getting_window():
    global list_has, dict_has, list_min, list_index, cycle
    minimized = 0
    m = tk.Toplevel()
    m.title("Informacja")
    tk.Label(m, text=f"Słów na liście: {len(list_has)}").pack()
    tk.Label(m, text=f"Słów wszystkich: {len(dict_has)}").pack()
    for el in list_has:
        if el[1] == list_min:
            minimized += 1
    tk.Label(
        m, text=f"Pudełko: {list_min+1}, zostało: {minimized}, zrobiono: {len(list_has)-minimized}").pack()
    tk.Label(
        m, text=f"Jesteśmy przy słowie {list_index+1} na liście, cykl {cycle+1}").pack()
    m.geometry('300x150+200+200')
    m.grab_set_global()

    tk.Button(m, text='Zamknij', command=lambda m=m: m.destroy()
              ).pack(side='bottom')


def choosing_window_explore(m, cb):
    global list_has
    # modify only if any is selected
    for x in cb:
        if x[1].get():
            list_has = [[el[0].cget('text'), 0] for el in cb if el[1].get()]
            giveKeyExe()
            break
    m.destroy()


def frame_show(frames, next=True):
    global frame_idx
    if frame_idx >= 0:
        frames[frame_idx].pack_forget()
    if next:
        frame_idx += 1
    else:
        if frame_idx > 0:
            frame_idx -= 1
    if frame_idx >= len(frames):
        frame_idx = len(frames)-1
    frames[frame_idx].pack(side='left')


def choosing_window():
    global list_has, dict_has, list_min, list_index, cycle, SIZE, frame_idx, count_max
    m = tk.Toplevel()
    m.title("Wybór ręczny")
    list_cb = []
    list_fr = []
    frameMain = tk.Frame(m)
    frameMain.pack()
    count = 0
    frame_idx = -1
    for el in list_has:
        if count % count_max == 0:
            frameListed = tk.Frame(frameMain)
            list_fr.append(frameListed)
        if count % SIZE == 0:
            frame = tk.Frame(frameListed)
            # list_fr.append(frame)
            frame.pack(side='left', anchor='n')
        count += 1
        var = tk.BooleanVar()
        # var.set(True)
        cb = tk.Checkbutton(frame, text=el[0], font=(10), variable=var)
        cb.pack(anchor='w')
        list_cb.append((cb, var))

    m.grab_set_global()
    frame = tk.Frame(m)
    frame.pack(fill='x')
    tk.Button(frame, text="<", border=5,
              command=lambda list_fr=list_fr: frame_show(list_fr, False)).pack(side='left', expand=True, fill='x')
    tk.Button(frame, text=">", border=5,
              command=lambda list_fr=list_fr: frame_show(list_fr)).pack(side='left', expand=True, fill='x')
    frame = tk.Frame(m)
    frame.pack(fill='x')
    tk.Button(frame, text='Anuluj', border=5, command=lambda m=m: m.destroy()
              ).pack(side='left', expand=True, fill='x')
    tk.Button(frame, text='OK', border=5, command=lambda list_cb=list_cb, m=m: choosing_window_explore(m, list_cb)
              ).pack(side='left', expand=True, fill='x')
    frame_show(list_fr)


def menu_chosen():
    global was_has, list_has, SIZE
    i = random.randint(0, len(was_has)-SIZE)
    # i = 30
    list_has = [x for x in was_has[i:i+SIZE]]
    giveKeyExe()
    # global question, answer, context
    # giveKey('', question, answer, context)


def prepare_menu(win):
    menubar = tk.Menu(win)
    win.config(menu=menubar)
    menu_options = tk.Menu(menubar, font=(18), tearoff=False)
    menu_options.add_command(label="Cofnij do zera",
                             command=back_to_zero, underline=0)
    menu_options.add_command(
        label="Informacje", command=getting_window, underline=0)
    menu_options.add_command(
        label="Wybór ręczny", command=choosing_window, underline=0)
    menu_options.add_command(label="Weź ostatnie",
                             command=menu_last, underline=0)
    menu_options.add_command(label="Weź nieznane",
                             command=menu_zzz, underline=0)
    menu_options.add_command(label="Losuj z wybranych",
                             command=menu_chosen, underline=0)
    menu_options.add_command(label="Losuj nowe",
                             command=menu_get_list, underline=1)
    menu_options.add_command(label="Losuj nowe z nagraniem",
                             command=menu_get_list_f, underline=2)
    menu_options.add_command(label="Całość dotychczasowych",
                             command=menu_get_list_all, underline=2)
    menu_options.add_command(label="Usuwanie znanych",
                             command=menu_kill_marked, underline=0)
    menu_options.add_command(label="Przegląd całości",
                             command=menu_all_sequence, underline=0)
    menu_options.add_command(label="Zakończ", command=sys.exit, underline=0)
    menubar.add_cascade(label="Opcje", menu=menu_options, underline=0)


# fontW = TTFont('fonts_w.ttf')
# ctypes.windll.gdi32.AddFontResourceW('fonts_w.ttf')
readAll()
was_has = readFromFile(fname_was)
root = tk.Tk()
root.title("Kartoteka autodydaktyczna")
root.geometry('800x430+200+200')

prepare_menu(root)
question = framedLabel(root)
answer = framedText(root)
answer.config(background='SystemButtonFace', relief='raised', padx=30)
context = framedLabel(root, "Naciśnij Enter żeby rozpocząć", 14, 3)

# list_has = getList(dict_has, was_has, SIZE)
list_has = getListFromFile(was_has[-SIZE:], SIZE)

# print(list(map(lambda x: x[0], list_has)))
# appendToFile(fname_was, list_has, was_has)
root.bind('<KeyRelease>', lambda event,
          question=question, answer=answer, context=context: giveKey(event, question, answer, context))

# atexit.register(font_delete)
root.mainloop()
