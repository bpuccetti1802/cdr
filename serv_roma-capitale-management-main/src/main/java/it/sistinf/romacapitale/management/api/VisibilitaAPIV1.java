package it.sistinf.romacapitale.management.api;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import it.sistinf.romacapitale.core.api.AbstractSqlAPI;
import it.sistinf.romacapitale.core.dto.RequestListDTO;
import it.sistinf.romacapitale.core.dto.ResponseDTO;
import it.sistinf.romacapitale.core.dto.ResponseListDTO;
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
@RequestMapping("/api/v1/visibilita")
@Tag(
    name = "GESTIONE VISIBILITA",
    description = "Da vedere ?*? Gestione update/delete della visibilità del nodo struttura di un operatore (allineamento con base dati SIR)"
)
public class VisibilitaAPIV1 extends AbstractSqlAPI {

    private final VisibilitaDomain visibilitaDomain;

    @Operation(
        summary = "Update dati di visibilità",
        description = "Endpoint di update visiblità"
    )
    @PutMapping("/update")
    public ResponseDTO<Void> updateVisibilita(@RequestBody VisibilitaVO request) {
        visibilitaDomain.updateVisibilita(request);
        return new ResponseDTO<>();
    }

    @Operation(
        summary = "Delete dati di visibilità",
        description = "Endpoint di delete visiblità"
    )
    @DeleteMapping("/delete/{id}")
    public ResponseDTO<Void> deleteVisibilita(@PathVariable Long id) {
        visibilitaDomain.deleteVisibilitaById(id);
        return new ResponseDTO<>();
    }

    @Operation(
        summary = "Recupera visibilità filtrata",
        description = "Endpoint di recupero lista di visiblità filtrata"
    )
    @GetMapping("/list")
    public ResponseListDTO<VisibilitaVO> listVisibilita(
            @RequestParam(value = "filters", required = false) List<String> filtersList,
            @RequestParam(value = "sort", required = false) List<String> sortList,
            @RequestParam(value = "pageOffset", required = false) Integer pageOffset,
            @RequestParam(value = "pageSize", required = false) Integer pageSize
    ){
        RequestListDTO<VisibilitaVO> request = makePaginatedSearchRequest(filtersList, sortList, pageOffset, pageSize);
        return visibilitaDomain.listVisibilita(request);
        
    } 

}
