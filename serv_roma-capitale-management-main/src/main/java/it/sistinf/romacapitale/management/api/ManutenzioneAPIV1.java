package it.sistinf.romacapitale.management.api;
import io.swagger.v3.oas.annotations.Operation;
import it.sistinf.romacapitale.core.api.AbstractSqlAPI;
import it.sistinf.romacapitale.core.dto.ResponseDTO;
import it.sistinf.romacapitale.management.domain.ManutenzioneDomain;
import it.sistinf.romacapitale.management.vo.ManutenzioneVO;
import lombok.AllArgsConstructor;
import org.springframework.web.bind.annotation.*;

@RestController
@AllArgsConstructor
@RequestMapping("/api/v1/manutenzione")
public class ManutenzioneAPIV1 extends AbstractSqlAPI {
    private final ManutenzioneDomain manutenzioneDomain;

    @Operation(summary = "l'applicazione va in manutenzione", description = "Scrive se l'applicazione va in manutenzione")
    @PostMapping("")
    public ResponseDTO<ManutenzioneVO> writeIsInManutenzione(
            @RequestBody() ManutenzioneVO manutenzioneVO
    ) {
        manutenzioneDomain.write(manutenzioneVO.getCdAmbito(), manutenzioneVO.getCdApplicazione(), manutenzioneVO.getManutenzione() || false);
        return new ResponseDTO<>(manutenzioneVO);
    }

    @Operation(summary = "Visualizza applicazione in manutenzione", description = "Recupera l'applicazione in manutenziona da cdAmbito e cdApplicazione")
    @GetMapping("/{cdAmbito}/{cdApplicazione}")
    public ResponseDTO<ManutenzioneVO> getIsInManutenzione(
            @PathVariable String cdAmbito,
            @PathVariable String cdApplicazione
    ) {
        Boolean isInManutenzione =  manutenzioneDomain.read(cdAmbito, cdApplicazione);
        ManutenzioneVO manutenzioneVO = new ManutenzioneVO();
        manutenzioneVO.setCdAmbito(cdAmbito);
        manutenzioneVO.setCdApplicazione(cdApplicazione);
        manutenzioneVO.setManutenzione(isInManutenzione);
        return new ResponseDTO<>(manutenzioneVO);
    }

}
