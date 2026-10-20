package it.sistinf.romacapitale.management.pman.dto;

import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.ToString;

import java.io.Serializable;

@Data
@ToString
@NoArgsConstructor
public class PmPreferitiDTO implements Serializable {
	private static final long serialVersionUID = 1L;

	private Long idApplicazione;
	private Long idUtente;
	private Long idRuolo;
	private Long idNodo;
	private Long idMicrofunzione;
	private String descrizione;
	private String url;
	private Long ordine;
	private String codEsterno;
	private ApplicazioneDTO pmApplicazioniDto;
	private ProfiloDTO pmRuoliDto;
	private UtenteDTO pmUtentiDto;
	private NodoStrutturaDTO pmNodiPiantaOrganicaDto;
	private AbilitazioneDTO pmMicrofunzioniDto;
	

}