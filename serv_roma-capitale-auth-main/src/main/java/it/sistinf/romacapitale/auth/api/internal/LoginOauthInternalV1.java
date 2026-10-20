package it.sistinf.romacapitale.auth.api.internal;

import io.swagger.v3.oas.annotations.Operation;
import it.sistinf.romacapitale.auth.domain.LoginDomain;
import it.sistinf.romacapitale.auth.dto.TokenRequestDTO;
import it.sistinf.romacapitale.integration.auth.vo.TokenRequestVO;
import it.sistinf.romacapitale.integration.auth.vo.TokenResponseDTO;
import it.sistinf.romacapitale.core.api.AbstractSqlAPI;
import it.sistinf.romacapitale.core.dto.RequestDTO;
import it.sistinf.romacapitale.core.dto.ResponseDTO;
import jakarta.validation.Valid;
import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@Slf4j
@AllArgsConstructor
@RestController
@RequestMapping("/api/internal/v1/oauth")
public class LoginOauthInternalV1 extends AbstractSqlAPI {

    private LoginDomain loginDomain;

    @PostMapping("/token")
    @Operation(summary = "Login M2M", description = "Login M2M interno")
    public ResponseDTO<TokenResponseDTO> loginSist(@Valid @RequestBody RequestDTO<TokenRequestVO> request) {
        TokenRequestVO tokenRequestVO = request.getPayload();
        TokenRequestDTO tokenRequestDTO = new TokenRequestDTO();
        tokenRequestDTO.setClientId(tokenRequestVO.getClientId());
        tokenRequestDTO.setClientSecret(tokenRequestVO.getClientSecret());
        tokenRequestDTO.setGrantType(tokenRequestVO.getGrantType());
        tokenRequestDTO.setScope(tokenRequestVO.getScope());
        TokenResponseDTO response = loginDomain.loginSist(tokenRequestDTO);
        return new ResponseDTO<>(response);
    }
}
