package it.sistinf.romacapitale.management.api;


import io.swagger.v3.oas.annotations.Operation;
import it.sistinf.romacapitale.core.api.AbstractSqlAPI;
import it.sistinf.romacapitale.core.dto.RequestListDTO;
import it.sistinf.romacapitale.core.dto.ResponseDTO;
import it.sistinf.romacapitale.core.dto.ResponseListDTO;
import it.sistinf.romacapitale.integration.management.vo.RicercaApplicazioneVO;
import it.sistinf.romacapitale.management.domain.ApplicazioneDomain;
import it.sistinf.romacapitale.management.entity.ApplicazioneEntityPK;
import it.sistinf.romacapitale.integration.management.vo.ApplicazioneVO;
import it.sistinf.romacapitale.integration.management.vo.ApplicazioneKeyVO;
import jakarta.validation.Valid;
import lombok.AllArgsConstructor;
import org.springframework.core.io.Resource;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@AllArgsConstructor
@RequestMapping("/api/v1/applicazione")
public class ApplicazioneAPIV1 extends AbstractSqlAPI {

    private final ApplicazioneDomain applicazioneDomain;

    @Operation(summary = "Lista applicazioni", description = "Restituisce la lista delle applicazioni di Roma Capitale")
    @GetMapping("/list")
    public ResponseListDTO<ApplicazioneVO> listApplicazione(
            @RequestParam(value = "filters", required = false) List<String> filtersList,
            @RequestParam(value = "sort", required = false) List<String> sortList,
            @RequestParam(value = "pageOffset", required = false) Integer pageOffset,
            @RequestParam(value = "pageSize", required = false) Integer pageSize
    ){
        RequestListDTO<ApplicazioneVO> request = makePaginatedSearchRequest(filtersList, sortList, pageOffset, pageSize);
        return applicazioneDomain.listApplicazioni(request);
    }

    @Operation(summary = "Ricerca applicazione per id", description = "Ricerca di un'applicazione di Roma Capitale per id")
    @GetMapping("/{cdAmbito}/{cdApplicazione}")
    public ResponseDTO<ApplicazioneVO> getApplicazione(@PathVariable String cdAmbito, @PathVariable String cdApplicazione) {
        ApplicazioneEntityPK id = new ApplicazioneEntityPK(cdAmbito, cdApplicazione);
        ApplicazioneVO resp = applicazioneDomain.getApplicazione(id);
        return new ResponseDTO<>(resp);
    }

    @Operation(summary = "Ricerca applicazione per context root", description = "Ricerca di un'applicazione di Roma Capitale per context root")
    @GetMapping("/context-root/{contextRoot}")
    public ResponseDTO<ApplicazioneVO> getApplicazioneFromContextRoot(@PathVariable String contextRoot) {
        ApplicazioneVO resp = applicazioneDomain.getApplicazioneFromContextRoot(contextRoot);
        return new ResponseDTO<>(resp);
    }

    @Operation(summary = "Ricerca applicazione", description = "Ricerca di una o più applicazioni tramite parametri di ricerca")
    @PostMapping("/ricerca")
    public ResponseListDTO<ApplicazioneVO> getApplicazioni(@Valid @RequestBody RicercaApplicazioneVO request) {
        ResponseListDTO<ApplicazioneVO> response = new ResponseListDTO<>();
        response.setList(applicazioneDomain.getApplicazioneByParams(request));
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

    @Operation(summary = "Inserimento applicazione", description = "Inserimento di una applicazione")
    @PostMapping("/")
    public ResponseDTO<ApplicazioneVO> createApplicazione(@Valid @RequestBody ApplicazioneVO request) {
        return new ResponseDTO<>(applicazioneDomain.createApplicazione(request));
    }

    @Operation(summary = "Modifica applicazione", description = "Modifica di una applicazione")
    @PutMapping("/")
    public ResponseDTO<ApplicazioneVO> updateApplicazione(@Valid @RequestBody ApplicazioneVO request) {
        return new ResponseDTO<>(applicazioneDomain.updateApplicazione(request));
    }

    @Operation(summary = "Cancellazione applicazione", description = "Cancellazione di una applicazione tramite id")
    @DeleteMapping("/{cdAmbito}/{cdApplicazione}")
    public ResponseDTO<Boolean> deleteApplicazione(@PathVariable String cdAmbito, @PathVariable String cdApplicazione) {

        return new ResponseDTO<>(applicazioneDomain.deleteApplicazione(new ApplicazioneKeyVO(cdAmbito, cdApplicazione)));
    }
}
