import sqlite3
from random import shuffle

def insert_player(player_id,username):
    con = sqlite3.connect("db.db")
    cur =con.cursor()
    sql = f"INSERT INTO players (player_id,username) VALUES ('{player_id}','{username}')"
    cur.execute(sql)
    con.commit()
    con.close()


def players_amount():
    con = sqlite3.connect("db.db")
    cur = con.cursor()
    sql = f"SELECT * FROM players"
    cur.execute(sql)
    res = cur.fetchall()
    con.close()
    return len(res)


def get_mafia_usernames():
    con = sqlite3.connect("db.db")
    cur =con.cursor()
    sql = f"SELECT username FROM PLAYERS where role='mafia'"
    cur.execute(sql)
    data = cur.fetchall()
    names = ''
    for row in data:
        name = row[0]
        names += name +'\n'
    con.close()
    return names


def get_players_roles():
    con = sqlite3.connect("db.db")
    cur =con.cursor()
    sql = f"SELECT player_id, role FROM players"
    cur.execute(sql)
    data = cur.fetchall()
    con.close()
    return data


def get_all_alive():
    con = sqlite3.connect("db.db")
    cur =con.cursor()
    sql = f"SELECT username FROM players WHERE dead=0"
    cur.execute(sql)
    data = cur.fetchall()
    data =[row[0] for row in data]
    con.close()
    return data


def set_roles(players):
     con = sqlite3.connect("db.db")
     cur =con.cursor()
     game_roles = ['citizen'] * players
     mafia = int(players * 0.3)
     for i in range(mafia):
         game_roles[i]='mafia'
     shuffle(game_roles)
     sql = f"SELECT player_id FROM players"
     cur.execute(sql)
     player_ids = cur.fetchall()
     player_ids =[row[0] for row in player_ids]
     for role,player_id in zip(game_roles,player_ids):
         sql = f"UPDATE players SET role = '{role}' WHERE player_id ={player_id}"
         cur.execute(sql)
     con.commit()
     con.close()



def vote(type,user_name,player_id):
    con = sqlite3.connect("db.db")
    cur =con.cursor()
    sql = f"SELECT username FROM players WHERE player_id={player_id} AND dead=0 AND voted=0"
    cur.execute(sql)
    can_vote = cur.fetchone()
    if can_vote:
        sql = f"UPDATE players SET {type} = {type}+1 WHERE username = '{user_name}'"
        cur.execute(sql)
        cur.execute(f"UPDATE players SET voted = 1 WHERE player_id = '{player_id}' ")
        con.commit()
        con.close()
        return True
    con.close()
    return False


def mafia_kill():
    con = sqlite3.connect("db.db")
    cur = con.cursor()
    cur.execute(f"SELECT MAX(mafia_vote) FROM players")
    max_votes = cur.fetchone()[0]
    cur.execute(f"SELECT COUNT(*) WHERE dead =0 and role ='mafia'")
    mafia_alive = cur.fetchone()[0]
    username_killed = 'никого'
    if mafia_vote == mafia_alive:
        cur.execute(f"SELECT username FROM players WHERE mafia_vote ={max_votes}")
        username_killed = cur.fetchone()[0]
        cur.execute(f"UPDATE players SET dead = 1 WHERE username = '{username_killed}'")
        con.commit()
    con.close()
    return username_killed


def citizens_kill():
    con = sqlite3.connect("db.db")
    cur = con.cursor()
    cur.execute(f"SELECT MAX(citizen_vote) FROM players")
    max_votes = cur.fetchone()[0]
    cur.execute(f"SELECT COUNT(*) FROM players WHERE citizen_vote ={max_votes}")
    max_votes_count = cur.fetchone()[0]
    username_killed = 'никого'
    if max_votes_count ==1:
        cur.execute(f"SELECT username FROM players WHERE citizen_vote ={max_votes}")
        username_killed = cur.fectchone()[0]
        cur.excute(f"UPDATE players SET dead =1 WHERE username='{username_killed}'")
    con.close()
    return username_killed


def check_winner():
    con = sqlite3.connect("db.db")
    cur = con.cursor()
    cur.execute(f"SELECT COUNT(*) FROM players WHERE dead = 0 and role = 'mafia'")
    mafia_alive = cur.fetchone()[0]
    cur.execute(f"SELECT COUNT(*) FROM players WHERE dead = 0 and role = 'citizen'")
    citizen_alive = cur.fetchone()[0]
    if mafia_alive >= citizen_alive:
        return 'мафия'
    if mafia_alive == 0:
        return 'горожане'

def clear(dead=False):
    con = sqlite3.connect("db.db")
    cur = con.cursor()
    sql = f"UPDATE players SET citizen_vote=0, mafia_vote=0, voted=0"
    if dead:
        sql += ',dead=0'
    cur.execute(sql)
    con.commit()
    con.close()

