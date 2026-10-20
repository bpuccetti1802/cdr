package it.sistinf.romacapitale.management.pman.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonRootName;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.ToString;

import java.util.List;

@Data
@ToString
@NoArgsConstructor
@JsonRootName("PmMacrofunzioniDTO")
public class MenuDTO {


    @JsonProperty("idApplicazione")
    private Long idApplicazioneSa;

    @JsonProperty("idMacrofunzione")
    private Long id;

    @JsonProperty("codice")
    private String cdMenu;

    @JsonProperty("descrizione")
    private String dsMenu;

    @JsonProperty("pmApplicazioniDto")
    private ApplicazioneDTO applicazione;

    @JsonProperty("lstPmMicrofunzioniDto")
    private List<AbilitazioneDTO> abilitazione;


}
