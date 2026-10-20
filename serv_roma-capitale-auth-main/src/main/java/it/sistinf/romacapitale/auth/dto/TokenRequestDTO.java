package it.sistinf.romacapitale.auth.dto;

import lombok.Data;
import org.apache.logging.log4j.core.config.plugins.validation.constraints.NotBlank;

@Data
public class TokenRequestDTO {

    @NotBlank
    private String grantType;

    @NotBlank
    private String clientId;

    @NotBlank
    private String clientSecret;

    @NotBlank
    private String scope;

}
