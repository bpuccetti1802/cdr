package it.sistinf.romacapitale.management.pman.dto;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonRootName;
import io.swagger.v3.oas.annotations.media.Schema;
import it.sistinf.romacapitale.integration.management.vo.AmbitoVO;
import it.sistinf.romacapitale.integration.management.vo.ApplicazioneVO;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.ToString;

import java.io.Serializable;

@Data
@ToString
@NoArgsConstructor
@JsonRootName("PmApplicazioniDTO")
public class ApplicazioneDTO implements Serializable {
	private static final long serialVersionUID = 1L;

	@JsonProperty("idApplicazione")
	private Long idApplicazioneSa;

	@JsonProperty("descrizione")
	private String dsApplicazione;

	@JsonProperty("label")
	private String dsLabel;

	@JsonProperty("ordine")
	private Integer nmOrdine;

	@JsonProperty("service")
	private String dsService;

	@JsonProperty("url")
	private String dsEndpoint;

	@JsonProperty("urlDatiSpecifici")
	private String urlDatiSpecifici;

	@JsonIgnore
	private ApplicazioneDTO applicazionePadre;

}