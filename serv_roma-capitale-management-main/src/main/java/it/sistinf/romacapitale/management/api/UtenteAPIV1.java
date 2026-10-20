package it.sistinf.romacapitale.management.api;

import io.swagger.v3.oas.annotations.Operation;
import it.sistinf.romacapitale.core.api.AbstractSqlAPI;
import it.sistinf.romacapitale.core.dto.RequestListDTO;
import it.sistinf.romacapitale.core.dto.ResponseDTO;
import it.sistinf.romacapitale.core.dto.ResponseListDTO;
import it.sistinf.romacapitale.integration.management.vo.InserisciUtenteVO;
import it.sistinf.romacapitale.integration.management.vo.ModificaUtenteVO;
import it.sistinf.romacapitale.integration.management.vo.RicercaUtenteVO;
import it.sistinf.romacapitale.integration.management.vo.UtenteVO;
import it.sistinf.romacapitale.management.domain.ApplicazioneDomain;
import it.sistinf.romacapitale.management.domain.UtenteDomain;
import org.springframework.core.io.Resource;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import jakarta.validation.Valid;
import lombok.AllArgsConstructor;

import java.util.List;

@RestController
@AllArgsConstructor
@RequestMapping("/api/v1/utente")
public class UtenteAPIV1 extends AbstractSqlAPI {

    private final UtenteDomain utenteDomain;
    private final ApplicazioneDomain applicazioneDomain;

    @Operation(summary = "Lista utenti", description = "Restituisce la lista utenti")
    @GetMapping("/list")
    public ResponseListDTO<UtenteVO> listUtenti(
            @RequestParam(value = "filters", required = false) List<String> filtersList,
            @RequestParam(value = "sort", required = false) List<String> sortList,
            @RequestParam(value = "pageOffset", required = false) Integer pageOffset,
            @RequestParam(value = "pageSize", required = false) Integer pageSize
    ) {
        RequestListDTO<UtenteVO> request = makePaginatedSearchRequest(filtersList, sortList, pageOffset, pageSize);
        return utenteDomain.listUtenti(request);
    }


    @Operation(summary = "Ricerca Utente", description = "Ricerca di un utente tramite parametri di ricerca")
    @PostMapping("/ricerca")
    public ResponseListDTO<UtenteVO> getUtente(@Valid @RequestBody RicercaUtenteVO request) {
        ResponseListDTO<UtenteVO> response = new ResponseListDTO<>();
        response.setList(utenteDomain.getUtenteByParams(request));
        return response;
    }

    @Operation(summary = "Restituisce il manuale utente", description = "Restituisce il manuale di un utente")
    @GetMapping("/getManuale")
    public ResponseEntity<Resource> getManualeUtente(
            @RequestParam("cdAmbito") String cdAmbito,
            @RequestParam("cdApplicazione") String cdApplicazione
    ) {
        return applicazioneDomain.getManualeUtente(cdAmbito, cdApplicazione);
    }


    @Operation(summary = "Interrogazione Utente", description = "Interrogazione di un utente")
    @GetMapping("/{id}")
    public ResponseDTO<UtenteVO> getUtente(@PathVariable Long id) {
        UtenteVO response = utenteDomain.getUtente(id);
        return new ResponseDTO<>(response);
    }

    @Operation(summary = "Inserimento utente", description = "Inserimento di un utente")
    @PostMapping("/")
    public ResponseDTO<UtenteVO> createUtente(@Valid @RequestBody InserisciUtenteVO request) {
        return new ResponseDTO<>(utenteDomain.createUtente(request));
    }

    @Operation(summary = "Modifica utente", description = "Modifica di un utente")
    @PutMapping("/")
    public ResponseDTO<UtenteVO> updateUtente(@Valid @RequestBody ModificaUtenteVO request) {
        return new ResponseDTO<>( utenteDomain.updateUtente(request));
    }

    @Operation(summary = "Cancellazione utente", description = "Cancellazione di un utente")
    @DeleteMapping("/{id}")
    public ResponseDTO<Boolean> deleteUtente(@PathVariable Long id) {
        return new ResponseDTO<>(utenteDomain.deleteUtente(id));
    }


}
