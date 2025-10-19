from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

DB_NAME = "airline.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

# Create tables if not exist
def init_db():
    if not os.path.exists(DB_NAME):
        conn = get_db_connection()
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS flights (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            flight_name TEXT,
            source TEXT,
            destination TEXT,
            departure TEXT,
            arrival TEXT,
            price REAL
        );

        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            flight_id INTEGER,
            name TEXT,
            email TEXT,
            seats INTEGER,
            FOREIGN KEY (flight_id) REFERENCES flights (id)
        );

        INSERT INTO flights (flight_name, source, destination, departure, arrival, price)
        VALUES
        ('Air India 101', 'Delhi', 'Mumbai', '08:00', '10:00', 4500),
        ('IndiGo 205', 'Chennai', 'Kolkata', '09:30', '12:15', 5200),
        ('SpiceJet 302', 'Bangalore', 'Goa', '07:45', '09:15', 3800),
        ('Vistara 410', 'Delhi', 'Dubai', '13:00', '16:30', 18000);
        """)
        conn.commit()
        conn.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/flights')
def flights():
    conn = get_db_connection()
    flights = conn.execute('SELECT * FROM flights').fetchall()
    conn.close()
    return render_template('flights.html', flights=flights)

@app.route('/book/<int:flight_id>', methods=['GET', 'POST'])
def book(flight_id):
    conn = get_db_connection()
    flight = conn.execute('SELECT * FROM flights WHERE id = ?', (flight_id,)).fetchone()
    if not flight:
        conn.close()
        return "Flight not found", 404

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        seats = request.form['seats']

        conn.execute(
            'INSERT INTO bookings (flight_id, name, email, seats) VALUES (?, ?, ?, ?)',
            (flight_id, name, email, seats)
        )
        conn.commit()
        conn.close()
        return redirect('/confirmation')
    conn.close()
    return render_template('book.html', flight=flight)

@app.route('/confirmation')
def confirmation():
    return render_template('confirmation.html')

@app.route('/admin')
def admin():
    conn = get_db_connection()
    bookings = conn.execute("""
        SELECT b.id, f.flight_name, b.name, b.email, b.seats
        FROM bookings b JOIN flights f ON b.flight_id = f.id
    """).fetchall()
    conn.close()
    return render_template('admin.html', bookings=bookings)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
