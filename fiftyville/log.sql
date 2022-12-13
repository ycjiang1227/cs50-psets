-- Keep a log of any SQL queries you execute as you solve the mystery.

-- looking for crime scene report of crimes occuring on the day and street
SELECT * FROM crime_scene_reports WHERE year = 2021 AND month = 7 AND day = 28 AND street = "Humphrey Street";
    -- three interviews which mention bakery

-- Query for interviews mentioning the bakery
SELECT * FROM interviews WHERE transcript LIKE "%bakery%";
    -- Ruth: car left within 10 minutes of crime
    -- Eugene: recognised; withdrew money from Leggett St ATm
    -- Raymond: called for a minute to book earliest flight out of Fiftyville the next day

-- Look for bakery security logs within 10 minutes of crime; cars exiting within 10am
SELECT * FROM bakery_security_logs WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND minute < 25 AND activity = "exit";
    -- table of license plates generated in license_plate

-- Query for atm transactions at Legett St before 10:15am. gives account numbers
SELECT * FROM atm_transactions WHERE year = 2021 AND month = 7 AND day = 28 AND atm_location = "Leggett Street";
    -- account_number generated

-- Query for phone calls around 10am
SELECT * FROM phone_calls WHERE year = 2021 AND month = 7 AND day = 28 AND duration <60;
    -- caller and receivers that day generated

-- Query airports
SELECT * FROM airports WHERE city = "Fiftyville";
    -- fifty ville airport; ID = 8 ; abbreviation CSF

-- Query flights out of fiftyville on 29/7
SELECT * FROM flights WHERE year = 2021 AND month = 7 AND day = 29 AND origin_airport_id = 8;
    -- earliest flight is 8:20 to LaGuardia, flight id 36

-- Query passengers on flight
SELECT * FROM passengers WHERE flight_id = 36;
    -- passport_numbers can be queried

-- Query people with phone_number and passport_number, license_plate in list
SELECT * FROM people
WHERE phone_number IN (SELECT caller FROM phone_calls WHERE year = 2021 AND month = 7 AND day = 28 AND duration <60)
AND license_plate IN (SELECT license_plate FROM bakery_security_logs WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND minute < 25 AND activity = "exit")
AND passport_number IN (SELECT passport_number FROM passengers WHERE flight_id = 36);
    -- four suspects generated

-- Query people with matching bank accounts
SELECT * FROM people
WHERE id IN
(SELECT person_id FROM bank_accounts WHERE account_number IN
    (SELECT account_number FROM atm_transactions WHERE year = 2021 AND month = 7 AND day = 28 AND atm_location = "Leggett Street")
);

-- Narrow down suspect
SELECT * FROM people
WHERE phone_number IN (SELECT caller FROM phone_calls WHERE year = 2021 AND month = 7 AND day = 28 AND duration <60)
AND license_plate IN (SELECT license_plate FROM bakery_security_logs WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND minute < 25 AND activity = "exit")
AND passport_number IN (SELECT passport_number FROM passengers WHERE flight_id = 36)
AND id IN (SELECT person_id FROM bank_accounts WHERE account_number IN
    (SELECT account_number FROM atm_transactions WHERE year = 2021 AND month = 7 AND day = 28 AND atm_location = "Leggett Street")
);
    -- bruce is the thief, id 686048

-- caller ID
SELECT receiver FROM phone_calls WHERE year = 2021 AND month = 7 AND day = 28 AND duration <60 AND caller = (SELECT phone_number FROM people WHERE id = 686048);

-- accomplice
SELECT name FROM people WHERE phone_number = (SELECT receiver FROM phone_calls WHERE year = 2021 AND month = 7 AND day = 28 AND duration <60 AND caller = (SELECT phone_number FROM people WHERE id = 686048));