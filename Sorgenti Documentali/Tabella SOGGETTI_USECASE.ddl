-- atti.soggetti_usecase definition

-- Drop table

-- DROP TABLE atti.soggetti_usecase;

CREATE TABLE atti.soggetti_usecase (
	cd_usecase varchar(10) NOT NULL,
	cd_soggetto varchar(50) NOT NULL,
	ty_soggetto varchar(30) NOT NULL,
	nm_soggetto varchar(250) NOT NULL,
	ty_presenza varchar(10) NOT NULL,
	ty_configurazione varchar(10) NOT NULL,
	fg_dichiarante bpchar(1) NOT NULL,
	fg_comparente bpchar(1) NOT NULL,
	fg_firmatario bpchar(1) NOT NULL,
	nr_ordinamento int2 NOT NULL,
	fg_operante bpchar(1) NOT NULL,
	tx_note text NULL,
	cd_ope_ins_dt bpchar(6) NOT NULL,
	ts_ins_dt timestamp NULL,
	cd_ope_ult_agg_dt bpchar(6) NULL,
	ts_ult_agg_dt timestamp NULL,
	ds_note_dt varchar(50) NULL,
	CONSTRAINT soggetti_usecase_fg_comparente_check CHECK ((fg_comparente = ANY (ARRAY['0'::bpchar, '1'::bpchar]))),
	CONSTRAINT soggetti_usecase_fg_dichiarante_check CHECK ((fg_dichiarante = ANY (ARRAY['0'::bpchar, '1'::bpchar]))),
	CONSTRAINT soggetti_usecase_fg_firmatario_check CHECK ((fg_firmatario = ANY (ARRAY['0'::bpchar, '1'::bpchar]))),
	CONSTRAINT soggetti_usecase_fg_operante_check CHECK ((fg_operante = ANY (ARRAY['0'::bpchar, '1'::bpchar]))),
	CONSTRAINT soggetti_usecase_pk PRIMARY KEY (cd_usecase, cd_soggetto)
);

-- Table Triggers

create trigger soggetti_usecase_insert after
insert
    on
    atti.soggetti_usecase for each row execute function registra_soggetti_usecase_insert();
create trigger soggetti_usecase_update after
update
    on
    atti.soggetti_usecase for each row execute function registra_soggetti_usecase_update();
create trigger soggetti_usecase_delete after
delete
    on
    atti.soggetti_usecase for each row execute function registra_soggetti_usecase_delete();