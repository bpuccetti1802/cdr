package it.sistinf.romacapitale.management.pman.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonRootName;
import io.swagger.v3.oas.annotations.media.Schema;
import it.sistinf.romacapitale.integration.management.vo.AbilitazioneVO;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.ToString;

@Data
@ToString
@NoArgsConstructor
@JsonRootName("PmRuoliMicrofunzioniDTO")
public class ProfiloPerAbilitazioneDTO {

    @JsonProperty("idApplicazione")
    private Long idApplicazione;

    @JsonProperty("idMicrofunzione")
    private Long idAbilitazione;

    @JsonProperty("idRuolo")
    private Long idProfilo;

    @JsonProperty("pmMicrofunzioniDto")
    private AbilitazioneDTO abilitazione;

    @JsonProperty("pmRuoliDto")
    private ProfiloDTO profilo;


}
