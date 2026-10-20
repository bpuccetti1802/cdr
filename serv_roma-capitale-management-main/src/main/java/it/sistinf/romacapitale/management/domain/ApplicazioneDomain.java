package it.sistinf.romacapitale.management.domain;

import feign.FeignException;
import it.sistinf.romacapitale.core.domain.AbstractDomain;
import it.sistinf.romacapitale.core.dto.PageInfo;
import it.sistinf.romacapitale.core.dto.RequestDTO;
import it.sistinf.romacapitale.core.dto.RequestHeader;
import it.sistinf.romacapitale.core.dto.RequestListDTO;
import it.sistinf.romacapitale.core.dto.ResponseListDTO;
import it.sistinf.romacapitale.core.enums.SearchTypeEnum;
import it.sistinf.romacapitale.core.exceptions.ApplicationException;
import it.sistinf.romacapitale.core.exceptions.ObjectNotFoundException;
import it.sistinf.romacapitale.core.messages.EnumMessage;
import it.sistinf.romacapitale.core.utils.ControlloCampi;
import it.sistinf.romacapitale.integration.archiviazione.api.ArchiviazioneApiClient;
import it.sistinf.romacapitale.integration.management.vo.*;
import it.sistinf.romacapitale.management.entity.ApplicazioneEntity;
import it.sistinf.romacapitale.management.entity.ApplicazioneEntityPK;
import it.sistinf.romacapitale.management.enums.EnumManagementDomainTypeFunction;
import it.sistinf.romacapitale.management.mapper.ApplicazioneMapper;
import it.sistinf.romacapitale.management.repository.ApplicazioneRepository;
import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.core.io.Resource;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Propagation;
import org.springframework.transaction.annotation.Transactional;
import java.util.HashMap;
import java.util.List;

@Service
@AllArgsConstructor
@Slf4j
public class ApplicazioneDomain extends AbstractDomain {

    private final ApplicazioneMapper applicazioneMapper;

    private ApplicazioneRepository applicazioneRepository;

    private final ArchiviazioneApiClient archiviazioneApiClient;



    public ResponseListDTO<ApplicazioneVO> listApplicazioni(RequestListDTO<ApplicazioneVO> request) {

        HashMap<String, Object> hParams = getFilteredQueryMap(request);
        PageInfo pageInfo = new PageInfo();

        List<ApplicazioneEntity> results = null;
        Long totalCount;
        if (request.getPageInfo() != null) {
            results = applicazioneRepository.findAll(
                    hParams, request.getPageInfo().getPage(), request.getPageInfo().getPageSize(), EnumManagementDomainTypeFunction.GET_ALL_APPLICAZIONI_FILTERED
            );
            pageInfo = request.getPageInfo();
            totalCount = applicazioneRepository.count(hParams, EnumManagementDomainTypeFunction.GET_ALL_APPLICAZIONI_FILTERED_COUNT);
        } else {
            results = applicazioneRepository.findAll(hParams, EnumManagementDomainTypeFunction.GET_ALL_APPLICAZIONI_FILTERED);
            totalCount = (long)results.size();
        }


        ResponseListDTO<ApplicazioneVO> response = new ResponseListDTO<>();

        response.setList(applicazioneMapper.mapTo(results));
        response.setPageInfo(pageInfo);
        response.getPageInfo().setTotalCount(totalCount);
        return response;
    }


    public ApplicazioneVO getApplicazione(ApplicazioneEntityPK id) throws ApplicationException {
        return applicazioneMapper.mapTo(applicazioneRepository.findById(id));
    }

    public ApplicazioneVO getApplicazioneFromContextRoot(String contextRoot) throws ApplicationException {
        HashMap<String, Object> hParams = new HashMap<>();
        hParams.put("dsContextRoot", contextRoot);
        return applicazioneMapper.mapTo(applicazioneRepository.findOne(hParams, EnumManagementDomainTypeFunction.GET_ALL_APPLICAZIONI_FILTERED));
    }

