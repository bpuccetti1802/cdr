package it.sistinf.romacapitale.management.api.internal;

import it.sistinf.romacapitale.core.api.AbstractSqlAPI;
import it.sistinf.romacapitale.core.dto.ResponseDTO;
import it.sistinf.romacapitale.management.domain.ConfigurazioneDomain;
import lombok.AllArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;

@RestController
@AllArgsConstructor
@RequestMapping("/api/internal/v1/configurazione")
public class ConfigurazioneInternalV1 extends AbstractSqlAPI {

    private final ConfigurazioneDomain configurazioneDomain;

    @GetMapping("/{cdAmbito}/{cdApplicazione}")
    public ResponseDTO<HashMap<String, String>> getProperties(
            @PathVariable String cdAmbito,
            @PathVariable String cdApplicazione)
    {
        return configurazioneDomain.getProperties(cdAmbito, cdApplicazione);
    }

}
