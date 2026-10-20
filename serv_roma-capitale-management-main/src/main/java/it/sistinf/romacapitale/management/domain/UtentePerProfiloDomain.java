package it.sistinf.romacapitale.management.domain;

import it.sistinf.romacapitale.core.domain.AbstractDomain;
import it.sistinf.romacapitale.core.exceptions.ApplicationException;
import it.sistinf.romacapitale.core.messages.EnumMessage;
import it.sistinf.romacapitale.core.utils.ControlloCampi;
import it.sistinf.romacapitale.integration.management.vo.ApplicazioneKeyVO;
import it.sistinf.romacapitale.integration.management.vo.ApplicazioneVO;
import it.sistinf.romacapitale.integration.management.vo.UtentePerProfiloVO;
import it.sistinf.romacapitale.management.entity.UtentePerProfiloEntity;
import it.sistinf.romacapitale.management.enums.EnumManagementDomainTypeFunction;
import it.sistinf.romacapitale.management.mapper.ApplicazioneMapper;
import it.sistinf.romacapitale.management.mapper.UtentePerProfiloMapper;
import it.sistinf.romacapitale.management.repository.ApplicazioneRepository;
import it.sistinf.romacapitale.management.repository.UtentePerProfiloRepository;
import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Propagation;
import org.springframework.transaction.annotation.Transactional;

import java.sql.Timestamp;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;


@Service
@AllArgsConstructor
@Slf4j
public class UtentePerProfiloDomain extends AbstractDomain {

    private UtentePerProfiloRepository utentePerProfiloRepository;
    private ApplicazioneRepository applicazioneRepository;

    private UtentePerProfiloMapper utentePerProfiloMapper;
    private ApplicazioneMapper applicazioneMapper;


    @Transactional(propagation = Propagation.REQUIRED)
    public UtentePerProfiloVO createUtentePerProfilo(UtentePerProfiloVO utentePerProfiloVO) throws ApplicationException {
        if (ControlloCampi.campoVuoto(utentePerProfiloVO)) {
            throw new ApplicationException(EnumMessage.DATO_OBBLIGATORIO, "payload");
        }
        if (ControlloCampi.campoVuoto(utentePerProfiloVO.getKey().getIdUtente())) {
            throw new ApplicationException(EnumMessage.DATO_OBBLIGATORIO, "idUtente");
        }
//        if (ControlloCampi.campoVuoto(utentePerProfiloVO.getProfiloDefault())) {
//            throw new ApplicationException(EnumMessage.DATO_OBBLIGATORIO, "profiloDefault");
//        }

        UtentePerProfiloEntity entity = utentePerProfiloMapper.mapFrom(utentePerProfiloVO);
        entity.setUtenteInserimento(getCurrentUser().getUsername());
        entity.setTimestampInserimento(Timestamp.valueOf(LocalDateTime.now()));
        entity.setUtenteUltimoAggiornamento(getCurrentUser().getUsername());
        entity.setTimestampUltimoAggiornamento(Timestamp.valueOf(LocalDateTime.now()));
        utentePerProfiloRepository.create(entity);

        return utentePerProfiloMapper.mapTo(entity);
    }

    @Transactional(propagation = Propagation.REQUIRED)
    public void deleteAllUtentePerProfiloByIdUtente(Long idUtente) throws ApplicationException {
        if (ControlloCampi.campoVuoto(idUtente)) {
            throw new ApplicationException(EnumMessage.DATO_OBBLIGATORIO, "idUtente");
        }

        HashMap<String, Object> hParams = new HashMap<>();
        hParams.put("idUtente", idUtente);

        try {
            log.info("Delete allUtentePerProfiloByIdUtente");
            utentePerProfiloRepository.removeAll(hParams, EnumManagementDomainTypeFunction.DELETE_ALL_UTENTE_PER_PROFILO_BY_ID_UTENTE);
        } catch (ApplicationException ae) {
            log.error("Errore nella cancellazione di UtentePerProfilo con Id Utente: {}", idUtente);
            throw new ApplicationException("Errore nella cancellazione di UtentePerProfilo con Id Utente: " + idUtente);
        }
    }


