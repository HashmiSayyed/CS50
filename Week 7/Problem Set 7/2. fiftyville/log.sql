-- Keep a log of any SQL queries you execute as you solve the mystery.

-- 1. Looking for crime_scene_reports 28-July-2021.
SELECT description FROM crime_scene_reports
WHERE year = 2021 AND month = 7 AND day = 28;
-- time: 10:15am, place: Humphrey Street bakery, No. of witnesses: 3.
-- Notes: each of their(witnesses) interview transcripts mentions the bakery.

-- 2. Looking at interview transcript
SELECT name,transcript From interviews
WHERE year = 2021 AND month = 7 AND day = 28 AND transcript LIKE "%bakery%";
-- Transcripts:
-- Ruth: Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away. If you have security footage from the bakery parking lot, you might want to look for cars that left the parking lot in that time frame.

-- Eugene: I don't know the thief's name, but it was someone I recognized. Earlier this morning, before I arrived at Emma's bakery, I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money.

-- Raymond: As the thief was leaving the bakery, they called someone who talked to them for less than a minute. In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow. The thief then asked the person on the other end of the phone to purchase the flight ticket.

-- 3. Looking at bakery_security_logs for between 10:15 and 10:25 then associate license plate to cars owner.
SELECT name FROM people
WHERE license_plate IN (
    SELECT license_plate FROM bakery_security_logs
    WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND minute >= 15 AND minute <= 25 AND activity = "exit"
);
-- names of suspects by looking at bakery_security_logs.
-- Vanessa
-- Barry
-- Iman
-- Sofia
-- Luca
-- Diana
-- Kelsey
-- Bruce

-- 4. Looking at atm_transactions for that day then associate account number with their owner.
SELECT people.name FROM bank_accounts
JOIN people ON person_id = people.id
WHERE bank_accounts.account_number IN (
    SELECT account_number FROM atm_transactions
    WHERE year = 2021 AND month = 7 AND day = 28 AND atm_location = "Leggett Street" AND transaction_type = "withdraw"
);
-- names of suspects by looking at atm_transactions.
-- Bruce
-- Diana
-- Brooke
-- Kenny
-- Iman
-- Luca
-- Taylor
-- Benista

-- common names in both lists.
-- Iman
-- Luca
-- Diana
-- Bruce

-- 5. First trying to find earliest flight then it's passengers.
SELECT name FROM people
WHERE passport_number IN (
    SELECT passport_number FROM passengers
    WHERE flight_id = (
        SELECT id FROM flights
        WHERE year = 2021 AND month = 7 AND day = 29 AND origin_airport_id = (
            SELECT id FROM airports
            WHERE city = "Fiftyville"
        ) ORDER BY hour, minute LIMIT 1
    )
);
-- names of suspects by looking at passengers list.
-- Kenny
-- Sofia
-- Taylor
-- Luca
-- Kelsey
-- Edward
-- Bruce
-- Doris

-- common names in all three lists.
-- Luca
-- Bruce

-- 6. Now trying to find something from phone_calls records.
SELECT name FROM people
WHERE phone_number IN (
    SELECT caller FROM phone_calls
    WHERE year = 2021 AND month = 7 AND day = 28 AND duration < 60
);
-- names of suspects by looking at phone_calls records.
-- Kenny
-- Sofia
-- Benista
-- Taylor
-- Diana
-- Kelsey
-- Bruce
-- Carina

-- common names in all Four lists.
-- Bruce

-- From all these data we can conclude that Bruce is thief now let's see who is accomplice.

-- 7. Receiver of the call must be accomplice.
SELECT name FROM people
WHERE phone_number = (
    SELECT receiver FROM phone_calls
    WHERE year = 2021 AND month = 7 AND day = 28 AND duration < 60 AND caller = (
        SELECT phone_number FROM people
        WHERE name = "Bruce"
    )
);
-- Robin

-- Robin is accomplice now let's find city the thief escaped to.

--8. We know flight id from this we can find destination airport.
SELECT city FROM airports
WHERE id = (
    SELECT destination_airport_id FROM flights
    WHERE id = (
        SELECT id FROM flights
        WHERE year = 2021 AND month = 7 AND day = 29 AND origin_airport_id = (
            SELECT id FROM airports
            WHERE city = "Fiftyville"
        ) ORDER BY hour, minute LIMIT 1
    )
);
-- New York City.