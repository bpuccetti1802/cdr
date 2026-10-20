package it.sistinf.romacapitale.management.pman.dto;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonProperty;
import io.swagger.v3.oas.annotations.media.Schema;
import it.sistinf.romacapitale.core.vo.AbstractKeyedVO;
import it.sistinf.romacapitale.integration.management.vo.NodoPerVisibilitaKeyVO;
import it.sistinf.romacapitale.integration.management.vo.VisibilitaVO;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import lombok.ToString;


@Data
@ToString
@NoArgsConstructor
public class NodoPerVisibilitaDTO {

    private Long idNodo;

    private Long idVisibilita;

    private VisibilitaDTO visibilita;

}
