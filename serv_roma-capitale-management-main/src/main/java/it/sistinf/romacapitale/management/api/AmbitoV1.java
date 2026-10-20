package it.sistinf.romacapitale.management.api;


import io.swagger.v3.oas.annotations.Operation;
import it.sistinf.romacapitale.core.api.AbstractSqlAPI;
import it.sistinf.romacapitale.core.dto.RequestListDTO;
import it.sistinf.romacapitale.core.dto.ResponseDTO;
import it.sistinf.romacapitale.core.dto.ResponseListDTO;
import it.sistinf.romacapitale.integration.management.vo.AmbitoVO;
import it.sistinf.romacapitale.management.domain.AmbitoDomain;
import jakarta.validation.Valid;
import lombok.AllArgsConstructor;

import java.util.List;

import org.springframework.web.bind.annotation.*;

@RestController
@AllArgsConstructor
@RequestMapping("/api/v1/ambito")
public class AmbitoV1 extends AbstractSqlAPI {

    private final AmbitoDomain ambitoDomain;

    @Operation(summary = "Lista ambiti", description = "Restituisce la lista degli ambiti delle applicazioni di Roma Capitale")
    @GetMapping("/list")
    public ResponseListDTO<AmbitoVO> listAmbiti(  
            @RequestParam(value = "filters", required = false) List<String> filtersList,
            @RequestParam(value = "sort", required = false) List<String> sortList,
            @RequestParam(value = "pageOffset", required = false) Integer pageOffset,
            @RequestParam(value = "pageSize", required = false) Integer pageSize){
        
            RequestListDTO<AmbitoVO> request = makePaginatedSearchRequest(filtersList, sortList, pageOffset, pageSize);
        
            return ambitoDomain.listAmbiti(request);
    }

    @Operation(summary = "Ricerca ambito per id", description = "Ricerca di un ambito di Roma Capitale per id")
    @GetMapping("/{codice}")
    public ResponseDTO<AmbitoVO> getAmbito(@PathVariable String codice) {
        AmbitoVO resp = ambitoDomain.getAmbito(codice);
        return new ResponseDTO<>(resp);
    }

    @Operation(summary = "Creazione Ambito", description = "Creazione nuovo Ambito")
    @PostMapping("/")
    public ResponseDTO<AmbitoVO> createAmbito(@RequestBody AmbitoVO request) {
        AmbitoVO resp = ambitoDomain.createAmbito(request);
        return new ResponseDTO<>(resp);
    }

    @Operation(summary = "Modifica Ambito", description = "Modifica di un Ambito")
    @PutMapping("/{codice}")
    public ResponseDTO<AmbitoVO> updateAmbito(
            @Valid @RequestBody AmbitoVO request,
            @PathVariable String codice) {
        request.setKey(codice);
        AmbitoVO response = ambitoDomain.updateAmbito(request);
        return new ResponseDTO<>(response);
    }

    @Operation(summary = "Cancellazione Ambito", description = "Cancellazione di un Ambito")
    @DeleteMapping("/{codice}")
    public ResponseDTO<AmbitoVO> deleteAmbito(@PathVariable String codice) {
        AmbitoVO response = ambitoDomain.deleteAmbito(codice);
        return new ResponseDTO<>(response);
    }

}
