package it.sistinf.romacapitale.management.api.internal;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import it.sistinf.romacapitale.core.api.AbstractSqlAPI;
import it.sistinf.romacapitale.core.dto.RequestDTO;
import it.sistinf.romacapitale.core.dto.ResponseDTO;
import it.sistinf.romacapitale.integration.management.vo.VisibilitaVO;
import it.sistinf.romacapitale.management.domain.VisibilitaDomain;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * @author Daniele Inferrera
 * @since 23/10/2025
 */
@RestController
@RequiredArgsConstructor
@RequestMapping("/api/internal/v1/visibilita")
@Tag(
    name = "GESTIONE VISIBILITA",
    description = "Gestione update/delete della visibilità del nodo struttura di un operatore (allineamento con base dati SIR)"
)
public class VisibilitaInternalV1 extends AbstractSqlAPI {

    private final VisibilitaDomain visibilitaDomain;

    @Operation(
        summary = "Update dati di visibilità",
        description = "Endpoint di update visiblità di un operatore (settore, ufficio, tributo)"
    )
    @PostMapping("/update")
    public ResponseDTO<Void> updateVisibilita(@RequestBody VisibilitaVO request) {
        visibilitaDomain.updateVisibilita(request);
        return new ResponseDTO<>();
    }

    @Operation(
        summary = "Delete dati di visibilità",
        description = "Endpoint di delete visiblità di un operatore (settore, ufficio, tributo)"
    )
    @PostMapping("/delete")
    public ResponseDTO<Void> deleteVisibilita(@RequestBody VisibilitaVO request) {
        visibilitaDomain.deleteVisibilita(request);
        return new ResponseDTO<>();
    }

    @Operation(
        summary = "Recupera visibilità utente",
        description = "Endpoint di recupero di una lista di visiblità di un operatore (settore, ufficio, tributo)"
    )
    @PostMapping("/list")
    public ResponseDTO<List<VisibilitaVO>> listVisibilita(@RequestBody RequestDTO<Void> request) {
        return new ResponseDTO<>(visibilitaDomain.listVisibilita());
    }

}
