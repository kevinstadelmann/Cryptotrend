# preparation

DROP DATABASE IF EXISTS cip_project;
CREATE DATABASE cip_project;
USE cip_project;

# create stage tables

CREATE TABLE IF NOT EXISTS twitter_bitcoin_stage(
date date NOT NULL,
asset VARCHAR(5) NOT NULL,
count INT,
percent_change DECIMAL(4,2),
source VARCHAR(30),
created_ts TIMESTAMP
);

CREATE TABLE IF NOT EXISTS googletrend_bitcoin_stage(
date date NOT NULL,
interest_rate decimal(4,2) NOT NULL,
percent_change DECIMAL(4,2),
);

CREATE TABLE IF NOT EXISTS coingecko_bitcoin_stage(
name varchar(50),
date date NOT NULL,
market_cap decimal(4,2) NOT NULL,
percent_change DECIMAL(4,2),
volume INT,
open INT,
close INT
);

