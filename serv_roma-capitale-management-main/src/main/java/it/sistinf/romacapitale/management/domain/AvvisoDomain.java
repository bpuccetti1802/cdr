package it.sistinf.romacapitale.management.domain;

import it.sistinf.romacapitale.core.domain.AbstractDomain;
import it.sistinf.romacapitale.core.dto.PageInfo;
import it.sistinf.romacapitale.core.dto.RequestListDTO;
import it.sistinf.romacapitale.core.dto.ResponseListDTO;
import it.sistinf.romacapitale.core.exceptions.ApplicationException;
import it.sistinf.romacapitale.core.messages.EnumMessage;
import it.sistinf.romacapitale.core.utils.ControlloCampi;
import it.sistinf.romacapitale.integration.management.vo.AvvisoVO;
import it.sistinf.romacapitale.management.entity.AvvisoEntity;
import it.sistinf.romacapitale.management.enums.EnumManagementDomainTypeFunction;
import it.sistinf.romacapitale.management.mapper.AvvisoMapper;
import it.sistinf.romacapitale.management.repository.AvvisoRepository;
import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.sql.Timestamp;
import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.List;

@Service
@AllArgsConstructor
@Slf4j
public class AvvisoDomain extends AbstractDomain {

    private final AvvisoMapper avvisoMapper;
    private final AvvisoRepository avvisoRepository;

    /**
     * Crea un nuovo avviso
     */
    @Transactional
    public AvvisoVO createAvviso(AvvisoVO avvisoVO) throws ApplicationException {
        if (ControlloCampi.campoVuoto(avvisoVO)) {
            throw new ApplicationException(EnumMessage.DATO_OBBLIGATORIO, "payload");
        }
        if (ControlloCampi.campoVuoto(avvisoVO.getCdAmbito())) {
            throw new ApplicationException(EnumMessage.DATO_OBBLIGATORIO, "Codice Ambito");
        }
        if (ControlloCampi.campoVuoto(avvisoVO.getCdApplicazione())) {
            throw new ApplicationException(EnumMessage.DATO_OBBLIGATORIO, "Codice Applicazione");
        }
        if (ControlloCampi.campoVuoto(avvisoVO.getDsTitoloAvviso())) {
            throw new ApplicationException(EnumMessage.DATO_OBBLIGATORIO, "Titolo Avviso");
        }
        if (ControlloCampi.campoVuoto(avvisoVO.getDsAvviso())) {
            throw new ApplicationException(EnumMessage.DATO_OBBLIGATORIO, "Descrizione Avviso");
        }
        if (ControlloCampi.campoVuoto(avvisoVO.getDtInizio())) {
            throw new ApplicationException(EnumMessage.DATO_OBBLIGATORIO, "Data Inizio");
        }
        if (ControlloCampi.campoVuoto(avvisoVO.getDtFine())) {
            throw new ApplicationException(EnumMessage.DATO_OBBLIGATORIO, "Data Fine");
        }
        AvvisoEntity entity = avvisoMapper.mapFrom(avvisoVO);

        if (entity.getFlAttivo() == null) {
            entity.setFlAttivo(true);
        }

        entity.setUtenteInserimento(getCurrentUser().getUsername());
        entity.setTimestampInserimento(Timestamp.valueOf(LocalDateTime.now()));
        entity.setUtenteUltimoAggiornamento(getCurrentUser().getUsername());
        entity.setTimestampUltimoAggiornamento(Timestamp.valueOf(LocalDateTime.now()));

        avvisoRepository.create(entity);

        return avvisoMapper.mapTo(entity);
    }

    /**
     * Aggiorna un avviso esistente
     */
    @Transactional
    public AvvisoVO updateAvviso(AvvisoVO avvisoVO) throws ApplicationException {
        if (ControlloCampi.campoVuoto(avvisoVO)) {
            throw new ApplicationException(EnumMessage.DATO_OBBLIGATORIO, "payload");
        }
        if (ControlloCampi.campoVuoto(avvisoVO.getKey())) {
            throw new ApplicationException(EnumMessage.DATO_OBBLIGATORIO, "Id Avviso");
        }

        AvvisoEntity entity = avvisoMapper.mapFrom(avvisoVO);

        entity.setUtenteInserimento(getCurrentUser().getUsername());
        entity.setTimestampInserimento(Timestamp.valueOf(LocalDateTime.now()));
        entity.setUtenteUltimoAggiornamento(getCurrentUser().getUsername());
        entity.setTimestampUltimoAggiornamento(Timestamp.valueOf(LocalDateTime.now()));

        avvisoRepository.update(entity);

        return avvisoMapper.mapTo(entity);
    }

    /**
     * Elimina un avviso per ID
     */
    @Transactional
    public AvvisoVO deleteAvviso(Long id) throws ApplicationException {
        if (ControlloCampi.campoVuoto(id)) {
            throw new ApplicationException(EnumMessage.DATO_OBBLIGATORIO, "Id Avviso");
        }

        AvvisoEntity entity = avvisoRepository.findById(id);
        avvisoRepository.removeById(entity.getId());

        return avvisoMapper.mapTo(entity);
    }

