CREATE SCHEMA `keyword` ;

CREATE TABLE `keyword`.`datamail` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `idMail` VARCHAR(45) NULL,
  `dateMsg` VARCHAR(45) NULL,
  `fromMsg` VARCHAR(45) NULL,
  `subjectMsg` VARCHAR(45) NULL,
  PRIMARY KEY (`id`));