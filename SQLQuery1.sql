CREATE DATABASE TRAVEL_ACTIVITIES;

USE TRAVEL_ACTIVITIES;


-- CREATING TABLES

CREATE TABLE AIRLINE_LOOKUP(
AIRLINE_CODE VARCHAR(10) PRIMARY KEY,
AIRLINE_NAME VARCHAR(100),
HOME_REGION VARCHAR(100)
)

CREATE TABLE AIRPORT_LOOKUP(
AIRPORT_CODE VARCHAR(10) PRIMARY KEY,
CITY VARCHAR(50),
REGION VARCHAR(100)
)

CREATE TABLE BOOKINGS(
BOOKING_ID VARCHAR(70) PRIMARY KEY,
BOOKING_DATE VARCHAR(20),
TRAVEL_DATE VARCHAR(20),
CHANNEL VARCHAR(20),
TRIP_TYPE VARCHAR(20),
CABIN VARCHAR(20),
AIRLINE VARCHAR(10),
ORIGIN VARCHAR(10),
DESTINATION VARCHAR(10),
ROUTE_BAND VARCHAR(50),
PAX_COUNT INT,
BASE_FARE FLOAT,
TAXES_USD FLOAT,
TOTAL_USD FLOAT,
COST_USD FLOAT,
PROFIT_USD FLOAT,
BOOKING_STATUS VARCHAR(50),
CANCEL_REASON VARCHAR(200),
LEAD_TIME INT,
SEASON VARCHAR(50)
foreign key (AIRLINE) references AIRLINE_LOOKUP (AIRLINE_CODE),
foreign key (ORIGIN) references AIRPORT_LOOKUP (AIRPORT_CODE)
)

CREATE TABLE PASSENGERS(
PASSENGER_ID VARCHAR(70) PRIMARY KEY,
BOOKING_ID VARCHAR(70),
PASSENGER_TYPE VARCHAR(10),
GENDER VARCHAR(5),
AGE INT,
NATIONALITY VARCHAR(100),
LOYALTY_MEMBER INT
FOREIGN KEY (BOOKING_ID) REFERENCES BOOKINGS (BOOKING_ID)
)


CREATE TABLE PAYMENTS(
PAYMENT_ID VARCHAR(70) PRIMARY KEY,
BOOKING_ID VARCHAR(70),
PAYMENT_METHOD VARCHAR(50),
PAID_USD FLOAT,
PAYMENT_DATE VARCHAR(70),
PAYMENT_STATUS VARCHAR(50)
FOREIGN KEY (BOOKING_ID) REFERENCES BOOKINGS (BOOKING_ID)
)


CREATE TABLE SEGMENTS(
SEGMENT_ID VARCHAR(70) PRIMARY KEY,
BOOKING_ID VARCHAR(70),
LEG_NO INT,
DEP_AIRPORT VARCHAR(10),
ARR_AIRPORT VARCHAR(10),
DEP_CITY VARCHAR(100),
ARR_CITY VARCHAR(100),
DEP_DATE VARCHAR(100),
FLIGHT_DURATION INT,
STOP_TYPE VARCHAR(50)
FOREIGN KEY (BOOKING_ID) REFERENCES BOOKINGS (BOOKING_ID)
)


-- UPLOAD DATA

bulk insert AIRLINE_LOOKUP
from 'C:\Users\USER\Documents\Travel Agency\airlines_lookup.csv'
with(
firstrow = 2,
fieldterminator = ',',
rowterminator = '\n',
tablock
);


BULK INSERT AIRPORT_LOOKUP
FROM 'C:\Users\USER\Documents\Travel Agency\airports_lookup.csv'
with(
firstrow = 2,
fieldterminator = ',',
rowterminator = '\n',
tablock
);



BULK INSERT BOOKINGS
FROM 'C:\Users\USER\Documents\Travel Agency\bookings.csv'
with(
firstrow = 2,
fieldterminator = ',',
rowterminator = '\n',
tablock
);



BULK INSERT PASSENGERS
FROM 'C:\Users\USER\Documents\Travel Agency\passengers.csv'
with(
firstrow = 2,
fieldterminator = ',',
rowterminator = '\n',
tablock
);



BULK INSERT PAYMENTS
FROM 'C:\Users\USER\Documents\Travel Agency\payments.csv'
with(
firstrow = 2,
fieldterminator = ',',
rowterminator = '\n',
tablock
);




BULK INSERT SEGMENTS
FROM 'C:\Users\USER\Documents\Travel Agency\segments.csv'
with(
firstrow = 2,
fieldterminator = ',',
rowterminator = '\n',
tablock
);



-- 1. Counts of trips taken by passengers

SELECT 
    passenger_id,
    COUNT(*) AS trip_count
FROM passengers
GROUP BY passenger_id
order by trip_count Desc


select * from bookings

-- 2. Top 3 expensive trip from and to

select Top 3 dep_city, arr_city
from
segments s
left join bookings b
on s.booking_id = b.booking_id
order by b.total_usd desc


-- 3. Top priority gender in term of number of booking

select Top 1 gender, count(*) as gender_count
from
passengers
group by gender
order by gender_count Desc

-- 4. Top priority gender in term of amount spent

select Top 1 gender, avg(b.total_usd) as Amount_Spent
from
passengers p
left join bookings b
on p.booking_id = b.booking_id
group by gender
order by Amount_Spent Desc

-- 5. Top 3 most booked destination

select Top 3 arr_city, count(*)
from segments
group by arr_city


-- Lets Gather data we need to solve predictive, segmentation, recommendation

select * from payments

select b.booking_date, b.travel_date, b.channel, b.trip_type, b.cabin, b.airline, b.origin, b.destination, b.pax_count,
b.base_fare, b.taxes_usd, b.total_usd, b.cost_usd, b.profit_usd, b.lead_time, b.season, p.passenger_type, p.gender, p.nationality, p.loyalty_member,
pa.payment_method, pa.paid_usd, pa.payment_date, s.dep_airport, s.arr_airport, s.dep_city, s.arr_city, s.dep_date, s.flight_duration, s.stop_type
from passengers p
left join bookings b
on p.booking_id = b.booking_id
left join payments pa
on b.booking_id = pa.booking_id
left join segments s
on b.booking_id = s.booking_id
where b.booking_status != 'Cancelled' and pa.payment_status = 'Paid'
