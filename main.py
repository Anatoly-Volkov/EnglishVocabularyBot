import sqlite3
import time
import random
import telegram
import threading as tr
BOT_TOKEN = "***"
admin_id = "***"
bot = telegram.Bot(BOT_TOKEN)
# -*- coding: utf-8 -*-

construs = ['¸', 'é', 'ö', 'ó', 'ê', 'å', 'í', 'ã', 'ø', 'ù', 'ç', 'õ', 'ú', 'ô', 'û', 'â', 'à', 'ï', 'ð', 'î', 'ë', 'ä', 'æ', 'ý', 'ÿ', '÷', 'ñ', 'ì', 'è', 'ò', 'ü', 'á', 'þ']

consteng = ['`', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', "'", 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.']

const = [60, 120, 600, 3600, 10800, 86400, 172800, 432000, 864000, 1814400, 3628800, 7776000, 15552000, 31104000, 62208000, 124416000, 248832000, 497664000, 995328000, 1990656000]

introducion = "Hello! I'm bot who can help you to learn English vocabulary. I can ask you words you have added. Use words 'add' and 'ask' to communicate with me and then follow the bot instructions. You can also write 'help' to get the list of special words"

helplist = "add - write it to add the new word \n\nask - write it to check yourself \n\n/delete - write it if you want to delete the word I have just asked \n\nstop - write this word to come to the zero state \n\nhelp - write it to repeat this message. \n\nAdvise: don't add words 'ask',  'add',  'help',  '/delete',  'stop' in your vocabulary."

'''
conn = sqlite3.connect('wordbot.db')
cursor = conn.cursor()
w1 = sqlite3.connect('eng_rus_words.db')
wcursor = w1.cursor()'''

def engl(s):
    letters = 'abcdefghijklmnopqrstuvwxyz '
    for elem in s:
        if elem not in letters:
            return False
    return True

def convert(word):
    ans = ''
    word.lower()
    for elem in word:
        if elem in construs:
            ans += consteng[construs.index(elem)]
        else:
            if elem in consteng:
                ans += construs[consteng.index(elem)]
            else:
                ans += elem
    return ans
'''
def P(word, wcursor):
    wcursor.execute("Select count from english where word = ?", [word])
    a = wcursor.fetchall()
    wcursor.execute("Select count from russian where word = ?", [word])
    b = wcursor.fetchall()  
    if len(a) == 0:
        ans1 = 0
    else:
        ans1 = a[0][0]
    if len(b) == 0:
        ans2 = 0
    else:
        ans2 = b[0][0]
    return max(ans1, ans2)

def correction(word, wcursor):
    return max(candidates(word), key=P(wcursor))
'''
def candidates(word):
    a = set([convert(word)])
    b = set([word])
    a = a.union(b)
    a = a.union(edits1(word))
    if len(word) < 10:
        a = a.union(edits2(word))
    return a
'''
def known(words, wcursor):
    wcursor.execute("Select word from english where word in ?", [words])
    a = wcursor.fetchall()
    return set(w[0] for w in a)
'''
def edits1(word):
    if engl(word):
        letters = 'abcdefghijklmnopqrstuvwxyz '
    else:
        letters = 'àáâãäå¸æçèéêëìíîïðñòóôõö÷øùúûüýþÿ '
    #"All edits that are one edit away from `word`."
    splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes    = [L + R[1:] for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:] for L, R in splits if R for c in letters]
    inserts    = [L + c + R for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word):
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))

def next_time(now, period):
    return time.time() + const[min(19, period)]
        
        
def message(bot, update, txt):
    #update.message.text
    bot.sendMessage(chat_id=update.message.chat.id,
                    text=txt)


            
    
