package it.sistinf.romacapitale.management.vo;

import io.swagger.v3.oas.annotations.media.Schema;
import it.sistinf.romacapitale.core.vo.IVO;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.ToString;

import java.io.Serial;

@Data
@ToString
@NoArgsConstructor
@AllArgsConstructor
@Schema(description = "Configurazione key")
public class ConfigurazioneKeyVO implements IVO {

    @Serial
    private static final long serialVersionUID = 1L;

    @Schema (description = "Codice ambito")
    private String cdAmbito;

    @Schema (description = "Codice applicazione")
    private String cdApplicazione;

    @Schema (description = "Nome del parametro")
    private String desNomeParametro;

}
