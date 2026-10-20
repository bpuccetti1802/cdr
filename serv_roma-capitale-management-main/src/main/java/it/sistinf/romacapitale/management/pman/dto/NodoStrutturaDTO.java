package it.sistinf.romacapitale.management.pman.dto;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonRootName;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.ToString;

import java.util.List;


@Data
@ToString
@NoArgsConstructor
@JsonRootName("PmNodiPiantaOrganicaDTO")
public class NodoStrutturaDTO {


    @JsonProperty("idPiantaOrganica")
    private Long idStruttura;

    @JsonProperty("idNodo")
    private Long id;

    @JsonProperty("codice")
    private String cdNodo;

    @JsonProperty("descrizione")
    private String dsNodo;

    @JsonProperty("nome")
    private String nmNodo;

    @JsonProperty("pmNodoPadre")
    private NodoStrutturaDTO pmNodoPadre;

    @JsonProperty("lstPmNodiPiantaOrganicaDto")
    private List<NodoStrutturaDTO> lstPmNodiPiantaOrganicaDto;

    @JsonProperty("pmPiantaOrganicaDto")
    private StrutturaDTO struttura;

    @JsonProperty("lstPmUtentiRuoliDto")
    private List<UtentePerProfiloDTO> lstPmUtentiRuoliDto;

    @JsonProperty("lstPmFiltriDto")
    private List<VisibilitaDTO> visibilitaList;

    @JsonIgnore
    private Long idNodoPadre;

    @JsonIgnore
    private List<NodoPerVisibilitaDTO> nodoPerVisibilitaList;


}
