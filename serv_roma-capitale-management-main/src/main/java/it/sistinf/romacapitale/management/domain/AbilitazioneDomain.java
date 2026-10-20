package it.sistinf.romacapitale.management.domain;

import it.sistinf.romacapitale.core.domain.AbstractDomain;
import it.sistinf.romacapitale.core.dto.PageInfo;
import it.sistinf.romacapitale.core.dto.RequestListDTO;
import it.sistinf.romacapitale.core.dto.ResponseListDTO;
import it.sistinf.romacapitale.core.exceptions.ApplicationException;
import it.sistinf.romacapitale.core.exceptions.ObjectNotFoundException;
import it.sistinf.romacapitale.core.messages.EnumMessage;
import it.sistinf.romacapitale.core.utils.ControlloCampi;
import it.sistinf.romacapitale.integration.management.vo.AbilitazioneVO;
import it.sistinf.romacapitale.management.entity.AbilitazioneEntity;
import it.sistinf.romacapitale.management.entity.ApplicazioneEntityPK;
import it.sistinf.romacapitale.management.enums.EnumManagementDomainTypeFunction;
import it.sistinf.romacapitale.management.mapper.AbilitazioneMapper;
import it.sistinf.romacapitale.management.repository.AbilitazioneRepository;
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
public class AbilitazioneDomain extends AbstractDomain {


    private final AbilitazioneMapper abilitazioneMapper;
    private AbilitazioneRepository abilitazioneRepository;
    private ApplicazioneDomain applicazioneDomain;


    public ResponseListDTO<AbilitazioneVO> listAbilitazioni(RequestListDTO<AbilitazioneVO> request) {

        HashMap<String, Object> hParams = getFilteredQueryMap(request);
        PageInfo pageInfo = new PageInfo();

        List<AbilitazioneEntity> results = null;
        Long totalCount;
        if (request.getPageInfo() != null) {
            results = abilitazioneRepository.findAll(
                    hParams, request.getPageInfo().getPage(), request.getPageInfo().getPageSize(), EnumManagementDomainTypeFunction.GET_ALL_ABILITAZIONI_FILTERED
            );
            pageInfo = request.getPageInfo();
            totalCount = abilitazioneRepository.count(hParams, EnumManagementDomainTypeFunction.GET_ALL_ABILITAZIONI_FILTERED_COUNT);
        } else {
            results = abilitazioneRepository.findAll(hParams, EnumManagementDomainTypeFunction.GET_ALL_ABILITAZIONI_FILTERED);
            totalCount = (long) results.size();
        }


        ResponseListDTO<AbilitazioneVO> response = new ResponseListDTO<>();

        response.setList(abilitazioneMapper.mapTo(results));
        response.setPageInfo(pageInfo);
        response.getPageInfo().setTotalCount(totalCount);
        return response;
    }

    public AbilitazioneVO getAbilitazioneById(Long id) throws ApplicationException {
        if (ControlloCampi.campoVuoto(id)) {
            throw new ApplicationException(EnumMessage.DATO_OBBLIGATORIO, "Id Abilitazione");
        }

        return abilitazioneMapper.mapTo(abilitazioneRepository.findById(id));
    }


    @Transactional(propagation = Propagation.REQUIRED)
    public AbilitazioneVO createAbilitazione(AbilitazioneVO abilitazioneVO) {
        if (ControlloCampi.campoVuoto(abilitazioneVO)) {
            throw new ApplicationException(EnumMessage.DATO_OBBLIGATORIO, "payload");
        }
        if (ControlloCampi.campoVuoto(abilitazioneVO.getCdAbilitazione())) {
            throw new ApplicationException(EnumMessage.DATO_OBBLIGATORIO, "cdAbilitazione");
        }
        if (ControlloCampi.campoVuoto(abilitazioneVO.getCdAmbito())) {
            throw new ApplicationException(EnumMessage.DATO_OBBLIGATORIO, "cdAmbito");
        }
        if (ControlloCampi.campoVuoto(abilitazioneVO.getCdApplicazione())) {
            throw new ApplicationException(EnumMessage.DATO_OBBLIGATORIO, "cdApplicazione");
        }

        try {
             applicazioneDomain.getApplicazione(new ApplicazioneEntityPK(abilitazioneVO.getCdAmbito(),  abilitazioneVO.getCdApplicazione()));
        } catch (ObjectNotFoundException e) {
            throw new ApplicationException( "Nessuna applicazione trovata con cdAmbito: " + abilitazioneVO.getCdAmbito()+ " e cdApplicazione: "+ abilitazioneVO.getCdApplicazione());
        }

        AbilitazioneEntity entity = abilitazioneMapper.mapFrom(abilitazioneVO);

        HashMap<String, Object> hParams = new HashMap<>();
        hParams.put("cdAbilitazione", entity.getCdAbilitazione());
        hParams.put("cdAmbito", entity.getCdAmbito());
        hParams.put("cdApplicazione", entity.getCdApplicazione());
        try {
            AbilitazioneEntity abilitazioneDb = abilitazioneRepository.findOne(hParams, EnumManagementDomainTypeFunction.GET_ABILITAZIONE_BY_COD_ABILITAZIONE);
            if ( abilitazioneDb != null) {
                throw new ApplicationException( "Esiste già un' abilitazione con cdAbilitazione " + entity.getCdAbilitazione() + " per l'applicazione indicata");
            }
        } catch (ObjectNotFoundException e) {
            log.debug("Nessuna abilitazione trovata con cdAbilitazione " + entity.getCdAbilitazione());
        }

        entity.setUtenteInserimento(getCurrentUser().getUsername());
        entity.setTimestampInserimento(Timestamp.valueOf(LocalDateTime.now()));
        entity.setUtenteUltimoAggiornamento(getCurrentUser().getUsername());
        entity.setTimestampUltimoAggiornamento(Timestamp.valueOf(LocalDateTime.now()));
        abilitazioneRepository.create(entity);
        abilitazioneVO = abilitazioneMapper.mapTo(entity);
        return abilitazioneVO;
    }


