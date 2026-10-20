package it.sistinf.romacapitale.management.pman.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonRootName;
import io.swagger.v3.oas.annotations.media.Schema;
import it.sistinf.romacapitale.integration.management.vo.NodoStrutturaVO;
import it.sistinf.romacapitale.integration.management.vo.ProfiloVO;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.ToString;


/**
 * Classe UtentePerProfiloVO
 */
@Data
@ToString
@NoArgsConstructor
@JsonRootName("PmUtentiRuoliDTO")
public class UtentePerProfiloDTO {


    private Long idApplicazione;

    @JsonProperty("idUtente")
    private Long idUtente;

    @JsonProperty("idRuolo")
    private Long idProfilo;

    @JsonProperty("idNodo")
    private Long idNodo;

    @JsonProperty("ruoloDiDefault")
    private String ruoloDiDefault = "N";

    @JsonProperty("pmApplicazioniDto")
    private ApplicazioneDTO applicazione;

    @JsonProperty("pmRuoliDto")
    private ProfiloDTO profilo;

    @JsonProperty("pmUtentiDto")
    private UtenteDTO utente;

    @JsonProperty("pmNodiPiantaOrganicaDto")
    private NodoStrutturaDTO nodoStruttura;






}