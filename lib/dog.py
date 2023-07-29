import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    def __init__(self, name, breed):
      self.name = name
      self.breed = breed
      self.id = None

    @classmethod
    def create_table(cls):
        CURSOR.execute('''
            CREATE TABLE IF NOT EXISTS dogs (
            id INTEGER PRIMARY KEY, 
            name TEXT NOT NULL,
            breed TEXT NOT NULL
        )
    ''')
        CONN.commit()
    
    @classmethod
    def drop_table(cls):
      CURSOR.execute('DROP TABLE IF EXISTS dogs')
      CONN.commit()

    def save(self):
      if self.id is None:
         CURSOR.execute('INSERT INTO dogs (name, breed) VALUES (?, ?)', (self.name, self.breed))
         self.id = CURSOR.lastrowid
      else:
        CURSOR.execute('UPDATE dogs SET name=?, breed=?, WHERE id=?', (self.name, self.breed, self.id))
    CONN.commit()

    @classmethod
    def create(cls, name, breed):
      dog = cls(name, breed)
      dog.save()
      return dog
   
    @classmethod
    def new_from_db(cls, row):
      dog = cls(row[1], row[2])
      dog.id = row[0]
      return dog
   
    @classmethod
    def get_all(cls):
      CURSOR.execute('SELECT * FROM dogs')
      rows = CURSOR.fetchall()
      return [cls.new_from_db(row) for row in rows]
   
    @classmethod
    def find_by_name(cls, name):
      CURSOR.execute('SELECT * FROM dogs WHERE name=?', (name,))
      row = CURSOR.fetchone()
      if row:
         return cls.new_from_db(row)
      return None
   
    @classmethod
    def find_by_id(cls, dog_id):
      CURSOR.execute('SELECT *  FROM dogs WHERE id=?', (dog_id,))
      row = CURSOR.fetchone()
      if row:
         return cls.new_from_db(row)
      return None
    
    def update(self):
       if self.id is not None:
          CURSOR.execute('UPDATE dogs SET name=?, breed=? WHERE id=?', (self.name, self.breed, self.id))
          CONN.commit()
       else:
          raise ValueError("Cannot update a Dog without an ID.")

    @classmethod
    def find_or_create_by(cls, name, breed):
       found_dog = cls.find_by_name_and_breed(name, breed)
       if found_dog:
          return found_dog
       
       new_dog = cls(name, breed)
       new_dog.save()
       return new_dog
    
    @classmethod
    def find_by_name_and_breed(cls, name, breed):
       CURSOR.execute('SELECT * FROM dogs WHERE name=? AND breed=?', (name, breed))
       row = CURSOR.fetchone()
       if row:
          return cls.new_from_db(row)
       return None
