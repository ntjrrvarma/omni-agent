CREATE TABLE IF NOT EXISTS freezers (
    unit_id VARCHAR PRIMARY KEY,
    temperature FLOAT,
    status VARCHAR
);

INSERT INTO freezers (unit_id, temperature, status) VALUES 
('404', -72, 'Optimal'),
('405', -68, 'Warning'),
('406', -75, 'Normal');