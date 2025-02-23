DROP TABLE IF EXISTS vacation;
DROP TABLE IF EXISTS roles;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS country;
DROP TABLE IF EXISTS likes;

CREATE TABLE roles ( id SERIAL PRIMARY KEY,role_name VARCHAR(20));

CREATE TABLE users (id SERIAL PRIMARY KEY, 
                    first_name VARCHAR(20),
                    last_name VARCHAR(20),
                    email  VARCHAR(30) NOT NULL UNIQUE,
                    password INT,
                    role_id SERIAL NOT NULL,
                    FOREIGN KEY (role_id) REFERENCES roles(id)ON DELETE CASCADE);

CREATE TABLE country(id SERIAL PRIMARY KEY,country_name VARCHAR(30));

CREATE  TABLE vacation (id SERIAL PRIMARY KEY,
                       id_country SERIAL,
                       vacation_description TEXT,
                       start_date DATE,
                       end_date DATE,
                       file_image VARCHAR(150),
                       FOREIGN KEY (id_country) REFERENCES country(id) ON DELETE CASCADE);
CREATE TABLE likes( user_id SERIAL,
                    vacation_id SERIAL,
                    FOREIGN KEY(vacation_id) REFERENCES vacation(id) ON DELETE CASCADE,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE);
ALTER TABLE vacation
ADD price FLOAT;
INSERT INTO roles(role_name) 
VALUES
('admin'),
('user');
INSERT INTO users(first_name,last_name,email,password,role_id) 
VALUES
('Moshe','Cohen','moshecohen@gmail.com',12345,1),
('Izhak','Sade','izhaksade@gmail.com',54321,2);

INSERT INTO country(country_name)
VALUES
('France'), ('Italy'), ('Japan'), ('USA'), ('Canada'),
('Spain'), ('Germany'), ('Brazil'), ('Australia'), ('Greece');
INSERT INTO vacation(id_country,vacation_description,start_date,end_date,file_image,price)
VALUES
(2,'The best vacation for pizza lovers','2025-3-20','2025-3-25','pizza.jpg',500),
(1,'Honey moon vacation','2025-4-1','2025-4-8','honey_moon.jpg',1000),
(3,'Samurai experience in Tokyo','2025-4-10','2025-4-24','samurai.jpg',3200),
(4,'A trip to the California coast','2025-09-10','2025-09-20','california.jpg',3500),
(5,'Exploring the Canadian Rockies','2025-10-01','2025-10-10','canada_rockies.jpg',2800),
(6,'Historical tour of Madrid','2025-11-05','2025-11-15','madrid.jpg',2200),
(7,'A trip to the Black Forest in Germany','2025-12-10','2025-12-20','forest.jpg',2900),
(8,'Adventure in the Amazon, Brazil','2026-01-15','2026-01-25','amazon.jpg',4900),
(9,'Beach vacation in Australia','2026-02-10','2026-02-20','aust_beach.jpg',3300),
(10,'Weekend in Ancient Greece','2026-03-05','2026-03-10','greece.jpg',1900),
(1,'A trip to rural France','2026-04-01','2026-04-10','france_rural.jpg',2700),
(2,'Wine vacation in Tuscany','2026-05-10','2026-05-20','tuscany_wine.jpg',3100);
