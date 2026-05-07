--Load the tables

Create table pinsy_gff as 
select * from read_csv(Pinsy01.gff3, ignore_errors=true);

Create table pinsy_tsv as 
select * from read_csv(Pinsy01.tsv, ignore_errors=true);

Create table bepen_gff as 
select * from read_csv(Bepen.gff3, ignore_errors=true);

Create table bepen_tsv as 
select * from read_csv('Bepen.tsv', ignore_errors=true);

Create table picab_gff as 
select * from read_csv(Picab02.gff3, ignore_errors=true);

Create table picab_tsv as 
select * from read_csv(Picab02.tsv, ignore_errors=true);

Create table potra_gff as 
select * from read_csv(Potra02.gff3, ignore_errors=true);

Create table potra_tsv as 
select * from read_csv(Potra02.tsv, ignore_errors=true);

Create table tieton_gff as 
select * from read_csv(Tieton02.gff3, ignore_errors=true);

Create table tieton_tsv as 
select * from read_csv(Tieton02.tsv, ignore_errors=true);

Create table araport as 
select * from read_csv(TAIR10_araport11_sorted.gff3, ignore_errors=true);

Create table tair_gff as 
select * from read_csv(TAIR10_GFF3_genes_sorted.gff3, ignore_errors=true);

create table pinsy_genes as
select column2, column8 from pinsy_gff where column2 = 'gene' ; 

create table pinsy_id as select 
string_split(string_split(column8, ';')[1], '=')[2] as "ID"
from pinsy_genes; 

--Verify
--select * from pinsy_id where ID not like 'PS_%' ;

update pinsy_tsv set id = string_split(id, '.')[1];

Create table pinsy as select
a.*, b.eggnog_description
from  pinsy_id a
join pinsy_tsv b on a.ID = b.id;

--Verify: pinsy and pinsy_tsv should have the same rows. 

--eggnog_description NULL instead of NA
update pinsy set eggnog_description = CASE WHEN eggnog_description = 'NA' then NULL else eggnog_description END; 






create table bepen_genes as
select column2, column8 from bepen_gff where column2 = 'gene' ; 

create table bepen_id as select 
string_split(string_split(column8, ';')[1], '=')[2] as "ID"
from bepen_genes
OFFSET 1; 

--Verify
--select * from bepen_id where ID not like 'Bpev%' ;


update bepen_tsv set query = regexp_replace(query, '\.[^.]*$', '');

Create table bepen as select
a.*, b.Description
from  bepen_id a
join bepen_tsv b on a.ID = b.query;

--Verify: bepen 55 less rows than bepen_tsv

update bepen set Description = CASE WHEN Description = '-' then NULL else Description END; 







create table picab_genes as
select column2, column8 from picab_gff where column2 = 'gene' ; 

create table picab_id as select 
string_split(string_split(column8, ';')[1], '=')[2] as "ID"
from picab_genes; 

--Verify
--select * from picab_id where ID not like 'PA_%' ;

update picab_tsv set id = string_split(id, '.')[1];

Create table picab as select
a.*, b.eggnog_description
from  picab_id a
join picab_tsv b on a.ID = b.id;

--Verify: OK

--eggnog_description NULL instead of NA
update picab set eggnog_description = CASE WHEN eggnog_description = 'NA' then NULL else eggnog_description END; 





create table tieton_genes as
select column2, column8 from tieton_gff where column2 = 'gene' ; 

create table tieton_id as select 
string_split(string_split(column8, ';')[1], '=')[2] as "ID"
from tieton_genes; 

--Verify
--select * from tieton_id where ID not like 'FUN_%' ;

update tieton_tsv set query = string_split(query, '-')[1];

Create table tieton as select
a.*, b.Description
from  tieton_id a
join tieton_tsv b on a.ID = b.query;

--Verify: Same rows 

--Description NULL instead of -
update tieton set Description = CASE WHEN Description = '-' then NULL else Description END; 

--Remove the genes that don't have annotations

Create table middle_pinsy as
select * from pinsy where eggnog_description not null; -- From 83.8k to 62.1k 


Create table middle_bepen as
select * from bepen where Description not null; --1.5k less 

Create table middle_picab as
select * from picab where eggnog_description not null; --3.4k less


Create table middle_tieton as
select * from tieton where Description not null; --2.8k less

Drop table pinsy; 
Drop table bepen; 
Drop table picab;
Drop table tieton;

--Check for dublicates and remove them

--select distinct ID from middle_pinsy; --38,120 unique
--select distinct ID from middle_picab; --32,225 unique 
--select distinct ID from middle_bepen; -- 20,619 unique 
--select distinct ID from middle_tieton; --25,291 unique 


create table pinsy_ids as
select distinct ID from middle_pinsy;
create table picab_ids as
select distinct ID from middle_picab;
create table tieton_ids as
select distinct ID from middle_tieton;
create table bepen_ids as
select distinct ID from middle_bepen;

Create table pinsy as 
select a.*, b.eggnog_description 
from pinsy_ids a 
left join lateral(
select eggnog_description 
from middle_pinsy b 
where b.ID = a.ID 
LIMIT 1 
) b on true; 

Create table picab as 
select a.*, b.eggnog_description 
from picab_ids a 
left join lateral(
select eggnog_description 
from middle_picab b 
where b.ID = a.ID 
LIMIT 1 
) b on true; 

Create table tieton as 
select a.*, b.Description 
from tieton_ids a 
left join lateral(
select Description
from middle_tieton b 
where b.ID = a.ID 
LIMIT 1 
) b on true; 

Create table bepen as 
select a.*, b.Description 
from bepen_ids a 
left join lateral(
select Description
from middle_bepen b 
where b.ID = a.ID 
LIMIT 1 
) b on true; 

--Clean database
drop table pinsy_genes;
drop table pinsy_gff;
drop table pinsy_tsv; 
drop table pinsy_id; 

drop table bepen_genes;
drop table bepen_gff;
drop table bepen_tsv; 
drop table bepen_id; 

drop table picab_genes;
drop table picab_gff;
drop table picab_tsv; 
drop table picab_id; 

drop table tieton_genes;
drop table tieton_gff;
drop table tieton_tsv; 
drop table tieton_id; 

drop table middle_pinsy;
drop table middle_picab;
drop table middle_tieton;
drop table middle_bepen;

drop table pinsy_ids; 
drop table picab_ids; 
drop table tieton_ids; 
drop table bepen_ids; 

--Export tables as csvs
COPY pinsy to 'pinsy.csv' (HEADER FALSE);
Copy bepen to 'bepen.csv' (HEADER FALSE); 
copy picab to 'picab.csv' (HEADER FALSE);
copy tieton to 'tieton.csv'(HEADER FALSE);
