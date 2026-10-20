package it.sistinf.romacapitale.management.pman.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonRootName;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.ToString;

import java.sql.Timestamp;


/**
 * Classe EnteVO
 */
@Data
@ToString
@NoArgsConstructor
@JsonRootName("PmEnteDTO")
public class EnteDTO {

    @JsonProperty("pkEnte")
    private Long id;

    @JsonProperty("codEnte")
    private String cdEnte;

    @JsonProperty("desEnte")
    private String dsEnte;

    @JsonProperty("tmsIns")
    private Timestamp tmsIns;

    @JsonProperty("tmsVar")
    private Timestamp tmsVar;

    @JsonProperty("uteIns")
    private String uteIns;

    @JsonProperty("uteVar")
    private String uteVar;


}
