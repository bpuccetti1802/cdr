package it.sistinf.romacapitale.management.domain;

import it.sistinf.romacapitale.core.domain.AbstractDomain;
import it.sistinf.romacapitale.core.exceptions.ApplicationException;
import it.sistinf.romacapitale.core.messages.EnumMessage;
import it.sistinf.romacapitale.core.utils.ControlloCampi;
import it.sistinf.romacapitale.integration.management.vo.ProfiloPerAbilitazioneVO;
import it.sistinf.romacapitale.management.entity.AbilitazioneEntity;
import it.sistinf.romacapitale.management.entity.ProfiloPerAbilitazioneEntity;
import it.sistinf.romacapitale.management.enums.EnumManagementDomainTypeFunction;
import it.sistinf.romacapitale.management.mapper.ProfiloPerAbilitazioneMapper;
import it.sistinf.romacapitale.management.repository.AbilitazioneRepository;
import it.sistinf.romacapitale.management.repository.ProfiloPerAbilitazioneRepository;
import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Propagation;
import org.springframework.transaction.annotation.Transactional;

import java.sql.Timestamp;
import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.List;


@Service
@AllArgsConstructor
@Slf4j
public class ProfiloPerAbilitazioneDomain extends AbstractDomain {

    private final ProfiloPerAbilitazioneMapper profiloPerAbilitazioneMapper;
    private ProfiloPerAbilitazioneRepository profiloPerAbilitazioneRepository;
    private AbilitazioneRepository abilitazioneRepository;
    @Transactional(propagation = Propagation.REQUIRED)
    public ProfiloPerAbilitazioneVO createProfiloPerAbilitazione(ProfiloPerAbilitazioneVO profiloPerAbilitazioneVO) throws ApplicationException {
        if (ControlloCampi.campoVuoto(profiloPerAbilitazioneVO)) {
            throw new ApplicationException(EnumMessage.DATO_OBBLIGATORIO, "payload");
        }
        if (ControlloCampi.campoVuoto(profiloPerAbilitazioneVO.getKey().getIdProfilo())) {
            throw new ApplicationException(EnumMessage.DATO_OBBLIGATORIO, "idProfilo");
        }
//        if (ControlloCampi.campoVuoto(utentePerProfiloVO.getProfiloDefault())) {
//            throw new ApplicationException(EnumMessage.DATO_OBBLIGATORIO, "profiloDefault");
//        }

        ProfiloPerAbilitazioneEntity entity = profiloPerAbilitazioneMapper.mapFrom(profiloPerAbilitazioneVO);
        AbilitazioneEntity abilitazione = abilitazioneRepository.findById(entity.getId().getIdAbilitazione());
        entity.setAbilitazione(abilitazione);
        entity.setUtenteInserimento(getCurrentUser().getUsername());
        entity.setTimestampInserimento(Timestamp.valueOf(LocalDateTime.now()));
        entity.setUtenteUltimoAggiornamento(getCurrentUser().getUsername());
        entity.setTimestampUltimoAggiornamento(Timestamp.valueOf(LocalDateTime.now()));
        profiloPerAbilitazioneRepository.create(entity);

        return profiloPerAbilitazioneMapper.mapTo(entity);
    }

    @Transactional(propagation = Propagation.REQUIRED)
    public void deleteAllProfiloPerAbilitazioneByIdProfilo(Long idProfilo) throws ApplicationException {
        if (ControlloCampi.campoVuoto(idProfilo)) {
            throw new ApplicationException(EnumMessage.DATO_OBBLIGATORIO, "idProfilo");
        }

        HashMap<String, Object> hParams = new HashMap<>();
        hParams.put("idProfilo", idProfilo);

        try {
            log.info("Delete allProfiloPerAbilitazione");
            profiloPerAbilitazioneRepository.removeAll(hParams, EnumManagementDomainTypeFunction.DELETE_ALL_PROFILO_PER_ABILITAZIONE_BY_ID_PROFILO);
        } catch (ApplicationException ae) {
            log.error("Errore nella cancellazione di ProfiloPerAbilitazione con Id Utente: " + idProfilo);
            throw new ApplicationException("Errore nella cancellazione di ProfiloPerAbilitazione con Id Profilo: " + idProfilo);
        }
    }

    public List<ProfiloPerAbilitazioneVO> listProfiloPerAbilitazioneByProfiloList(List<Long> idProfiloList) throws ApplicationException {

        if (ControlloCampi.campoVuoto(idProfiloList)) {
            throw new ApplicationException(EnumMessage.DATO_OBBLIGATORIO, "idProfiloList");
        }

        HashMap<String, Object> hParams = new HashMap<>();
        hParams.put("idProfiloList", idProfiloList);

        List<ProfiloPerAbilitazioneEntity> results = profiloPerAbilitazioneRepository.findAll(hParams, EnumManagementDomainTypeFunction.GET_ALL_PROFILO_PER_ABILITAZIONE_BY_PROFILO_LIST);

        return profiloPerAbilitazioneMapper.mapTo(results);
    }

}
