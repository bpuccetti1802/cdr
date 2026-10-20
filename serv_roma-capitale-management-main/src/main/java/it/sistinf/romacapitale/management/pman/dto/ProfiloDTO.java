package it.sistinf.romacapitale.management.pman.dto;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonRootName;
import io.swagger.v3.oas.annotations.media.Schema;
import it.sistinf.romacapitale.integration.management.vo.ProfiloPerAbilitazioneVO;
import it.sistinf.romacapitale.integration.management.vo.UtentePerProfiloVO;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.ToString;

import java.util.List;


@Data
@ToString
@NoArgsConstructor
@JsonRootName("PmRuoliDTO")
public class ProfiloDTO {

    @JsonProperty("idApplicazione")
    private Long idApplicazione;

    @JsonProperty("idRuolo")
    private Long id;

    @JsonProperty("codiceRuolo")
    private String cdRuoloProfilo;

    @JsonProperty("flgDatiSpecifici")
    private String flgDatiSpecifici;

    @JsonProperty("nomeRuolo")
    private String nomeRuolo;

    @JsonProperty("ruoloDiDefault")
    private String fgProfiloDefault;

    @JsonProperty("valore")
    private Long nmValore;

    @JsonIgnore
    private String cdAmbito;

    @JsonIgnore
    private String cdApplicazione;

    @JsonProperty("pmApplicazioniDto")
    private ApplicazioneDTO pmApplicazioniDto;

//    @JsonProperty("lstPmRuoliMicrofunzioniDto")
    @JsonIgnore
    private List<ProfiloPerAbilitazioneDTO> profiloPerAbilitazioneList;

    @JsonProperty("lstPmUtentiRuoliDto")
    private List<UtentePerProfiloDTO> utentePerProfiloList;

    @JsonProperty("lstPmMicrofunzioniDto")
    private List<AbilitazioneDTO> abilitazioneList;




}