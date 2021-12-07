# preparation

DROP DATABASE IF EXISTS cip_project;
CREATE DATABASE cip_project;
USE cip_project;

# create stage tables

CREATE TABLE IF NOT EXISTS coingecko_stage(
date date NOT NULL,
name CHAR(7) NOT NULL,
market_cap DECIMAL(20,1) NOT NULL,
perc_market_cap FLOAT(6),
volume DECIMAL(16,1),
perc_volume FLOAT(6),
open DECIMAL(7,2),
perc_open FLOAT(6),
close DECIMAL(7,2),
perc_close FLOAT(6),
gain_loss DECIMAL(6,2),
time_stamps date NOT NULL);


CREATE TABLE IF NOT EXISTS original_coingecko(
name CHAR(7) NOT NULL,
date varchar(10) NOT NULL,
market_cap DECIMAL(20,1) NOT NULL,
volume DECIMAL(16,1),
open DECIMAL(7,2),
close DECIMAL(7,2)
);
