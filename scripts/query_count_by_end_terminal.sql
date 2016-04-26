-- All rentals counted by end terminal

SELECT `all_rentals`.end_terminal, count(*), `station_locations`.terminal,
    `station_locations`.station, `station_locations`.location,
    `station_locations`.lat, `station_locations`.lon,
    `station_locations`.dock_count
FROM `all_rentals`
LEFT JOIN `station_locations`
ON (
    `all_rentals`.end_terminal = `station_locations`.terminal
) GROUP BY `all_rentals`.end_terminal ;
