DROP DATABASE IF EXISTS cip_project;

CREATE DATABASE cip_project;

USE cip_project;

# Create tables
CREATE TABLE IF NOT EXISTS twitter_bitcoin_stage(
alias VARCHAR(5) NOT NULL,
date DATE NOT NULL,
valuation FLOAT(8) NOT NULL,
created_dt TIMESTAMP,
source VARCHAR(40)
);

