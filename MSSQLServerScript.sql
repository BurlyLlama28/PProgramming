CREATE DATABASE cinema_db;

CREATE TABLE `cinema_db`.users (
  `id` NVARCHAR(36) PRIMARY KEY UNIQUE NOT NULL,
  `full_name` LONGTEXT NOT NULL,
  `birthday` DATE,
  `email` NVARCHAR(345) NOT NULL,
  `phone_number` NVARCHAR(15)
);

CREATE TABLE `cinema_db`.schedules (
  `id` NVARCHAR(36) PRIMARY KEY UNIQUE NOT NULL,
  `date` DATE NOT NULL,
  `occupancy_of_hall` INT NOT NULL
);

CREATE TABLE `cinema_db`.films (
  `id` NVARCHAR(36) PRIMARY KEY UNIQUE NOT NULL,
  `duration` DECIMAL(18,0) NOT NULL,
  `name` LONGTEXT NOT NULL
);

CREATE TABLE `cinema_db`.filmsSchedules (
  `id` NVARCHAR(36) PRIMARY KEY UNIQUE NOT NULL,
  `film_id` NVARCHAR(36) NOT NULL,
  `schedule_id` NVARCHAR(36) NOT NULL,
  CONSTRAINT `fk schedules.id to filmsSchedules.schedule_id` FOREIGN KEY (`schedule_id`) REFERENCES `cinema_db`.schedules(`id`),
  CONSTRAINT `fk films.id to filmsSchedules.film_id` FOREIGN KEY (`film_id`) REFERENCES `cinema_db`.films(`id`)
);

CREATE TABLE `cinema_db`.busy_times (
  `id` NVARCHAR(36) PRIMARY KEY UNIQUE NOT NULL,
  `schedule_id` NVARCHAR(36) NOT NULL,
  `film_id` NVARCHAR(36) NOT NULL,
  `start_time` TIME(6) NOT NULL,
  `end_time` TIME(6) NOT NULL,
  CONSTRAINT `fk schedules.id to busy_times.schedule_id` FOREIGN KEY (`schedule_id`) REFERENCES `cinema_db`.schedules(`id`),
  CONSTRAINT `fk films.id to busy_times.film_id` FOREIGN KEY (`film_id`) REFERENCES `cinema_db`.films(`id`)
);