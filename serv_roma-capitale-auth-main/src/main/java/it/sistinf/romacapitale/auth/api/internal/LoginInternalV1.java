package it.sistinf.romacapitale.auth.api.internal;

import io.swagger.v3.oas.annotations.Operation;
import it.sistinf.romacapitale.auth.domain.LoginDomain;
import it.sistinf.romacapitale.core.api.AbstractSqlAPI;
import it.sistinf.romacapitale.core.dto.RequestDTO;
import it.sistinf.romacapitale.core.dto.ResponseDTO;
import it.sistinf.romacapitale.integration.auth.vo.InputLoginUtenteTecnicoVO;
import it.sistinf.romacapitale.integration.auth.vo.UtenteTecnicoVO;
import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@Slf4j
@AllArgsConstructor
@RestController
@RequestMapping("/api/internal/v1/loginTecnico")
public class LoginInternalV1 extends AbstractSqlAPI {

    private LoginDomain loginDomain;

    @PostMapping("/")
    @Operation(summary = "Login utente tecnico", description = "Login interno per utenti tecnici")
    public ResponseDTO<UtenteTecnicoVO> loginUtenteTecnico(@RequestBody RequestDTO<InputLoginUtenteTecnicoVO> request) {
        UtenteTecnicoVO response = loginDomain.loginUtenteTecnico(
                request.getPayload().getTipoUtenteTecnico(),
                request.getHeader().getCdAmbito(),
                request.getHeader().getCdApplicazione()
        );
        return new ResponseDTO<>(response);
    }

}
