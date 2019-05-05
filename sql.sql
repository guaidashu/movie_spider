create table `mv_type`
(
    `id`           int(11)      NOT NULL AUTO_INCREMENT COMMENT 'primary key',
    `name`         varchar(255) NOT NULL COMMENT 'movie type name',
    `url`          varchar(255) NOT NULL COMMENT 'movie type`s url address',
    `img_src`      varchar(255) NOT NULL COMMENT 'movie type`s cover img src',
    `icon_img_src` varchar(255) NOT NULL COMMENT 'movie type`s icon img src',
    `description`  text         NOT NULL COMMENT 'movie type`s description',
    `status`       int(1)       NOT NULL COMMENT 'type`s status, mark whether movie list is get',
    PRIMARY KEY (`id`)
) ENGINE = InnoDB
  AUTO_INCREMENT = 1
  DEFAULT CHARSET = utf8 COMMENT 'movie type table';

create table `mv_list`
(
    `id`                 int(11)      NOT NULL AUTO_INCREMENT COMMENT 'primary key',
    `url`                varchar(255) NOT NULL COMMENT 'movie url',
    `img_src`            varchar(255) NOT NULL COMMENT 'cover img src',
    `description`        text         NOT NULL COMMENT 'detail description',
    `description_poster` text         NOT NULL COMMENT 'simple description',
    `origin_src`         varchar(255) NOT NULL COMMENT 'origin img src(little icon)',
    `star`               varchar(255) NOT NULL COMMENT 'star level',
    `title`              varchar(255) NOT NULL COMMENT 'movie title',
    `page_views`         int(11)      NOT NULL COMMENT 'movie pageviews',
    `director`           varchar(255) NOT NULL COMMENT 'movie`s director',
    `label`              varchar(255) NOT NULL COMMENT 'movie label',
    `category_id`        int(11)      NOT NULL COMMENT 'category id',
    PRIMARY KEY (`id`)
) ENGINE = InnoDB
  AUTO_INCREMENT = 1
  DEFAULT CHARSET = utf8 COMMENT 'movie list table';

create table `mv_content`
(
    `id`        int(11) NOT NULL AUTO_INCREMENT COMMENT 'primary key',
    `url`       text    NOT NULL COMMENT 'video url address',
    `video_src` text    NOT NULL COMMENT 'video origin src address',
    `parent_id` int(11) NOT NULL COMMENT 'movie list table`s id',
    PRIMARY KEY (`id`)
) ENGINE = InnoDB
  AUTO_INCREMENT = 1
  DEFAULT CHARSET = utf8 COMMENT 'movie detail content';