def f(text, ident, wid, typ, p, bot, update, cursor):
    text = text.lower()
    cursor.execute("Select name from users where id = ?", [ident])
    a = cursor.fetchall()
    if (a[0][0] == admin_id and text == '/statistics'):
        cursor.execute("Select count(*) from users")
        a = cursor.fetchall()
        message(bot, update, "There are " + str(a[0][0]) + " users")
        return
    if len(text) > 30:
        message(bot, update, "Max lenth is 30 symbols. Try again")
        #print("Max lenth is 30 symbols. Try again")
    if text == 'stop':
        p = 0
        cursor.execute("Update users set position = ?, last = ? where id = ?", [p, text, ident])
        #conn.commit()
        return
    if text == 'help':
        message(bot, update, helplist)
        return 
    if p == 0:
        if text == 'ask':
            cursor.execute("Select * from connection where connection.usid = ? and nexttime < ?", [ident, time.time()])
            a = cursor.fetchall()
            if len(a) == 0:
                cursor.execute("Select * from connection where connection.usid = ?", [ident])
                a = cursor.fetchall()
                if len(a) == 0:
                    message(bot, update, "You have no words. Add them first")
                else:
                    message(bot, update, "Warning: add some new words")
                    cursor.execute("Select last from users where id = ?", [ident])
                    a = cursor.fetchall()
                    if a[0][0] == "@@@":
                        f('@@@', ident, wid, typ, 3, bot, update, cursor)
                        return 
                    message(bot, update, "Do you want me to ask you english(1) or russian(2) word. Write 1 or 2")
                    p = 3
                    last = ""
            else:
                cursor.execute("Select last from users where id = ?", [ident])
                a = cursor.fetchall()
                if a[0][0] == "@@@":
                    f('@@@', ident, wid, typ, 1, bot, update, cursor)
                    return
                message(bot, update, "Do you want me to ask you english(1) or russian(2) word. Write 1 or 2")
                p = 1
                last = ""
        else:
            typ = 0
        if text == 'add':
            message(bot, update, "Write the word in english")
            p = 6
            #print("Write the word in english")
        #print(p)
        cursor.execute("Update users set position = ?, typ = ?, last = ? where id = ?", [p, typ, "", ident])
        cursor.execute("Select position from users where id = ?", [ident])
        a = cursor.fetchall()
        #conn.commit()
        return
    if p == 1:
        if text == 'stop':
            p = 0
            cursor.execute("Update users set typ = ?, wid = ?, position = ?, last = ? where id = ?", [typ, wid, p, "", ident])
            #conn.commit()
            return
        if text == 'add':
            f('add', ident, wid, typ, 0, bot, update, cursor)
            return
        
        if text != "@@@":
            if text not in ['1', '2', 'stop', 'add']:
                message(bot, update, "It's incorrect. Try again")
                return
            if text == '1' or text == '2':
                p = 2
                typ = int(text)            
        p = 2
        cursor.execute("Select * from connection where connection.usid = ? and nexttime < ?", [ident, time.time()])
        a = cursor.fetchall()
        rand = random.randint(0, len(a) - 1)
        cursor.execute("Select * from words where words.id = ?", [a[rand][1]])
        a2 = cursor.fetchall()
        if typ == 1:
            message(bot, update, a2[0][1])
        else:
            message(bot, update, a2[0][2])
        wid = a2[0][0]
        cursor.execute("Update users set typ = ?, wid = ?, position = ? where id = ?", [typ, wid, p, ident])
        #conn.commit()
        return
        
    if p == 2:
        cursor.execute("Select * from words where words.id = ?", [wid])
        a = cursor.fetchall()
        cand = candidates(text)
        if (typ == 1 and a[0][2] in cand) or (typ == 2 and a[0][1] in cand):
            if (typ == 1 and a[0][2] == text) or (typ == 2 and a[0][1] == text):
                message(bot, update, "Correct!")
                #print("Correct!")
            else:
                if typ == 1:
                    message(bot, update, "Correct but with spelling mistake. The wright answer was " + a[0][2])
                    #print("Correct but with spelling mistake. The wright answer was " + a[0][2])
                else:
                    message(bot, update, "Correct but with spelling mistake. The wright answer was " + a[0][1])
                    #print("Correct but with spelling mistake. The wright answer was " + a[0][1])
            cursor.execute("Select nexttime, timeperiod from connection where usid = ? and wid = ?", [ident, wid])
            res = cursor.fetchall()
            cursor.execute("Update connection set nexttime = ?, timeperiod = ? where usid = ? and wid = ?", [next_time(res[0][0], res[0][1]), res[0][1] + 1, ident, wid])
            #conn.commit()
        else:
            if text == '/delete':
                cursor.execute("Delete from words where userid = ? and id = ?", [ident, wid])
                cursor.execute("Delete from connection where usid = ? and wid = ?", [ident, wid])
                #conn.commit()
                message(bot, update, "Succesfully")
                #print("Succesfully")
            else:
                if typ == 1:
                    message(bot, update, "Incorrect... The wright answer is " + a[0][2])
                    #print("Incorrect... The wright answer is " + a[0][2])
                else:
                    message(bot, update, "Incorrect... The wright answer is " + a[0][1])
                    #print("Incorrect... The wright answer is " + a[0][1])                
        
        cursor.execute("Update users set typ = ?, wid = ?, last = ? where id = ?", [typ, wid, "@@@", ident])
        f('ask', ident, wid, typ, 0, bot, update, cursor)
        #conn.commit()
        return
    if p == 3:
        if text == 'stop':
            p = 0
            last = ""
            cursor.execute("Update users set typ = ?, wid = ?, position = ?, last = ? where id = ?", [typ, wid, p, last, ident])
            #conn.commit()
            return
        if text == 'add':
            f('add', ident, wid, typ, 0, bot, update, cursor)
            return
        if text != "@@@":
            if text not in ['1', '2', 'stop', 'add']:
                message(bot, update, "It's incorrect. Try again")
                return
            if text == '1' or text == '2':
                p = 4
                typ = int(text)            
            #print("It's incorrect. Try again")
        p = 4
        cursor.execute("Select * from connection where connection.usid = ?", [ident])
        a = cursor.fetchall()
        rand = random.randint(0, len(a) - 1)
        cursor.execute("Select * from words where words.id = ?", [a[rand][1]])
        a2 = cursor.fetchall()
        if typ == 1:
            message(bot, update, a2[0][1])
            #print(a2[0][1])  
        else:
            message(bot, update, a2[0][2])
            #print(a2[0][2])
        wid = a2[0][0]
        cursor.execute("Update users set typ = ?, wid = ?, position = ? where id = ?", [typ, wid, p, ident])
        #conn.commit()
        return        
    if p == 4:
        cursor.execute("Select * from words where words.id = ?", [wid])
        a = cursor.fetchall()
        cand = candidates(text)
        if (typ == 1 and a[0][2] in cand) or (typ == 2 and a[0][1] in cand):
            if (typ == 1 and a[0][2] == text) or (typ == 2 and a[0][1] == text):
                message(bot, update, "Correct!")
                #print("Correct!")
            else:
                if typ == 1:
                    message(bot, update, "Correct but with spelling mistake. The wright answer was " + a[0][2])
                    #print("Correct but with spelling mistake. The wright answer was " + a[0][2])
                else:
                    message(bot, update, "Correct but with spelling mistake. The wright answer was " + a[0][1])
                    #print("Correct but with spelling mistake. The wright answer was " + a[0][1])
        else:
            if text == '/delete':
                cursor.execute("Delete from words where userid = ? and id = ?", [ident, wid])
                cursor.execute("Delete from connection where usid = ? and wid = ?", [ident, wid])
                #conn.commit()
                message(bot, update, "Succesfully")
                #print("Succesfully")
            else:
                if typ == 1:
                    message(bot, update, "Incorrect... The wright answer is " + a[0][2])
                    #print("Incorrect... The wright answer is " + a[0][2])
                else:
                    message(bot, update, "Incorrect... The wright answer is " + a[0][1])
                    #print("Incorrect... The wright answer is " + a[0][1])                
        
        cursor.execute("Update users set typ = ?, wid = ?, last = ? where id = ?", [typ, wid, "@@@", ident])
        f('ask', ident, wid, typ, 0, bot, update, cursor)
        #conn.commit()
        return        
    if p == 6:
        if text == 'stop':
            p = 0
            cursor.execute("Update users set position = ?, last = ? where id = ?", [p, text, ident])
            #conn.commit()            
        if text == 'ask':
            f('ask', ident, wid, typ, 0, bot, update, cursor)
        if text not in ["stop", "ask"]:
            if not engl(text):
                message(bot, update, "It is not in english. Try again")
                #print("It is not in english. Try again")
            else:
                message(bot, update, "Write the translation")
                #print("Write the translation")
                p = 7
            cursor.execute("Update users set position = ?, last = ? where id = ?", [p, text, ident])
            #conn.commit()
        return
    if p == 7:
        if text == 'stop':
            p = 0
            cursor.execute("Update users set position = ?", [0])
        if text == 'ask':
            f('ask', ident, wid, typ, 0, bot, update, cursor)
        if text not in ["stop", "ask"]:
            cursor.execute("Select last from users where id = ?", [ident])
            a = cursor.fetchall()
            english = a[0][0]
            russian = text
            cursor.execute("Select id from words where words.enword = ? and words.rusword = ? and words.userid = ?", [english, russian, ident])
            a = cursor.fetchall()
            if len(a) != 0:
                message(bot, update, "You have added these word before")
            else:
                cursor.execute("Insert into words (enword, rusword, userid) values(?, ?, ?)", [english, russian, ident])
                cursor.execute("Select id from words where words.enword = ? and words.rusword = ? and words.userid = ?", [english, russian, ident])
                a = cursor.fetchall()
                cursor.execute("Insert into connection (usid, wid, nexttime, timeperiod) values(?, ?, ?, ?)", [int(ident), int(a[0][0]), time.time(), 0])
                #conn.commit()
                message(bot, update, "Succesfully")
            message(bot, update, "Add another word or write 'stop' or 'ask'")
            f('add', ident, wid, typ, 0, bot, update, cursor)
            #cursor.execute("Update users set last = ? where id = ?", [last, ident])
        #conn.commit()
        return


