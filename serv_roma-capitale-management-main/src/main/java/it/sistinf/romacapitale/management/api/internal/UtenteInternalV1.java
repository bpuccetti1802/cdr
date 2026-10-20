package it.sistinf.romacapitale.management.api.internal;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import it.sistinf.romacapitale.core.api.AbstractSqlAPI;
import it.sistinf.romacapitale.core.dto.RequestDTO;
import it.sistinf.romacapitale.core.dto.ResponseDTO;
import it.sistinf.romacapitale.core.vo.auth.LoginVO;
import it.sistinf.romacapitale.integration.management.vo.InputRecuperaUtentiPerRuoloVO;
import it.sistinf.romacapitale.integration.management.vo.ProfileUserVO;
import it.sistinf.romacapitale.integration.management.vo.UtenteVO;
import it.sistinf.romacapitale.management.domain.UtenteDomain;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequiredArgsConstructor
@RequestMapping("/api/internal/v1/utente")
public class UtenteInternalV1 extends AbstractSqlAPI {

    private final UtenteDomain utenteDomain;

    @Operation(summary = "Interrogazione Utente by Username", description = "Interrogazione Utente by Username")
    @PostMapping(value = "/username")
    public ResponseDTO<ProfileUserVO> getUtenteAndAbilitazioniByUsername(@RequestBody RequestDTO<LoginVO> request) {
        ProfileUserVO resp = utenteDomain.getUtenteAndAbilitazioniByUsername(request.getPayload());
        return new ResponseDTO<>(resp);
    }

    @Operation(summary = "Interrogazione Utente by CodFiscale", description = "Interrogazione Utente by CodFiscale")
    @PostMapping(value = "/cod-fiscale")
    public ResponseDTO<ProfileUserVO> getUtenteAndAbilitazioniByCodFiscale(@RequestBody RequestDTO<LoginVO> request) {
        ProfileUserVO resp = utenteDomain.getUtenteAndAbilitazioniByCodFiscale(request.getPayload());
        return new ResponseDTO<>(resp);
    }

    @Operation(summary = "Modifica utente", description = "Modifica di un utente")
    @PutMapping("/")
    public ResponseDTO<UtenteVO> updateUtenteForLogin(@RequestBody RequestDTO<UtenteVO> request) {
        UtenteVO resp = utenteDomain.updateUtenteForLogin(request.getPayload());
        return new ResponseDTO<>(resp);
    }


    @Parameter(name = "idProfilo", description = "Codice ambito")
    @Operation(summary = "Recupera utenti per ruolo", description = "Recupera utenti con un dato ruolo")
    @PostMapping("/listUtenti")
    public ResponseDTO<List<UtenteVO>> recuperaUtentiPerRuolo(@RequestBody RequestDTO<InputRecuperaUtentiPerRuoloVO> request) {
        return new ResponseDTO<>(utenteDomain.listUtentiPerRuolo(request.getPayload().getIdProfilo()));
    }

    @Operation(summary = "Interrogazione Utente by Username e codStruttura GET", description = "Interrogazione Utente by Username e codStruttura GET")
    @PostMapping(value = "/username-struttura-get")
    public ResponseDTO<ProfileUserVO> getUtenteAndAbilitazioniByUsernameAndStruttura(@RequestBody RequestDTO<LoginVO> request, @RequestParam(name = "codStrutturaGet") String codStrutturaGet) {
        ProfileUserVO resp = utenteDomain.getUtenteAndAbilitazioniByUsernameAndStruttura(request.getPayload(),codStrutturaGet);
        return new ResponseDTO<>(resp);
    }

    @Operation(summary = "Interrogazione Utente by CodFiscale e codStruttura GET", description = "Interrogazione Utente by CodFiscale e codStruttura GET")
    @PostMapping(value = "/cod-fiscale-struttura-get")
    public ResponseDTO<ProfileUserVO> getUtenteAndAbilitazioniByCodFiscaleAndStruttura(@RequestBody RequestDTO<LoginVO> request, @RequestParam(name = "codStrutturaGet") String codStrutturaGet) {
        ProfileUserVO resp = utenteDomain.getUtenteAndAbilitazioniByCodFiscaleAndStruttura(request.getPayload(),codStrutturaGet);
        return new ResponseDTO<>(resp);
    }

}
