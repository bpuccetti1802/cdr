package it.sistinf.romacapitale.management.api;

import io.swagger.v3.oas.annotations.Operation;
import it.sistinf.romacapitale.core.api.AbstractSqlAPI;
import it.sistinf.romacapitale.core.dto.RequestListDTO;
import it.sistinf.romacapitale.core.dto.ResponseDTO;
import it.sistinf.romacapitale.core.dto.ResponseListDTO;
import it.sistinf.romacapitale.integration.management.vo.AbilitazioneVO;
import it.sistinf.romacapitale.management.domain.AbilitazioneDomain;
import jakarta.validation.Valid;
import lombok.AllArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@AllArgsConstructor
@RequestMapping("/api/v1/abilitazione")
public class AbilitazioneAPIV1 extends AbstractSqlAPI {

    private final AbilitazioneDomain abilitazioneDomain;

    @Operation(summary = "Lista abilitazioni", description = "Restituisce la Lista delle abilitazoni")
    @GetMapping("/list")
    public ResponseListDTO<AbilitazioneVO> listAbilitazioni(
            @RequestParam(value = "filters", required = false) List<String> filtersList,
            @RequestParam(value = "sort", required = false) List<String> sortList,
            @RequestParam(value = "pageOffset", required = false) Integer pageOffset,
            @RequestParam(value = "pageSize", required = false) Integer pageSize
    ) {
        RequestListDTO<AbilitazioneVO> request = makePaginatedSearchRequest(filtersList, sortList, pageOffset, pageSize);
        ResponseListDTO<AbilitazioneVO> response = abilitazioneDomain.listAbilitazioni(request);
        return response;
    }

    @Operation(summary = "Get Abilitazione", description = "Restituisce l'abilitazione")
    @GetMapping("/{id}")
    public ResponseDTO<AbilitazioneVO> getAbilitazioneById(@PathVariable Long id) {
        AbilitazioneVO response = abilitazioneDomain.getAbilitazioneById(id);
        return new ResponseDTO<>(response);
    }

    @Operation(summary = "Creazione Abilitazione", description = "Creazione Abilitazione")
    @PostMapping("/")
    public ResponseDTO<AbilitazioneVO> createAbilitazione(@RequestBody AbilitazioneVO request) {
        AbilitazioneVO resp = abilitazioneDomain.createAbilitazione(request);
        return new ResponseDTO<>(resp);
    }


    @Operation(summary = "Modifica Abilitazione", description = "Modifica di un Abilitazione")
    @PutMapping("/{id}")
    public ResponseDTO<AbilitazioneVO> updateAbilitazione(
            @Valid @RequestBody AbilitazioneVO request,
            @PathVariable Long id
    ) {
        request.setKey(id);
        AbilitazioneVO response = abilitazioneDomain.updateAbilitazione(request);
        return new ResponseDTO<>(response);
    }

    @Operation(summary = "Cancellazione Abilitazione", description = "Cancellazione di un Abilitazione")
    @DeleteMapping("/{id}")
    public ResponseDTO<AbilitazioneVO> deleteAbilitazione(@PathVariable Long id) {
        AbilitazioneVO response = abilitazioneDomain.deleteAbilitazione(id);
        return new ResponseDTO<>(response);
    }

}
