import sqlite3

def add_user(email, name1, name2, name3, passw, verify_number):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO Users (verifytag, email, password, whitelisted, namea, nameb, namec) VALUES (?, ?, ?, ?, ?, ?, ?)', (verify_number, email, passw, 0, name1, name2, name3,))
    connection.commit()
    cursor.execute('SELECT MAX(id) FROM Users')
    max_id = cursor.fetchone()[0]
    connection.close()
    return max_id

def add_trip(destination, description, group, price, state, participants):
    connection = sqlite3.connect('trips.db')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO Trips (destination, description, class, price, state, quantity) VALUES (?, ?, ?, ?, ?, ?)', (destination, description, group, price, state, participants,))
    connection.commit()
    cursor.execute('SELECT MAX(id) FROM Trips')
    max_id = cursor.fetchone()[0]
    connection.close()
    return max_id

def add_participant(participant, id):
    id = str(id)
    participant = str(participant)
    connection = sqlite3.connect('trips.db')
    cursor = connection.cursor()
    cursor.execute('SELECT participants FROM Trips WHERE id = ?', (id,))
    participants = ""
    for i in cursor.fetchall():
        if i[0] is None or i[0] == '':
            participants = participant
        else:
            participants = i[0] + "_" + participant
    cursor.execute('UPDATE Trips SET participants = ? WHERE id = ?', (participants, id,))
    connection.commit()
    connection.close()

def delete_participant(participant, id):
    id = str(id)
    participant = str(participant)
    connection = sqlite3.connect('trips.db')
    cursor = connection.cursor()
    cursor.execute('SELECT participants FROM Trips WHERE id = ?', (id,))
    participants = ""
    for i in cursor.fetchall():
        participants = i[0].replace("_" + participant, "")
        participants = participants.replace(participant, "")
    cursor.execute('UPDATE Trips SET participants = ? WHERE id = ?', (participants, id,))
    connection.commit()
    connection.close()

def whitelist_user(verify_number):
    verify_number = str(verify_number)
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    cursor.execute('UPDATE Users SET whitelisted = 1 WHERE verifytag = ?', (verify_number,))
    connection.commit()
    connection.close()

def read_users():
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Users')
    users = cursor.fetchall()
    result = list()
    for user in users:
        result.append(list(user))
    connection.close()
    return result

def read_users_verify_number():
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    cursor.execute('SELECT verifytag FROM Users')
    users = cursor.fetchall()
    result = list()
    for user in users:
        result.append(user[0])
    connection.close()
    return result

def get_user_data(id="-1", verify_number="-1"):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    if id == "-1":
        cursor.execute('SELECT * FROM Users WHERE verifytag = ?', (verify_number,))
    else:
        cursor.execute('SELECT * FROM Users WHERE id = ?', (id,))
    users = cursor.fetchall()
    res = list()
    for costyl in users:
        res = list(costyl)
    connection.close()
    return res


def check_whitelisting(verify_number):
    l = get_user_data(verify_number=str(verify_number))
    if l != [] and l[4] == 1:
        return True
    else:
        return False

def read_trips():
    connection = sqlite3.connect('trips.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Trips')
    trips = cursor.fetchall()
    result = list()
    for trip in trips:
        result.append(list(trip))
    connection.close()
    return result

def read_trip_participants(id):
    id = str(id)
    connection = sqlite3.connect('trips.db')
    cursor = connection.cursor()
    cursor.execute('SELECT participants FROM Trips WHERE id = ?', (id,))
    trips = cursor.fetchall()
    result = list()
    for trip in trips:
        result = list(str(trip[0]).split('_'))
    connection.close()
    if result == ['']:
        result = []
    return result

def get_trips_verifies():
    l = read_trips()
    res = list()
    for i in range(len(l)):
        res.append(l[i][7])
    return res

def update_state(id, new_state):
    connection = sqlite3.connect('trips.db')
    cursor = connection.cursor()
    cursor.execute('UPDATE Trips SET state = ? WHERE id = ?', (new_state, id,))
    connection.commit()
    connection.close()
