CREATE TABLE users (
	id int PRIMARY KEY auto_increment, 
	username varchar(50) NOT NULL,
	password_hash varchar(100) NOT NULL,
	avatar varchar(100) NULL,
	created_on datetime default current_timestamp(),
	verification_key varchar(4) NOT NULL,
	verified tinyint default 0,
	notification_key varchar(100),
	account_type tinyint default 1,
    target_amount float,
    target_date datetime
);

CREATE INDEX idx_users_username ON users(username);

CREATE TABLE incomings (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    label VARCHAR(100) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    frequency ENUM('Monthly', 'Yearly', 'Weekly', 'Daily') NOT NULL,
    created_on DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX idx_incomings_user_id ON incomings(user_id);

CREATE TABLE outgoings (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    label VARCHAR(100) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    frequency ENUM('Monthly', 'Yearly', 'Weekly', 'Daily') NOT NULL,
    created_on DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX idx_outgoings_user_id ON outgoings(user_id);

CREATE TABLE savings (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    label VARCHAR(100) NOT NULL,
    current_amount DECIMAL(10,2) DEFAULT 0,
    created_on DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX idx_savings_user_id ON savings(user_id);

CREATE TABLE daily_spends (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    label VARCHAR(100),
    amount DECIMAL(10,2) NOT NULL,
    spend_date DATE NOT NULL,
    created_on DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX idx_daily_spends_user_id ON daily_spends(user_id);
CREATE INDEX idx_daily_spends_spend_date ON daily_spends(spend_date);
