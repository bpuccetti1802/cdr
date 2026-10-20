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
@JsonRootName("PmFiltriDTO")
public class VisibilitaDTO {


    @JsonProperty("idFiltro")
    private Long id;

    @JsonProperty("colonna")
    private String nmColonna;

    @JsonProperty("descBreve")
    private String dsBreve;

    @JsonProperty("descrizione")
    private String dsVisibilita;

    @JsonProperty("valore")
    private String dsValore;

    @JsonProperty("lstPmNodiPiantaOrganicaDto")
    private List<NodoStrutturaDTO> lstPmNodiPiantaOrganicaDto;



}