    /**
     * Recupera un avviso per ID
     */
    public AvvisoVO avvisoById(Long id) throws ApplicationException {
        if (ControlloCampi.campoVuoto(id)) {
            throw new ApplicationException(EnumMessage.DATO_OBBLIGATORIO, "Id Avviso");
        }
        return avvisoMapper.mapTo(avvisoRepository.findById(id));
    }

    /**
     * Lista avvisi con filtri opzionali e paginazione
     * Per la gestione (Console di Amministrazione)
     */
    public ResponseListDTO<AvvisoVO> listAvvisi(RequestListDTO<AvvisoVO> request) throws ApplicationException {

        HashMap<String, Object> hParams = getFilteredQueryMap(request);
        PageInfo pageInfo = new PageInfo();

        List<AvvisoEntity> results;
        Long totalCount;

        if (request.getPageInfo() != null) {
            results = avvisoRepository.findAll(
                hParams, request.getPageInfo().getPage(), request.getPageInfo().getPageSize(),
                EnumManagementDomainTypeFunction.GET_ALL_AVVISI_FILTERED
            );
            pageInfo = request.getPageInfo();
            totalCount = avvisoRepository.count(hParams, EnumManagementDomainTypeFunction.GET_ALL_AVVISI_FILTERED_COUNT);
        } else {
            results = avvisoRepository.findAll(hParams, EnumManagementDomainTypeFunction.GET_ALL_AVVISI_FILTERED);
            totalCount = (long) results.size();
        }

        ResponseListDTO<AvvisoVO> response = new ResponseListDTO<>();
        response.setList(avvisoMapper.mapTo(results));
        response.setPageInfo(pageInfo);
        response.getPageInfo().setTotalCount(totalCount);

        return response;
    }

    /**
     * Visualizza avvisi attivi per ambito e applicazione
     * Include avvisi cross (cd_ambito = '00') e filtrati per data corrente
     */
    public ResponseListDTO<AvvisoVO> getAvvisiAttivi(String cdAmbito, String cdApplicazione, RequestListDTO<AvvisoVO> request) throws ApplicationException {
        if (ControlloCampi.campoVuoto(cdAmbito)) {
            throw new ApplicationException(EnumMessage.DATO_OBBLIGATORIO, "Codice Ambito");
        }
        if (ControlloCampi.campoVuoto(cdApplicazione)) {
            throw new ApplicationException(EnumMessage.DATO_OBBLIGATORIO, "Codice Applicazione");
        }

        HashMap<String, Object> hParams = getFilteredQueryMap(request);
        hParams.put("cdAmbito", cdAmbito);
        hParams.put("cdApplicazione", cdApplicazione);

        PageInfo pageInfo = new PageInfo();
        List<AvvisoEntity> results;
        Long totalCount;

        if (request.getPageInfo() != null) {
            results = avvisoRepository.findAll(
                hParams, request.getPageInfo().getPage(), request.getPageInfo().getPageSize(),
                EnumManagementDomainTypeFunction.GET_AVVISI_ATTIVI_BY_AMBITO_APPLICAZIONE
            );
            pageInfo = request.getPageInfo();
            totalCount = avvisoRepository.count(hParams, EnumManagementDomainTypeFunction.GET_AVVISI_ATTIVI_BY_AMBITO_APPLICAZIONE_COUNT);
        } else {
            results = avvisoRepository.findAll(hParams, EnumManagementDomainTypeFunction.GET_AVVISI_ATTIVI_BY_AMBITO_APPLICAZIONE);
            totalCount = (long) results.size();
        }

        ResponseListDTO<AvvisoVO> response = new ResponseListDTO<>();
        response.setList(avvisoMapper.mapTo(results));
        response.setPageInfo(pageInfo);
        response.getPageInfo().setTotalCount(totalCount);

        return response;
    }

    /**
     * Attiva un avviso
     */
    @Transactional
    public AvvisoVO enableAvviso(Long id) throws ApplicationException {
        if (ControlloCampi.campoVuoto(id)) {
            throw new ApplicationException(EnumMessage.DATO_OBBLIGATORIO, "Id Avviso");
        }

        AvvisoEntity entity = avvisoRepository.findById(id);
        entity.setFlAttivo(true);
        entity.setUtenteUltimoAggiornamento(getCurrentUser().getUsername());
        entity.setTimestampUltimoAggiornamento(Timestamp.valueOf(LocalDateTime.now()));

        avvisoRepository.update(entity);

        return avvisoMapper.mapTo(entity);
    }

    /**
     * Disattiva un avviso
     */
    @Transactional
    public AvvisoVO disableAvviso(Long id) throws ApplicationException {
        if (ControlloCampi.campoVuoto(id)) {
            throw new ApplicationException(EnumMessage.DATO_OBBLIGATORIO, "Id Avviso");
        }

        AvvisoEntity entity = avvisoRepository.findById(id);
        entity.setFlAttivo(false);
        entity.setUtenteUltimoAggiornamento(getCurrentUser().getUsername());
        entity.setTimestampUltimoAggiornamento(Timestamp.valueOf(LocalDateTime.now()));

        avvisoRepository.update(entity);

        return avvisoMapper.mapTo(entity);
    }
}