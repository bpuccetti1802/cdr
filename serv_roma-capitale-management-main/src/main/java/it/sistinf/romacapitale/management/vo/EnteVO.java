package it.sistinf.romacapitale.management.vo;

import io.swagger.v3.oas.annotations.media.Schema;
import it.sistinf.romacapitale.core.vo.AbstractKeyedVO;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import lombok.ToString;

import java.util.Date;


/**
 * Classe EnteVO
 */
@Data
@ToString
@NoArgsConstructor
@EqualsAndHashCode(callSuper = true)
@Schema(description = "Ente")
public class EnteVO extends AbstractKeyedVO<Long> {

    @Schema(description = "codice ente")
    private Long cdEnte;

    @Schema(description = "descrizione ente")
    private String dsEnte;

}
