package it.sistinf.romacapitale.management.pman.dto;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonRootName;
import io.swagger.v3.oas.annotations.media.Schema;
import it.sistinf.romacapitale.integration.management.vo.ApplicazioneVO;
import it.sistinf.romacapitale.integration.management.vo.MenuVO;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.ToString;


@Data
@ToString
@NoArgsConstructor
@JsonRootName("PmMicrofunzioniDTO")
public class AbilitazioneDTO {

    @JsonProperty("idApplicazione")
    private Long idApplicazione;

    @JsonIgnore
    private String cdAmbito;

    @JsonIgnore
    private String cdApplicazione;

    @JsonProperty("idMicrofunzione")
    private Long id;

    @JsonProperty("codEsterno")
    private String cdEsterno;

    @JsonProperty("codice")
    private String cdAbilitazione;

    @JsonProperty("descrizione")
    private String descAbilitazione;

    @JsonProperty("pmMacrofunzioniDto")
    private MenuDTO menu;

    @JsonIgnore
    private Long idMenu;

    @JsonIgnore
    private ApplicazioneDTO applicazione;


}