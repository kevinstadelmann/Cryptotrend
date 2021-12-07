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
date date NOT NULL,
name varchar(50) NOT NULL,
market_cap DECIMAL(20,1) NOT NULL,
%_market_cap DECIMAL(3,3)
volume DECIMAL(16,1),
%_volume DECIMAL(4,2),
open DECIMAL(7,2),
%_open DECIMAL(3,3),
close DECIMAL(7,2),
%_close DECIMAL(3,3),
gain/loss DECIMAL(6,2),
created_ts TIMESTAMP
);

CREATE TABLE IF NOT EXISTS yahoo_oil_stage(
date date NOT NULL,
open DECIMAL(5,2) NOT NULL,
high DECIMAL(5,2) NOT NULL,
low DECIMAL(5,2) NOT NULL,
close DECIMAL(5,2) NOT NULL,
adjusted_close DECIMAL(5,2) NOT NULL,
volume INT,
percent_change DECIMAL(4,2),
name varchar(50) NOT NULL,
source varchar(50) NOT NULL,
);

CREATE TABLE IF NOT EXISTS yahoo_gold_stage(
date date NOT NULL,
open DECIMAL(6,2) NOT NULL,
high DECIMAL(6,2) NOT NULL,
low DECIMAL(6,2) NOT NULL,
close DECIMAL(6,2) NOT NULL,
adjusted_close DECIMAL(6,2) NOT NULL,
volume INT,
percent_change DECIMAL(4,2),
name varchar(50) NOT NULL,
source varchar(50) NOT NULL,
);

CREATE TABLE IF NOT EXISTS yahoo_nasdaq_stage(
date date NOT NULL,
open DECIMAL(7,2) NOT NULL,
high DECIMAL(7,2) NOT NULL,
low DECIMAL(7,2) NOT NULL,
close DECIMAL(7,2) NOT NULL,
adjusted_close DECIMAL(7,2) NOT NULL,
volume INT,
percent_change DECIMAL(4,2),
name varchar(50) NOT NULL,
source varchar(50) NOT NULL,
);