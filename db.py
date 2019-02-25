import os, psycopg2, csv

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(host="ec2-107-20-167-11.compute-1.amazonaws.com",database="d73a0td2ecipbc", user="gzxeabmkdscsaw", password="2fc456489aedf96b202f17cdd0d33ecaf86ed5e31736bdcfac35bac7846ad0d5")

csvfile = open("books.csv") 
reader = csv.reader(csvfile,delimiter=',')
print("Creating books table!")

cur = conn.cursor()

cur.execute("CREATE TABLE books ( id SERIAL PRIMARY KEY, \
								   isbn VARCHAR NOT NULL, \
								   title VARCHAR NOT NULL, \
								   author VARCHAR NOT NULL, \
								   year VARCHAR NOT NULL );")

print("Created!")

print("Adding values to table.")

for isbn, title, author, year in reader:
	cur.execute("INSERT INTO books (isbn, title, author, year) VALUES (%s, %s, %s, %s)",(isbn,title,author,year))

conn.commit()
print("Insert Completed!")


cur.execute("CREATE TABLE users (id SERIAL PRIMARY KEY, username VARCHAR(100) NOT NULL, email VARCHAR(100) NOT NULL, password VARCHAR NOT NULL, create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP);")
conn.commit()
print("user table created successfully")


cur.execute("CREATE TABLE reviews (id SERIAL PRIMARY KEY, review VARCHAR NOT NULL,book_id INTEGER NOT NULL,user_id INTEGER REFERENCES users);")
conn.commit()
print("Reviews table created successfully!")





