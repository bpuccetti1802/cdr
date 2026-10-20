package it.sistinf.romacapitale.management.api;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import it.sistinf.romacapitale.core.api.AbstractSqlAPI;
import it.sistinf.romacapitale.core.dto.RequestListDTO;
import it.sistinf.romacapitale.core.dto.ResponseDTO;
import it.sistinf.romacapitale.core.dto.ResponseListDTO;
import it.sistinf.romacapitale.integration.management.vo.AvvisoVO;
import it.sistinf.romacapitale.management.domain.AvvisoDomain;
import jakarta.validation.Valid;
import lombok.AllArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@AllArgsConstructor
@RequestMapping("/api/v1/avviso")
@Tag(name = "Avviso API", description = "API interne per la gestione degli avvisi")
public class AvvisoV1 extends AbstractSqlAPI {

    private final AvvisoDomain avvisoDomain;

    @Operation(summary = "Lista Avvisi", description = "Restituisce la lista di Avvisi")
    @GetMapping("/list")
    public ResponseListDTO<AvvisoVO> listAvvisi(
        @RequestParam(value = "filters", required = false) List<String> filtersList,
        @RequestParam(value = "sort", required = false) List<String> sortList,
        @RequestParam(value = "pageOffset", required = false) Integer pageOffset,
        @RequestParam(value = "pageSize", required = false) Integer pageSize
    ) {
        RequestListDTO<AvvisoVO> request = makePaginatedSearchRequest(filtersList, sortList, pageOffset, pageSize);
        return avvisoDomain.listAvvisi(request);
    }

    @Operation(summary = "Avviso", description = "Restituisce l'avviso per ID")
    @GetMapping("/{id}")
    public ResponseDTO<AvvisoVO> avvisoById(@PathVariable Long id) {
        AvvisoVO response = avvisoDomain.avvisoById(id);
        return new ResponseDTO<>(response);
    }

    @Operation(summary = "Creazione Avviso", description = "Creazione nuovo Avviso")
    @PostMapping("/create")
    public ResponseDTO<AvvisoVO> createAvviso(@RequestBody AvvisoVO request) {
        AvvisoVO resp = avvisoDomain.createAvviso(request);
        return new ResponseDTO<>(resp);
    }

    @Operation(summary = "Modifica Avviso", description = "Modifica di un Avviso")
    @PutMapping("/{id}")
    public ResponseDTO<AvvisoVO> updateAvviso(
        @Valid @RequestBody AvvisoVO request,
        @PathVariable Long id
    ) {
        request.setKey(id);
        AvvisoVO response = avvisoDomain.updateAvviso(request);
        return new ResponseDTO<>(response);
    }

    @Operation(summary = "Cancellazione Avviso", description = "Cancellazione di un Avviso")
    @DeleteMapping("/{id}")
    public ResponseDTO<AvvisoVO> deleteAvviso(@PathVariable Long id) {
        AvvisoVO response = avvisoDomain.deleteAvviso(id);
        return new ResponseDTO<>(response);
    }

    @Operation(summary = "Attiva Avviso", description = "Attiva un avviso esistente")
    @PatchMapping("/{id}/attiva")
    public ResponseDTO<AvvisoVO> enableAvviso(@PathVariable Long id) {
        AvvisoVO response = avvisoDomain.enableAvviso(id);
        return new ResponseDTO<>(response);
    }

    @Operation(summary = "Disattiva Avviso", description = "Disattiva un avviso esistente")
    @PatchMapping("/{id}/disattiva")
    public ResponseDTO<AvvisoVO> disableAvviso(@PathVariable Long id) {
        AvvisoVO response = avvisoDomain.disableAvviso(id);
        return new ResponseDTO<>(response);
    }
}