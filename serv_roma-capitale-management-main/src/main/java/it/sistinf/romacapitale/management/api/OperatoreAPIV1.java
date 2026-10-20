package it.sistinf.romacapitale.management.api;

import io.swagger.v3.oas.annotations.Operation;
import it.sistinf.romacapitale.core.api.AbstractSqlAPI;
import it.sistinf.romacapitale.core.dto.ResponseDTO;
import it.sistinf.romacapitale.integration.management.vo.requestVO.OperatoreRequestVO;
import it.sistinf.romacapitale.management.domain.OperatoreDomain;
import it.sistinf.romacapitale.integration.management.vo.OperatoreVO;
import it.sistinf.romacapitale.management.pman.dto.OperatoreDTO;
import jakarta.validation.Valid;
import lombok.AllArgsConstructor;
import org.springframework.web.bind.annotation.*;

@RestController
@AllArgsConstructor
@RequestMapping("/api/v1/operatore")
public class OperatoreAPIV1 extends AbstractSqlAPI {

    private OperatoreDomain operatoreDomain;

    /**
     * Consente il recupero delle funzioni di un operatore specifico
     * @param request body in ingresso contenente i dati dell'operatore
     * @return {@link OperatoreVO} dati dell'operatore
     */
    @Operation(summary = "Funzioni operatore", description = "servizio che restituisce l'Operatore e tutte le sue funzioni")
    @PostMapping("/funzioni")
    public ResponseDTO<OperatoreVO> getOperatoreAndFunzioni(@Valid @RequestBody OperatoreRequestVO request) {
        OperatoreVO response = operatoreDomain.getOperatoreAndFunzioni(request);
        return new ResponseDTO<>(response);
    }

    @Operation(summary = "Funzioni operatore", description = "servizio che restituisce l'Operatore e tutte le sue funzioni")
    @GetMapping("/funzioni")
    public ResponseDTO<OperatoreDTO> getFunzioniOperatore() {
        OperatoreDTO response = operatoreDomain.getFunzioniOperatore();
        return new ResponseDTO<>(response);
    }



}
