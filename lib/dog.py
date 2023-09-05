import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()



import sqlite3

import sqlite3

class Dog:
    def __init__(self, name, breed):
        self.name = name
        self.breed = breed
        self.id = None  # We'll set this later when saving to the database

    @classmethod
    def create_table(cls):
        connection = sqlite3.connect('lib/dogs.db')
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dogs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT
            )
        ''')
        connection.commit()
        connection.close()

    @classmethod
    def drop_table(cls):
        connection = sqlite3.connect('lib/dogs.db')
        cursor = connection.cursor()
        cursor.execute('DROP TABLE IF EXISTS dogs')
        connection.commit()
        connection.close()

    def save(self):
        connection = sqlite3.connect('lib/dogs.db')
        cursor = connection.cursor()
        if self.id is None:
            cursor.execute('INSERT INTO dogs (name, breed) VALUES (?, ?)', (self.name, self.breed))
            self.id = cursor.lastrowid
        else:
            cursor.execute('UPDATE dogs SET name = ?, breed = ? WHERE id = ?', (self.name, self.breed, self.id))
        connection.commit()
        connection.close()

    @classmethod
    def create(cls, name, breed):
        dog = cls(name, breed)
        dog.save()
        return dog

    @classmethod
    def new_from_db(cls, db_row):
        dog = cls(db_row[1], db_row[2])
        dog.id = db_row[0]
        return dog

    @classmethod
    def get_all(cls):
        connection = sqlite3.connect('lib/dogs.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM dogs')
        dogs_data = cursor.fetchall()
        connection.close()
        dogs = [cls.new_from_db(row) for row in dogs_data]
        return dogs

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('lib/dogs.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM dogs WHERE name = ?', (name,))
        dog_data = cursor.fetchone()
        connection.close()
        if dog_data:
            return cls.new_from_db(dog_data)
        else:
            return None

    @classmethod
    def find_by_id(cls, id):
        connection = sqlite3.connect('lib/dogs.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM dogs WHERE id = ?', (id,))
        dog_data = cursor.fetchone()
        connection.close()
        if dog_data:
            return cls.new_from_db(dog_data)
        else:
            return None

    @classmethod
    def find_or_create_by(cls, name, breed):
        existing_dog = cls.find_by_name(name)
        if existing_dog:
            return existing_dog
        else:
            return cls.create(name, breed)

    def update(self):
        if self.id:
            self.save()
        else:
            raise ValueError("Cannot update a dog without an ID")

# Create the dogs table if it doesn't exist
Dog.create_table()





