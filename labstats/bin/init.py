#!/usr/bin/env python3
# initializes the database
import labstats.db as db

cnx = db.get_connection()
cursor = cnx.cursor()

print('Creating session table...')

query = """
CREATE TABLE `session` (
    `id` int NOT NULL AUTO_INCREMENT,
    `host` varchar(255) NOT NULL,
    `user` varchar(16) NOT NULL,
    `start` datetime NOT NULL,
    `end` datetime DEFAULT NULL,
    `last_update` datetime,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB;

CREATE TABLE `staff` (
    `user` varchar(16) NOT NULL,
    PRIMARY KEY (`user`)
) ENGINE=InnoDB;

CREATE TABLE `printer_pages` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `date` datetime NOT NULL,
    `printer` varchar(255) NOT NULL,
    `value` int(11) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB;

CREATE TABLE `printer_toner` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `date` datetime NOT NULL,
    `printer` varchar(255) NOT NULL,
    `value` int(11) NOT NULL,
    `max` int(11) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB;

CREATE VIEW `session_duration` AS
    SELECT *, timediff(`end`, `start`) AS `duration` FROM `session`;

CREATE VIEW `session_duration_public` AS
    SELECT `id`, `host`, `start`, `end`, `duration` FROM `session_duration`;

CREATE VIEW `staff_session_duration_public` AS
    SELECT * FROM `session_duration` WHERE `user` IN (
        SELECT `user` FROM `staff`
    );

CREATE VIEW `users_in_lab` AS
    SELECT `user`, `host`, `start` FROM `session` WHERE `end` IS NULL;

CREATE VIEW `users_in_lab_count_public` AS
    SELECT COUNT(DISTINCT `user`) AS `count` FROM `users_in_lab`;

CREATE VIEW `staff_in_lab_public` AS
    SELECT `user`, `host`, `start` FROM `users_in_lab` WHERE `user` IN (
        SELECT `user` FROM `staff`
    );

CREATE VIEW `printer_pages_public` AS
    SELECT `id`, `date`, `printer`, `value` FROM `printer_pages`;

CREATE VIEW `printer_toner_public` AS
    SELECT `id`, `date`, `printer`, `value`, `max` FROM `printer_toner`;

CREATE VIEW `daily_sessions_public` AS
    SELECT
        COUNT(*) as logins,
            COUNT(DISTINCT `user`) as unique_logins,
            DATE(start) as date
        FROM `session`
        GROUP BY `date`
        ORDER BY `date` DESC;

GRANT SELECT ON `ocfstats`.`session_duration_public` TO 'anonymous'@'%';
GRANT SELECT ON `ocfstats`.`users_in_lab_count_public` TO 'anonymous'@'%';
GRANT SELECT ON `ocfstats`.`staff_in_lab_public` TO 'anonymous'@'%';
GRANT SELECT ON `ocfstats`.`staff_session_duration_public` TO 'anonymous'@'%';
GRANT SELECT ON `ocfstats`.`printer_pages_public` TO 'anonymous'@'%';
GRANT SELECT ON `ocfstats`.`printer_toner_public` TO 'anonymous'@'%';
GRANT SELECT ON `ocfstats`.`daily_sessions_public` TO 'anonymous'@'%';
"""

cursor.execute(query)
