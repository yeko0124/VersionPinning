DROP DATABASE version_db IF EXISTS version_db;

CREATE DATABASE version_db;
USE version_db;

CREATE TABLE IF NOT EXISTS user_table
(
    id int not null AUTO_INCREMENT PRIMARY KEY ,
    user CHAR(50) NOT NULL,
    depart VARCHAR(25) NULL,

    UNIQUE KEY user_info (user, depart)
);

CREATE TABLE IF NOT EXISTS version_final_table
(
    id int not null AUTO_INCREMENT PRIMARY KEY ,
    cache_name VARCHAR(100) NOT NULL,
    updated_time datetime,
    user_id  int NOT NULL,

    CONSTRAINT FK_version_final_user_id FOREIGN KEY (user_id)
    REFERENCES user_table (id)
    ON UPDATE CASCADE ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS user_history
(
    id int not null AUTO_INCREMENT PRIMARY KEY ,
    final_id int not null,
    user_id int not null,
    updated_date datetime,

    CONSTRAINT FK_user_history_final_id FOREIGN KEY (final_id)
    REFERENCES version_final_table (id)
    ON UPDATE CASCADE ON DELETE CASCADE,

    CONSTRAINT FK_user_history_user_id FOREIGN KEY (user_id)
    REFERENCES user_table (id)
    ON UPDATE CASCADE ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS cache_table
(
    id int not null AUTO_INCREMENT PRIMARY KEY ,
    final_id int not null,
    cache_path varchar(255) not null,

    CONSTRAINT FK_cache_final_id FOREIGN KEY (final_id)
        REFERENCES version_final_table (id)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS ref_note_table
(
    id int not null AUTO_INCREMENT PRIMARY KEY ,
    note text null,
    cache_id int not null,

    CONSTRAINT FK_ref_note_cache_id FOREIGN KEY (cache_id)
    REFERENCES cache_table (id)
    ON UPDATE CASCADE ON DELETE CASCADE
);

DELIMITER //

CREATE TRIGGER tgr_after_insert_version
    AFTER INSERT ON version_final_table
    FOR EACH ROW
    BEGIN
        INSERT into user_history (final_id, user_id, updated_date) VALUES(NEW.id, NEW.user_id, NOW());
    END;

CREATE TRIGGER tgr_after_update_version
    AFTER UPDATE ON version_final_table
    FOR EACH ROW
    BEGIN
        INSERT into user_history (final_id, user_id, updated_date) VALUES(NEW.id, NEW.user_id, NOW());
    END;

# USE version_db;
# show tables;
# drop trigger tgr_after_insert_version;


# 모든 user는 미리 등록해놓기
INSERT INTO user_table (user, depart) VALUES ('yeeun', 'Animation');
INSERT INTO user_table (user, depart) VALUES ('jiyoung', 'Effects');
INSERT INTO user_table (user, depart) VALUES ('jeonghyeon', 'Modeling');
INSERT INTO user_table (user, depart) VALUES ('junhyeok', 'Lighting');
INSERT INTO user_table (user, depart) VALUES ('sangbok', 'Texturing');
INSERT INTO user_table (user, depart) VALUES ('seonhui', 'Shading');
INSERT INTO user_table (user, depart) VALUES ('sian', 'Rendering');
INSERT INTO user_table (user, depart) VALUES ('juno', 'Effects');
INSERT INTO user_table (user, depart) VALUES ('sujin', 'Rigging');
INSERT INTO user_table (user, depart) VALUES ('seongcheol', 'Effects');

select * from user_table;
select * from user_history;
select * from version_final_table;
select * from cache_table;
select * from ref_note_table;

DELIMITER //

SELECT COUNT(*) FROM cache_table WHERE final_id = 1;
SELECT cache_path FROM cache_table WHERE final_id = 1;


# INSERT INTO user_table (user, depart) VALUES ('rapa', 'System');
# INSERT INTO user_table (email, depart) VALUES ('ljy@gmail.com', 'Effects');
# INSERT INTO user_table (email, depart) VALUES ('rapa@gmail.com', 'System');

# DELETE from user_table where id = 11;

# INSERT INTO version_final_table (cache_name, updated_time, user_id) VALUES ('usd_rop1_v001.usda', NOW(), 1);
# INSERT INTO cache_table (final_id, cache_path) VALUES (1, '/home/rapa/workspace/houdini/pinning_version/geo/pinning_version/usd_rop1/usd_rop1_v001.usda');
# INSERT INTO ref_note_table (note, cache_id) VALUES ('add five clouds on the blue building', 1);
# UPDATE user_table SET depart = 'Software Development' WHERE id = 3;

# delete * from user_table;
