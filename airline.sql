CREATE TABLE flights (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    flight_name TEXT,
    source TEXT,
    destination TEXT,
    departure TEXT,
    arrival TEXT,
    price REAL
);

CREATE TABLE bookings (
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
