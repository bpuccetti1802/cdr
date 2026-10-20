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
@JsonRootName("PmPiantaOrganicaDTO")
public class StrutturaDTO {

    @JsonProperty("idPiantaOrganica")
    private Long id;

    @JsonProperty("descrizione")
    private String dsStruttura;

    @JsonProperty("nome")
    private String nmStruttura;

    @JsonProperty("lstPmNodiPiantaOrganicaDto")
    private List<NodoStrutturaDTO> lstPmNodiPiantaOrganicaDto;


}
