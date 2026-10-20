package it.sistinf.romacapitale.management.domain;

import it.sistinf.romacapitale.core.domain.AbstractDomain;
import it.sistinf.romacapitale.core.exceptions.ApplicationException;
import it.sistinf.romacapitale.core.messages.EnumMessage;
import it.sistinf.romacapitale.core.utils.ControlloCampi;
import it.sistinf.romacapitale.integration.management.vo.UtentePerProfiloGetVO;
import it.sistinf.romacapitale.management.entity.UtentePerProfiloGetEntity;
import it.sistinf.romacapitale.management.enums.EnumManagementDomainTypeFunction;
import it.sistinf.romacapitale.management.mapper.UtentePerProfiloGetMapper;
import it.sistinf.romacapitale.management.repository.UtentePerProfiloGetRepository;
import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.util.HashMap;
import java.util.List;


@Service
@AllArgsConstructor
@Slf4j
public class UtentePerProfiloGetDomain extends AbstractDomain {

    private UtentePerProfiloGetRepository utentePerProfiloGetRepository;
    private UtentePerProfiloGetMapper utentePerProfiloGetMapper;

    public List<UtentePerProfiloGetVO> listUtentePerProfiloGetByIdUtenteAndCodStruttura(Long idUtente, String codStrutturaGet) throws ApplicationException {

        if (ControlloCampi.campoVuoto(idUtente)) {
            throw new ApplicationException(EnumMessage.DATO_OBBLIGATORIO, "idUtente");
        }

        HashMap<String, Object> hParams = new HashMap<>();
        hParams.put("idUtente", idUtente);
        hParams.put("codStrutturaGet", codStrutturaGet);

        List<UtentePerProfiloGetEntity> results = utentePerProfiloGetRepository.findAll(hParams, EnumManagementDomainTypeFunction.GET_ALL_UTENTE_PER_PROFILO_GET_BY_ID_UTENTE);

        return utentePerProfiloGetMapper.mapTo(results);
    }


}
