package it.sistinf.romacapitale.auth.dto;

import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class ErrorResponseDTO {

    private String error;
    private String errorDescription;

}
