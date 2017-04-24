
create database grader;
use grader;


-- -----------------------------------------------------
-- Table `grader`.`TENANT_TABLE`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `grader`.`TENANT_TABLE` (
  `TENANT_ID` VARCHAR(10) NOT NULL,
  `TENANT_PASS` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`TENANT_ID`))
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `grader`.`TENANT_FIELDS`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `grader`.`TENANT_FIELDS` (
  `TENANT_ID` VARCHAR(10) NOT NULL,
  `FIELD_NAME` VARCHAR(45) NOT NULL,
  `FIELD_TYPE` VARCHAR(80) NULL,
  `FIELD_COLUMN` INT NOT NULL,
  PRIMARY KEY (`TENANT_ID`, `FIELD_NAME`),
  CONSTRAINT `fk_TENANT_FIELDS_TENANT_TABLE`
    FOREIGN KEY (`TENANT_ID` )
    REFERENCES `grader`.`TENANT_TABLE` (`TENANT_ID` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `grader`.`TENANT_DATA`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `grader`.`TENANT_DATA` (
  `RECORD_ID` VARCHAR(45) NOT NULL,
  `TENANT_ID` VARCHAR(10) NOT NULL,
  `COLUMN_1` VARCHAR(80) NULL,
  `COLUMN_2` VARCHAR(80) NULL,
  `COLUMN_3` VARCHAR(80) NULL,
  `COLUMN_4` VARCHAR(80) NULL,
  `COLUMN_5` VARCHAR(80) NULL,
  PRIMARY KEY (`TENANT_ID`, `RECORD_ID`))
ENGINE = InnoDB;

-- TENANT TABLE
insert into TENANT_TABLE( TENANT_ID, TENANT_PASS )
values ( 'khwu', 'abc123' ) ;

-- TENANT FIELDS
insert into TENANT_FIELDS( TENANT_ID, FIELD_NAME, FIELD_TYPE, FIELD_COLUMN ) values ( 'khwu', 'NUM', 'INT', 1 ) ;
insert into TENANT_FIELDS( TENANT_ID, FIELD_NAME, FIELD_TYPE, FIELD_COLUMN ) values ( 'khwu', 'FILE_NAME', 'VARCHAR(45)', 2 ) ;
insert into TENANT_FIELDS( TENANT_ID, FIELD_NAME, FIELD_TYPE, FIELD_COLUMN ) values ( 'khwu', 'SCORE', 'VARCHAR(45)', 3 ) ;
insert into TENANT_FIELDS( TENANT_ID, FIELD_NAME, FIELD_TYPE, FIELD_COLUMN ) values ( 'khwu', 'COMMENT', 'VARCHAR(45)', 4 ) ;

-- TENANT_DATA Record Example
insert into TENANT_DATA (RECORD_ID, TENANT_ID, COLUMN_1, COLUMN_2  ) 
values ( '1', 'khwu', '90', 'Very good!' ) ;
insert into TENANT_DATA (RECORD_ID, TENANT_ID, COLUMN_1, COLUMN_2  ) 
values ( '2', 'khwu', '70', 'Not so good!' ) ;
insert into TENANT_DATA (RECORD_ID, TENANT_ID, COLUMN_1, COLUMN_2  ) 
values ( '3', 'khwu', '40', 'Thanks for your interest' ) ;
insert into TENANT_DATA (RECORD_ID, TENANT_ID, COLUMN_1, COLUMN_2  ) 
values ( '4', 'khwu', '100', 'Perfect' ) ;

-- QUERY
select T.TENANT_ID, F.FIELD_NAME, F.FIELD_TYPE, F.FIELD_COLUMN
from TENANT_TABLE T, TENANT_FIELDS F
where T.TENANT_ID = F.TENANT_ID
and T.TENANT_ID = 'khwu'
order by F.FIELD_COLUMN;


-- Test Queries
select * from TENANT_DATA where TENANT_ID = 'khwu' ;
select * from TENANT_FIELDS where TENANT_ID = 'khwu' ;
update TENANT_FIELDS SET FIELD_COLUMN = 4 where FIELD_NAME =  'COMMENT;
