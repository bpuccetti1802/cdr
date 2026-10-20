package it.sistinf.romacapitale.management.api;

import io.swagger.v3.oas.annotations.Operation;
import it.sistinf.romacapitale.core.api.AbstractSqlAPI;
import it.sistinf.romacapitale.core.dto.RequestListDTO;
import it.sistinf.romacapitale.core.dto.ResponseDTO;
import it.sistinf.romacapitale.core.dto.ResponseListDTO;
import it.sistinf.romacapitale.integration.management.vo.ProfiloVO;
import it.sistinf.romacapitale.management.domain.ProfiloDomain;

import jakarta.validation.Valid;
import lombok.AllArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@AllArgsConstructor
@RequestMapping("/api/v1/profilo")
public class ProfiloAPIV1 extends AbstractSqlAPI {

    private final ProfiloDomain profiloDomain;


    @Operation(summary = "Lista Profili", description = "Restituisce la lista di Profili")
    @GetMapping("/list")
    public ResponseListDTO<ProfiloVO> listProfili(
            @RequestParam(value = "filters", required = false) List<String> filtersList,
            @RequestParam(value = "sort", required = false) List<String> sortList,
            @RequestParam(value = "pageOffset", required = false) Integer pageOffset,
            @RequestParam(value = "pageSize", required = false) Integer pageSize
    ) {
        RequestListDTO<ProfiloVO> request = makePaginatedSearchRequest(filtersList, sortList, pageOffset, pageSize);
        ResponseListDTO<ProfiloVO> response = profiloDomain.listProfili(request);
        return response;
    }

    @Operation(summary = "Profilo", description = "Restituisce il profilo ")
    @GetMapping("/{id}")
    public ResponseDTO<ProfiloVO> profiloById(@PathVariable Long id) {
        ProfiloVO response = profiloDomain.profiloById(id);
        return new ResponseDTO<>(response);
    }

    @Operation(summary = "Creazione Profilo", description = "Creazione nuovo Profilo")
    @PostMapping("/")
    public ResponseDTO<ProfiloVO> createProfilo(@RequestBody ProfiloVO request) {
        ProfiloVO resp = profiloDomain.createProfilo(request);
        return new ResponseDTO<>(resp);
    }


    @Operation(summary = "Modifica Profilo", description = "Modifica di un Profilo")
    @PutMapping("/{id}")
    public ResponseDTO<ProfiloVO> updateProfilo(
            @Valid @RequestBody ProfiloVO request,
            @PathVariable Long id
    ) {
        request.setKey(id);
        ProfiloVO response = profiloDomain.updateProfilo(request);
        return new ResponseDTO<>(response);
    }

    @Operation(summary = "Cancellazione Profilo", description = "Cancellazione di un Profilo")
    @DeleteMapping("/{id}")
    public ResponseDTO<ProfiloVO> deleteUtente(@PathVariable Long id) {
        ProfiloVO response = profiloDomain.deleteProfilo(id);
        return new ResponseDTO<>(response);
    }

}