'''t = input()
while t != 'stop':
    cursor.execute("Select* from users where id = ?", [ident])
    y = cursor.fetchall()
    p = y[0][2]
    wid = y[0][3]
    typ = y[0][4]
    f(t, ident, wid, typ)
    t = input()
'''
f_r = open("config_file.in", "r")
help = list(map(str, f_r.readline().split('=')))
n = int(help[1])
help = list(map(str, f_r.readline().split('=')))
way = help[1]
f_r.close()
current_offset = 0
def request(num, fcfc):
    global current_offset, lock
    #conn = sqlite3.connect('wordbot.db')
    conn = sqlite3.connect(way)
    cursor = conn.cursor()
    #w1 = sqlite3.connect('eng_rus_words.db')
    #wcursor = w1.cursor()
    while True:
        try:
            lock.acquire()
            try:
                updates = bot.getUpdates(offset=current_offset, timeout=60,
                                         allowed_updates=["message"])
            except:
                lock.release()
                continue
            if len(updates) == 0:
                lock.release()
                continue
            update = updates[0]
            current_offset = update.update_id + 1
            lock.release()
            try:
                cursor.execute("Select * from users where name = ?", [str(update.message.chat.id)])
                a = cursor.fetchall()
                if len(a) == 0:
                    message(bot, update, introducion)
                    message(bot, update, helplist)
                    cursor.execute("Insert into users (name, position, wid, typ, last) values(?, ?, ?, ?, ?)", [str(update.message.chat.id), 0, 0, 1, ''])
                    message(bot, update, "Succesfuly")
                    cursor.execute("Select * from users where name = ?", [str(update.message.chat.id)])
                    a = cursor.fetchall()                
                #text, ident, wid, typ, p
                #print(a)
                cursor.execute("Select id, last from users where name = ?", [str(update.message.chat.id)])
                a2 = cursor.fetchall()
                try:
                    cursor.execute("Update users set last = ? where id = ?", [a2[0][1], a2[0][0]])
                    f(update.message.text, a2[0][0], a[0][3], a[0][4], a[0][2], bot, update, cursor)
                    #message(bot, update, num)
                    conn.commit()
                except Exception as e:
                    #print(e)
                    continue
            except Exception as e:
                #print(e)
                continue
        except Exception as e:
            #print(e)
            continue
    conn.close()
    w1.close()    
arr = []
lock = tr.Lock()
for num in range(n):
    arr.append(tr.Thread(target=request, args=(num, 0)))
    arr[-1].start()
for num in range(10):
    arr[num].join()
        
