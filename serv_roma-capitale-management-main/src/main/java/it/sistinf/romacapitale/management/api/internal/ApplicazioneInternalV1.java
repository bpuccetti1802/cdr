package it.sistinf.romacapitale.management.api.internal;

import io.swagger.v3.oas.annotations.Operation;
import it.sistinf.romacapitale.core.api.AbstractSqlAPI;
import it.sistinf.romacapitale.core.dto.ResponseDTO;
import it.sistinf.romacapitale.integration.management.vo.ApplicazioneVO;
import it.sistinf.romacapitale.management.domain.ApplicazioneDomain;
import it.sistinf.romacapitale.management.entity.ApplicazioneEntityPK;
import lombok.AllArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@AllArgsConstructor
@RequestMapping("/api/internal/v1/applicazione")
public class ApplicazioneInternalV1 extends AbstractSqlAPI {

    private final ApplicazioneDomain applicazioneDomain;

    @GetMapping("/{cdAmbito}/{cdApplicazione}")
    public ResponseDTO<ApplicazioneVO> getApplicazione(
            @PathVariable String cdAmbito,
            @PathVariable String cdApplicazione)
    {
        ApplicazioneEntityPK id = new ApplicazioneEntityPK(cdAmbito, cdApplicazione);
        ApplicazioneVO resp = applicazioneDomain.getApplicazione(id);
        return new ResponseDTO<>(resp);
    }

    @GetMapping("/{cdApplicazione}")
    public ResponseDTO<ApplicazioneVO> getApplicazioneFromCdApplicazione(@PathVariable String cdApplicazione) {
        ApplicazioneVO resp = applicazioneDomain.getApplicazioneFromCdApplicazione(cdApplicazione);
        return new ResponseDTO<>(resp);
    }

    @Operation(summary = "Ricerca applicazione per context root", description = "Ricerca di un'applicazione di Roma Capitale per context root")
    @GetMapping("/context-root/{contextRoot}")
    public ResponseDTO<ApplicazioneVO> getApplicazioneFromContextRoot(@PathVariable String contextRoot) {
        ApplicazioneVO resp = applicazioneDomain.getApplicazioneFromContextRoot(contextRoot);
        return new ResponseDTO<>(resp);
    }

}
