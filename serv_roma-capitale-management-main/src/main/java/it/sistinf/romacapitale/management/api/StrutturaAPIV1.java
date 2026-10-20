package it.sistinf.romacapitale.management.api;

import io.swagger.v3.oas.annotations.Operation;
import it.sistinf.romacapitale.core.api.AbstractSqlAPI;
import it.sistinf.romacapitale.core.dto.RequestListDTO;
import it.sistinf.romacapitale.core.dto.ResponseDTO;
import it.sistinf.romacapitale.core.dto.ResponseListDTO;
import it.sistinf.romacapitale.integration.management.vo.StrutturaVO;
import it.sistinf.romacapitale.management.domain.StrutturaDomain;
import jakarta.validation.Valid;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@AllArgsConstructor
@RequestMapping("/api/v1/struttura")
public class StrutturaAPIV1 extends AbstractSqlAPI {

    private final StrutturaDomain strutturaDomain;

    @Operation(summary = "Elenco strutture", description = "Restituisce l'elenco delle strutture in base ai filtri, ordinamenti e paginazione specificati")
    @GetMapping("/list")
    public ResponseListDTO<StrutturaVO> listStrutture(
            @RequestParam(value = "filters", required = false) List<String> filtersList,
            @RequestParam(value = "sort", required = false) List<String> sortList,
            @RequestParam(value = "pageOffset", required = false) Integer pageOffset,
            @RequestParam(value = "pageSize", required = false) Integer pageSize
    ) {
        RequestListDTO<StrutturaVO> request = makePaginatedSearchRequest(filtersList, sortList, pageOffset, pageSize);
        return strutturaDomain.listStrutture(request);
    }

    @Operation(summary = "Interrogazione Struttura", description = "Interrogazione di una struttura per id")
    @GetMapping("/{id}")
    public ResponseDTO<StrutturaVO> getStruttura(@PathVariable @NotNull Long id) {
        return new ResponseDTO<>(strutturaDomain.getStruttura(id));
    }

    @Operation(summary = "Inserimento Struttura", description = "Inserimento di una struttura")
    @PostMapping("/")
    public ResponseDTO<StrutturaVO> createStruttura(@Valid @RequestBody StrutturaVO request) {
        return new ResponseDTO<>(strutturaDomain.createStruttura(request));
    }

    @Operation(summary = "Modifica Struttura", description = "Modifica di una struttura")
    @PutMapping("/{id}")
    public ResponseDTO<StrutturaVO> updateStruttura(@PathVariable Long id, @Valid @RequestBody StrutturaVO request) {
        request.setKey(id);
        return new ResponseDTO<>(strutturaDomain.updateStruttura(request));
    }

    @Operation(summary = "Cancellazione Struttura", description = "Cancellazione di una struttura")
    @DeleteMapping("/{id}")
    public ResponseDTO<Boolean> deleteStruttura(@PathVariable Long id) {
        return new ResponseDTO<>(strutturaDomain.deleteStruttura(id));
    }
}

