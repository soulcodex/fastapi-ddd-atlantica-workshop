CREATE TABLE IF NOT EXISTS `shoes` (
    `id`            VARCHAR(26) NOT NULL,
    `name`          VARCHAR(255) NOT NULL,
    `color`         VARCHAR(100) NOT NULL,
    `size`          CHAR(10) NOT NULL,
    `price`         INT(11) NOT NULL,
    `available`     TINYINT(1) SIGNED NOT NULL,
    `created_at`    DATETIME(3) NOT NULL,
    `updated_at`    DATETIME(3) NOT NULL,
    PRIMARY KEY (`shoe_id`),
    KEY         `shoes_size_idx` (`size`),
    KEY         `shoes_color_idx`(`color`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE `utf8mb4_bin` ENGINE = InnoDB;