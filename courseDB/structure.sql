 TABLE customer(
Customer_ID INTEGER PRIMARY KEY NOT NULL,
Username TEXT NOT NULL,
Residence_address TEXT,
Phone TEXT NOT NULL,
Email TEXT NOT NULL,
GPS_location TEXT NOT NULL);


 TABLE bank_card(Number INTEGER PRIMARY KEY NOT NULL,
Expire TEXT NOT NULL,
Security_code INTEGER NOT NULL);


 TABLE car_order(
Order_ID INTEGER PRIMARY KEY NOT NULL,
Cost INTEGER NOT NULL,
Pickup TEXT NOT NULL,
Destination TEXT NOT NULL);


 TABLE car(
Car_ID INTEGER PRIMARY KEY NOT NULL,
Model TEXT NOT NULL,
License_plate INTEGER NOT NULL,
Color TEXT NOt NULL,
Mileage INTEGER NOT NULL,
GPS_location TEXT NOT NULL,
State TEXT,
Battery_level INTEGER);


 TABLE charging_station(
Station_ID INTEGER PRIMARY KEY NOT NULL,
price INTEGER NOT NULL,
charging_time INTEGER NOT NULL,
GPS_location TEXT NOT NULL,
Available_sockets INTEGER NOT NULL);


 TABLE parts_provide(
Provider_ID INTEGER PRIMARY KEY NOT NULL,
Name TEXT NOT NULL,
Address TEXT NOT NULL,
Phone INTEGER NOT NULL,
parts_types TEXT);


 TABLE car_part(
Part_ID INTEGER PRIMARY KEY NOT NULL,
Manufacturer_ID INTEGER NOT NULL,
type TEXT NOT NULL,
Color TEXT NOT NULL,
Price TEXT NOT NULL,
Provider TEXT NOT NULL);


 TABLE workshop(
Workshop_ID INTEGER PRIMARY KEY NOT NULL,
Work_time TEXT,
Address TEXT NOT NULL,
GPS_location TEXT NOT NULL);