    @Transactional(propagation = Propagation.REQUIRED)
    public void deleteAllUtentePerProfiloByIdProfilo(Long idProfilo) throws ApplicationException {
        if (ControlloCampi.campoVuoto(idProfilo)) {
            throw new ApplicationException(EnumMessage.DATO_OBBLIGATORIO, "idProfilo");
        }

        HashMap<String, Object> hParams = new HashMap<>();
        hParams.put("idProfilo", idProfilo);

        try {
            log.info("Delete allUtentePerProfiloByIdProfilo");
            utentePerProfiloRepository.removeAll(hParams, EnumManagementDomainTypeFunction.DELETE_ALL_UTENTE_PER_PROFILO_BY_ID_PROFILO);
        } catch (ApplicationException ae) {
            log.error("Errore nella cancellazione di UtentePerProfilo con Id Profilo: " + idProfilo);
            throw new ApplicationException("Errore nella cancellazione di UtentePerProfilo con Id Profilo: " + idProfilo);
        }
    }


    public List<UtentePerProfiloVO> listUtentePerProfiloByIdUtente(Long idUtente) throws ApplicationException {

        if (ControlloCampi.campoVuoto(idUtente)) {
            throw new ApplicationException(EnumMessage.DATO_OBBLIGATORIO, "idUtente");
        }

        HashMap<String, Object> hParams = new HashMap<>();
        hParams.put("idUtente", idUtente);

        List<UtentePerProfiloEntity> results = utentePerProfiloRepository.findAll(hParams, EnumManagementDomainTypeFunction.GET_ALL_UTENTE_PER_PROFILO_BY_ID_UTENTE);

        return utentePerProfiloMapper.mapTo(results);
    }


    public List<UtentePerProfiloVO> listUtentePerProfiloByUtenteAndApplicazione(ApplicazioneKeyVO applicazioneKey, Long idUtente) throws ApplicationException {

        HashMap<String, Object> hParams = new HashMap<>();
        List<UtentePerProfiloVO> resultsByApplicazione = new ArrayList<>();

        hParams.put("idUtente", idUtente);
        List<UtentePerProfiloVO> results = utentePerProfiloMapper
                .mapTo(utentePerProfiloRepository.findAll(hParams, EnumManagementDomainTypeFunction.GET_ALL_UTENTE_PER_PROFILO_BY_ID_UTENTE));

        hParams.clear();

        hParams.put("cdAmbito", applicazioneKey.getCdAmbito());
        hParams.put("cdAmbitoSearchType", "EQUALS");
        hParams.put("cdApplicazione", applicazioneKey.getCdApplicazione());
        hParams.put("cdApplicazioneSearchType", "EQUALS");
        ApplicazioneVO applicazione = applicazioneMapper
                .mapTo(applicazioneRepository.findOne(hParams, EnumManagementDomainTypeFunction.GET_ALL_APPLICAZIONI_FILTERED));

        for (UtentePerProfiloVO uPVO : results) {
            if (uPVO.getProfilo().getCdApplicazione().equals(applicazione.getKey().getCdApplicazione())
                    && uPVO.getProfilo().getCdAmbito().equals(applicazione.getKey().getCdAmbito())) {
                resultsByApplicazione.add(uPVO);
            }
        }
        return resultsByApplicazione;
    }

    public List<Long> listIdUtentiPerRuolo(Long idProfilo) throws ApplicationException {
        HashMap<String, Object> hParams = new HashMap<>();
        hParams.put("idProfilo", idProfilo);

        List<UtentePerProfiloEntity> utenti = utentePerProfiloRepository.findAll(hParams, EnumManagementDomainTypeFunction.GET_ALL_UTENTI_PER_PROFILO_BY_ID_PROFILO);

        if(utenti != null) {
            return utenti.stream().map(upp -> upp.getId().getIdUtente()).distinct().toList();
        }

        return null;
    }

}
