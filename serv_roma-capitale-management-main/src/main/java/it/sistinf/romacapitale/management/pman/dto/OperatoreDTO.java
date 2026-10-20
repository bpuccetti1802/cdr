package it.sistinf.romacapitale.management.pman.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonRootName;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.ToString;

import java.util.List;
import java.util.Map;

/**
 * Classe OperatoreVO
 */
@Data
@ToString
@NoArgsConstructor
@AllArgsConstructor
@JsonRootName("OperatoreDTO")
public class OperatoreDTO {

    @JsonProperty("pmUtenteDto")
    private UtenteDTO utente;

    @JsonProperty("idApplicazione")
    private Long idApplicazioneSa;

    @JsonProperty("idRuolo")
    private Long idProfilo;

    @JsonProperty("lstCodEsterno")
    private String lstCodEsterno;

    @JsonProperty("lstPmPreferitiDto")
    private List<PmPreferitiDTO> lstPmPreferitiDto;

    @JsonProperty("mFiltriOperatore")
    private Map<String, String> visibilitaOperatore;


}
