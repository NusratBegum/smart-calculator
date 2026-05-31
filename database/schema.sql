CREATE TABLE users(
    id SERIAL PRIMARY KEY,
    username varchar(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE calculation_history(
    id SERIAL PRIMARY KEY,
    user_id INT  not null REFERENCES users(id) on delete cascade,
    expression VARCHAR(100) NOT NULL,
    result FLOAT NOT NULL, 
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
