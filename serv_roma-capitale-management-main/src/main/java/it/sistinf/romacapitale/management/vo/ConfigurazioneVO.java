package it.sistinf.romacapitale.management.vo;

import io.swagger.v3.oas.annotations.media.Schema;
import it.sistinf.romacapitale.core.vo.AbstractKeyedVO;
import it.sistinf.romacapitale.integration.management.vo.ApplicazioneVO;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import lombok.ToString;

import java.io.Serial;

@Data
@ToString
@NoArgsConstructor
@EqualsAndHashCode(callSuper = true)
@Schema(description = "Configurazione")
public class ConfigurazioneVO extends AbstractKeyedVO<ConfigurazioneKeyVO> {

    @Serial
    private static final long serialVersionUID = 1L;

    @Schema (description = "Valore del parametro")
    private String desValParametro;

    @Schema ( description = "Tipo parametro: \"S\"=String, \"I\"=Integer, \"B\"=Boolean")
    private String tyParametro;

    private ApplicazioneVO applicazione;
}
