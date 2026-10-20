package it.sistinf.romacapitale.management.api;

import io.swagger.v3.oas.annotations.Operation;
import it.sistinf.romacapitale.core.api.AbstractSqlAPI;
import it.sistinf.romacapitale.core.dto.RequestListDTO;
import it.sistinf.romacapitale.core.dto.ResponseDTO;
import it.sistinf.romacapitale.core.dto.ResponseListDTO;
import it.sistinf.romacapitale.integration.management.vo.InserisciNodoStrutturaVO;
import it.sistinf.romacapitale.integration.management.vo.NodoStrutturaVO;
import it.sistinf.romacapitale.integration.management.vo.VisibilitaVO;
import it.sistinf.romacapitale.management.domain.NodoStrutturaDomain;
import it.sistinf.romacapitale.management.domain.NodoPerVisibilitaDomain;
import jakarta.validation.Valid;
import lombok.AllArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@AllArgsConstructor
@RequestMapping("/api/v1/nodo-struttura")
public class NodoStrutturaAPIV1 extends AbstractSqlAPI {

    private final NodoStrutturaDomain nodoStrutturaDomain;
    private final NodoPerVisibilitaDomain nodoPerVisibilitaDomain;

    @Operation(summary = "Elenco nodi", description = "Restituisce l'elenco  dei nodi struttura in base ai filtri, ordinamenti e paginazione specificati'")
    @GetMapping("/list")
    public ResponseListDTO<NodoStrutturaVO> elencoNodi(
            @RequestParam(value = "filters", required = false) List<String> filtersList,
            @RequestParam(value = "sort", required = false) List<String> sortList,
            @RequestParam(value = "pageOffset", required = false) Integer pageOffset,
            @RequestParam(value = "pageSize", required = false) Integer pageSize
    ) {
        RequestListDTO<NodoStrutturaVO> request = makePaginatedSearchRequest(filtersList, sortList, pageOffset, pageSize);
        return nodoStrutturaDomain.listNodoStruttura(request);
    }

/* 
    @Operation(summary = "Ricerca nodi", description = "Ricerca i nodi struttura in base ai parametri specificati")
    @PostMapping("/ricerca")
    public ResponseListDTO<NodoStrutturaVO> cercaNodoStruttura(@Valid @RequestBody NodoStrutturaVO request) {
        ResponseListDTO<NodoStrutturaVO> response = new ResponseListDTO<>();
        response.setList(nodoStrutturaDomain.listNodoStrutturaByParams(request));
        return response;
    } */

    @Operation(summary = "Inserimento nodo", description = "Inserimento di un nuovo nodo struttura")
    @PostMapping("/")
    public ResponseDTO<NodoStrutturaVO> creaNodoStruttura(@Valid @RequestBody InserisciNodoStrutturaVO request) {
        return new ResponseDTO<>(nodoStrutturaDomain.createNodoStruttura(request));
    }

    @Operation(summary = "Modifica nodo", description = "Modifica di un nodo struttura esistente")
    @PutMapping("/")
    public ResponseDTO<NodoStrutturaVO> modificaNodoStruttura(@Valid @RequestBody NodoStrutturaVO request) {
        return new ResponseDTO<>( nodoStrutturaDomain.updateNodoStruttura(request));
    }

    @Operation(summary = "Cancellazione nodo", description = "Cancellazione di un nodo struttura esistente")
    @DeleteMapping("/{id}")
    public ResponseDTO<Boolean> deleteUtente(@PathVariable Long id) {
        return new ResponseDTO<>(nodoStrutturaDomain.deleteNodoStruttura(id));
    }

    @Operation(summary = "Visibilità nodo", description = "Restituisce la lista di visibilità associate al nodo")
    @GetMapping("/{id}/visibilita")
    public ResponseDTO<List<VisibilitaVO>> listaVisibilitaNodo(@PathVariable Long id) {
        return new ResponseDTO<>(nodoPerVisibilitaDomain.listVisibilitaByNodo(id));
    }


}
