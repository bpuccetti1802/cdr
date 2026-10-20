package it.sistinf.romacapitale.management.api.unauthenticated;

import io.swagger.v3.oas.annotations.Operation;
import it.sistinf.romacapitale.core.api.AbstractSqlAPI;
import it.sistinf.romacapitale.core.dto.RequestListDTO;
import it.sistinf.romacapitale.core.dto.ResponseListDTO;
import it.sistinf.romacapitale.integration.management.vo.AvvisoVO;
import it.sistinf.romacapitale.management.domain.ApplicazioneDomain;
import it.sistinf.romacapitale.management.domain.AvvisoDomain;
import lombok.AllArgsConstructor;
import org.springframework.core.io.Resource;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@AllArgsConstructor
@RequestMapping("/api/util/non-autenticato")
public class UnauthenticatedAPIV1 extends AbstractSqlAPI {
    private final ApplicazioneDomain applicazioneDomain;
    private final AvvisoDomain avvisoDomain;

    @Operation(summary = "Restituisce il manuale utente", description = "Restituisce il manuale di un utente")
    @GetMapping("/getManuale")
    public ResponseEntity<Resource> getManualeUtente(
            @RequestParam("cdAmbito") String cdAmbito,
            @RequestParam("cdApplicazione") String cdApplicazione
    ) {
        return applicazioneDomain.getManualeUtente(cdAmbito, cdApplicazione);
    }

    @Operation(summary = "Visualizza avvisi attivi", description = "Recupera gli avvisi attivi per ambito e applicazione")
    @GetMapping("/avvisi/attivi/{cdAmbito}/{cdApplicazione}")
    public ResponseListDTO<AvvisoVO> getAvvisiAttivi(
        @PathVariable String cdAmbito,
        @PathVariable String cdApplicazione,
        @RequestParam(value = "filters", required = false) List<String> filtersList,
        @RequestParam(value = "sort", required = false) List<String> sortList,
        @RequestParam(value = "pageOffset", required = false) Integer pageOffset,
        @RequestParam(value = "pageSize", required = false) Integer pageSize
    ) {
        RequestListDTO<AvvisoVO> request = makePaginatedSearchRequest(filtersList, sortList, pageOffset, pageSize);
        return avvisoDomain.getAvvisiAttivi(cdAmbito, cdApplicazione, request);
    }

}
