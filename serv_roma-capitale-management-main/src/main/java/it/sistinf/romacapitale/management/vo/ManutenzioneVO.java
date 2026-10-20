package it.sistinf.romacapitale.management.vo;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.NonNull;
import lombok.ToString;

/**
 * Classe EnteVO
 */
@Data
@ToString
@NoArgsConstructor
@Schema(description = "Manutenzione")
public class ManutenzioneVO  {

    @Schema(description = "codice ambito")
    @NonNull
    private String cdAmbito;

    @Schema(description = "codice applicazione")
    @NonNull
    private String cdApplicazione;


    @Schema(description = "manutenzione attiva o meno")
    private Boolean manutenzione;
}