    @Transactional(propagation = Propagation.REQUIRED)
    public AbilitazioneVO updateAbilitazione(AbilitazioneVO abilitazioneVO) throws ApplicationException {
        if (ControlloCampi.campoVuoto(abilitazioneVO)) {
            throw new ApplicationException(EnumMessage.DATO_OBBLIGATORIO, "payload");
        }
        if (ControlloCampi.campoVuoto(abilitazioneVO.getCdAbilitazione())) {
            throw new ApplicationException(EnumMessage.DATO_OBBLIGATORIO, "cdAbilitazione");
        }
        if (ControlloCampi.campoVuoto(abilitazioneVO.getCdAmbito())) {
            throw new ApplicationException(EnumMessage.DATO_OBBLIGATORIO, "cdAmbito");
        }
        if (ControlloCampi.campoVuoto(abilitazioneVO.getCdApplicazione())) {
            throw new ApplicationException(EnumMessage.DATO_OBBLIGATORIO, "cdApplicazione");
        }

        try {
           applicazioneDomain.getApplicazione(new ApplicazioneEntityPK(abilitazioneVO.getCdAmbito(),  abilitazioneVO.getCdApplicazione()));
        } catch (ObjectNotFoundException e) {
            throw new ApplicationException( "Nessuna applicazione trovata con cdAmbito: " + abilitazioneVO.getCdAmbito()+ " e cdApplicazione: "+ abilitazioneVO.getCdApplicazione());
        }

        AbilitazioneEntity entity = abilitazioneMapper.mapFrom(abilitazioneVO);
        AbilitazioneEntity abilitazioneDb = abilitazioneRepository.findById(entity.getId());
        Long idAbilitazione = abilitazioneVO.getKey();

        HashMap<String, Object> hParams = new HashMap<>();
        hParams.put("cdAbilitazione", entity.getCdAbilitazione());
        hParams.put("cdAmbito", entity.getCdAmbito());
        hParams.put("cdApplicazione", entity.getCdApplicazione());
        try {
            AbilitazioneEntity abilitazioneFound = abilitazioneRepository.findOne(hParams, EnumManagementDomainTypeFunction.GET_ABILITAZIONE_BY_COD_ABILITAZIONE);
            if (abilitazioneFound != null && idAbilitazione.intValue() != abilitazioneFound.getId().intValue()) {
                throw new ApplicationException( "Esiste già un' abilitazione con cdAbilitazione " + entity.getCdAbilitazione() + " per l'applicazione indicata");
            }
        } catch (ObjectNotFoundException e) {
            log.debug("Nessuna abilitazione trovata con cdAbilitazione " + entity.getCdAbilitazione());
        }

        entity.setUtenteUltimoAggiornamento(getCurrentUser().getUsername());
        entity.setTimestampUltimoAggiornamento(Timestamp.valueOf(LocalDateTime.now()));
        entity.setUtenteInserimento(abilitazioneDb.getUtenteInserimento());
        entity.setTimestampInserimento(abilitazioneDb.getTimestampInserimento());

        abilitazioneRepository.update(entity);

        abilitazioneVO = abilitazioneMapper.mapTo(entity);
        return abilitazioneVO;
    }


    @Transactional(propagation = Propagation.REQUIRED)
    public AbilitazioneVO deleteAbilitazione(Long id) throws ApplicationException {
        if (ControlloCampi.campoVuoto(id)) {
            throw new ApplicationException(EnumMessage.DATO_OBBLIGATORIO, "Id Abilitazione");
        }
        AbilitazioneEntity entity = abilitazioneRepository.findById(id);

        abilitazioneRepository.removeById(entity.getId());
        return abilitazioneMapper.mapTo(entity);
    }


}
