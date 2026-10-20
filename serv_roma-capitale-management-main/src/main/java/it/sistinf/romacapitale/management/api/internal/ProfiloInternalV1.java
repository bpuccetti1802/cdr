package it.sistinf.romacapitale.management.api.internal;

import io.swagger.v3.oas.annotations.Operation;
import it.sistinf.romacapitale.core.api.AbstractSqlAPI;
import it.sistinf.romacapitale.core.dto.RequestDTO;
import it.sistinf.romacapitale.core.dto.ResponseDTO;
import it.sistinf.romacapitale.integration.management.vo.ProfiloVO;
import it.sistinf.romacapitale.management.domain.ProfiloDomain;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequiredArgsConstructor
@RequestMapping("/api/internal/v1/profilo")
public class ProfiloInternalV1 extends AbstractSqlAPI {

    private final ProfiloDomain profiloDomain;

    @Operation(summary = "Recupera ruoli profili", description = "Recupera ruoli dei profili di un dato applicativo")
    @PostMapping("/listRuoli")
    public ResponseDTO<List<ProfiloVO>> recuperaRuoli(@RequestBody RequestDTO<Void> request) {
        return new ResponseDTO<>(profiloDomain.recuperaRuoli(request.getHeader().getCdAmbito(), request.getHeader().getCdApplicazione()));
    }

}