    public ResponseEntity<Resource> getManualeUtente(String cdAmbito, String cdApplicazione) {

        ApplicazioneEntity app = applicazioneRepository.findById(new ApplicazioneEntityPK(cdAmbito, cdApplicazione));
        if (app == null) throw new ApplicationException("Applicazione non trovata");

        String cdDocManuale = app.getCdDocManuale();
        if (cdDocManuale == null || cdDocManuale.isBlank()) {
            throw new ApplicationException("Manuale non disponibile");
        }

        RequestDTO<String> req = new RequestDTO<>();
        req.setPayload(cdDocManuale);

        RequestHeader header = new RequestHeader();
        header.setCdAmbito(cdAmbito);
        header.setCdApplicazione(cdApplicazione);
        req.setHeader(header);

        try {
            ResponseEntity<Resource> resp = archiviazioneApiClient.downloadDocument(req);
            if (resp == null || resp.getBody() == null) {
                throw new ApplicationException("Manuale non disponibile");
            }
            return resp;

        } catch (FeignException.NotFound nf) {
            log.warn("Manuale non trovato in archiviazione (cdDocumento={})", cdDocManuale, nf);
            throw new ApplicationException("Manuale non disponibile");

        } catch (FeignException fe) {
            log.error("Errore Feign download manuale (cdDocumento={}) status={}", cdDocManuale, fe.status(), fe);
            throw new ApplicationException("Manuale non disponibile");
        }
    }

    public List<ApplicazioneVO> getApplicazioniFiglie(String cdAmbito, String cdApplicazione) throws ApplicationException {
        HashMap<String, Object> hParams = new HashMap<>();
        hParams.put("cdAmbito", cdAmbito);
        hParams.put("cdApplicazione", cdApplicazione);
        return applicazioneMapper.mapTo(applicazioneRepository.findAll(hParams, EnumManagementDomainTypeFunction.GET_ALL_APPLICAZIONI_FIGLIE));
    }

    public ApplicazioneVO getApplicazioneFromCdApplicazione(String cdApplicazione) throws ApplicationException {
        HashMap<String, Object> hParams = new HashMap<>();
        hParams.put("cdApplicazione", cdApplicazione);
        hParams.put("cdApplicazioneSearchType", "EQUALS");
        return applicazioneMapper.mapTo(applicazioneRepository.findOne(hParams, EnumManagementDomainTypeFunction.GET_ALL_APPLICAZIONI_FILTERED));
    }

    public List<ApplicazioneVO> getApplicazioneByParams(RicercaApplicazioneVO request) throws ApplicationException {
        HashMap<String, Object> hParams = new HashMap<>();
        if(ControlloCampi.campoVuoto(request)){
            return null;
        }

        if(!ControlloCampi.campoVuoto(request.getCdApplicazione())){
            hParams.put("cdApplicazione", request.getCdAmbito());
            hParams.put("cdApplicazioneSearchType", SearchTypeEnum.EQUALS.getSearchType());
        }

        if(!ControlloCampi.campoVuoto(request.getCdAmbito())){
            hParams.put("cdAmbito", request.getCdApplicazione());
            hParams.put("cdAmbitoSearchType", SearchTypeEnum.EQUALS.getSearchType());

        }

        if(!ControlloCampi.campoVuoto(request.getDsApplicazione())){
            hParams.put("dsApplicazione", request.getDsApplicazione());
            hParams.put("dsApplicazioneSearchType", SearchTypeEnum.EQUALS.getSearchType());
        }

        if(!ControlloCampi.campoVuoto(request.getCdCloud())){
            hParams.put("cdCloud", request.getCdCloud());
            hParams.put("cdCloudSearchType", SearchTypeEnum.EQUALS.getSearchType());

        }
        if(!ControlloCampi.campoVuoto(request.getDsContextRoot())){
            hParams.put("dsContextRoot", request.getDsContextRoot());
            hParams.put("dsContextRootSearchType", SearchTypeEnum.EQUALS.getSearchType());
        }

        if(!ControlloCampi.campoVuoto(request.getDsService())){
            hParams.put("dsService", request.getDsService());
            hParams.put("dsServiceSearchType", SearchTypeEnum.EQUALS.getSearchType());
        }

        if(!ControlloCampi.campoVuoto(request.getDsLabel())){
            hParams.put("dsLabel", request.getDsLabel());
            hParams.put("dsLabelSearchType", SearchTypeEnum.EQUALS.getSearchType());
        }

        if(!ControlloCampi.campoVuoto(request.getNmOrdine())){
            hParams.put("nmOrdine", request.getNmOrdine());
            hParams.put("nmOrdineSearchType", SearchTypeEnum.EQUALS.getSearchType());
        }

        if(!ControlloCampi.campoVuoto(request.getIdApplicazioneSa())){
            hParams.put("idApplicazioneSa", request.getIdApplicazioneSa());
            hParams.put("idApplicazioneSaSearchType", SearchTypeEnum.EQUALS.getSearchType());
        }

        if(!ControlloCampi.campoVuoto(request.getCdAmbitoPadre())){
            hParams.put("cdAmbitoPadre", request.getCdAmbitoPadre());
            hParams.put("cdAmbitoPadreSearchType", SearchTypeEnum.EQUALS.getSearchType());
        }

        if(!ControlloCampi.campoVuoto(request.getCdApplicazionePadre())){
            hParams.put("cdApplicazionePadre", request.getCdApplicazionePadre());
            hParams.put("cdApplicazionePadreSearchType", SearchTypeEnum.EQUALS.getSearchType());
        }

        return applicazioneMapper.mapTo(applicazioneRepository.findAll(hParams, EnumManagementDomainTypeFunction.GET_ALL_APPLICAZIONI_FILTERED));
    }

