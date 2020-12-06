CREATE DATABASE cinema_db;

CREATE TABLE cinema_db.users (
  id NVARCHAR(36) PRIMARY KEY UNIQUE NOT NULL,
  full_name LONGTEXT NOT NULL,
  birthday DATE,
  email NVARCHAR(345) NOT NULL,
  phone_number NVARCHAR(15),
  password NVARCHAR(MAX),
  role INT
);

CREATE TABLE cinema_db.halls (
  id NVARCHAR(36) PRIMARY KEY UNIQUE NOT NULL,
  occupancy_of_hall INT NOT NULL
);

CREATE TABLE cinema_db.films (
  id NVARCHAR(36) PRIMARY KEY UNIQUE NOT NULL,
  duration DECIMAL(18,0) NOT NULL,
  name LONGTEXT NOT NULL
);

CREATE TABLE cinema_db.schedules (
  id NVARCHAR(36) PRIMARY KEY UNIQUE NOT NULL,
  date DATE NOT NULL,
  hall_id NVARCHAR(36) NOT NULL,
  user_creator_id NVARCHAR(36) NOT NULL,
  FOREIGN KEY (hall_id) REFERENCES cinema_db.halls(id),
  FOREIGN KEY (user_creator_id) REFERENCES cinema_db.users(id)
);

CREATE TABLE cinema_db.film_occupation_times (
  id NVARCHAR(36) PRIMARY KEY UNIQUE NOT NULL,
  schedule_id NVARCHAR(36),
  film_id NVARCHAR(36),
  start_time TIME(6),
  end_time TIME(6),
  FOREIGN KEY (schedule_id) REFERENCES cinema_db.schedules(id),
  FOREIGN KEY (film_id) REFERENCES cinema_db.films(id)
);

CREATE TABLE cinema_db.occupied_seats (
  id NVARCHAR(36) PRIMARY KEY UNIQUE NOT NULL,
  user_id NVARCHAR(36),
  film_ocupation_time_id NVARCHAR(36),
  FOREIGN KEY (user_id) REFERENCES cinema_db.users(id),
  FOREIGN KEY (film_ocupation_time_id) REFERENCES cinema_db.film_occupation_times(id)
);