    @Transactional
    public ApplicazioneVO createApplicazione(ApplicazioneVO request) throws ApplicationException {
        ApplicazioneEntity entity = applicazioneMapper.mapFrom(request);
        try {
            applicazioneRepository.create(entity);
        } catch (ApplicationException e) {
            log.error("Errore creazione applicazione: {}", e.getMessage(), e);
            throw new ApplicationException("Errore creazione applicazione: " + e.getMessage());
        }

        return applicazioneMapper.mapTo(entity);
    }

    @Transactional(propagation = Propagation.REQUIRED)
    public ApplicazioneVO updateApplicazione(ApplicazioneVO request) throws ApplicationException {
        if (ControlloCampi.campoVuoto(request)) {
            throw new ApplicationException(EnumMessage.DATO_OBBLIGATORIO, "payload");
        }
        if (ControlloCampi.campoVuoto(request.getKey())
                && ControlloCampi.campoVuoto(request.getKey().getCdApplicazione())
                && ControlloCampi.campoVuoto(request.getKey().getCdAmbito())) {
            throw new ApplicationException(EnumMessage.DATO_OBBLIGATORIO, "Id composto (cdAmbito e cdApplicazione)");
        }

        // Recupera l'entità esistente dal database
        ApplicazioneEntityPK applicazioneEntityPK= new ApplicazioneEntityPK(request.getKey().getCdAmbito(), request.getKey().getCdApplicazione());
        ApplicazioneEntity entity;
        try {
            entity = applicazioneRepository.findById(applicazioneEntityPK);
        } catch (ObjectNotFoundException e) {
            throw new ApplicationException("Nessuna applicazione trovata con chiave: cdAmbito "
                    + applicazioneEntityPK.getCdAmbito()
                    + " e cdApplicazione "
                    + applicazioneEntityPK.getCdApplicazione());
        }

        // Aggiorna l'entità esistente con i valori del VO (preserva i campi non presenti nel VO)
        applicazioneMapper.updateEntityFromVO(request, entity);
        applicazioneRepository.update(entity);

        return applicazioneMapper.mapTo(entity);
    }

    @Transactional(propagation = Propagation.REQUIRED)
    public Boolean deleteApplicazione(ApplicazioneKeyVO request) throws ApplicationException {

        if (ControlloCampi.campoVuoto(request)) {
            throw new ApplicationException(EnumMessage.DATO_OBBLIGATORIO, "payload");
        }

        if (ControlloCampi.campoVuoto(request.getCdApplicazione())
                && ControlloCampi.campoVuoto(request.getCdAmbito())) {
            throw new ApplicationException(EnumMessage.DATO_OBBLIGATORIO, "Id composto (cdAmbito e cdApplicazione)");
        }

        // Recupera l'entità esistente dal database
        ApplicazioneEntityPK applicazioneEntityPK = new ApplicazioneEntityPK(request.getCdAmbito(), request.getCdApplicazione());

        try {
            applicazioneRepository.removeById(applicazioneEntityPK);
        } catch (ApplicationException e) {
            log.error("Errore interno, applicazione non eliminata. Chiave Applicazione: cdAmbito {} e cdApplicazione {}. Errore: {}",
                    applicazioneEntityPK.getCdAmbito(), applicazioneEntityPK.getCdApplicazione(), e.getMessage());
            return false;
        }

        return true;
    }

}
