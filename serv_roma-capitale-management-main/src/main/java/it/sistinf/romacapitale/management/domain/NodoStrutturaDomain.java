package it.sistinf.romacapitale.management.domain;

import it.sistinf.romacapitale.core.domain.AbstractDomain;
import it.sistinf.romacapitale.core.dto.PageInfo;
import it.sistinf.romacapitale.core.dto.RequestListDTO;
import it.sistinf.romacapitale.core.dto.ResponseListDTO;
import it.sistinf.romacapitale.core.enums.SearchTypeEnum;
import it.sistinf.romacapitale.core.exceptions.ApplicationException;
import it.sistinf.romacapitale.core.exceptions.ObjectNotFoundException;
import it.sistinf.romacapitale.core.messages.EnumMessage;
import it.sistinf.romacapitale.core.utils.ControlloCampi;
import it.sistinf.romacapitale.integration.management.vo.InserisciNodoStrutturaVO;
import it.sistinf.romacapitale.integration.management.vo.NodoStrutturaVO;
import it.sistinf.romacapitale.management.entity.NodoStrutturaEntity;
import it.sistinf.romacapitale.management.enums.EnumManagementDomainTypeFunction;
import it.sistinf.romacapitale.management.mapper.NodoStrutturaMapper;
import it.sistinf.romacapitale.management.repository.NodoStrutturaRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Propagation;
import org.springframework.transaction.annotation.Transactional;

import java.util.HashMap;
import java.util.List;

@Service
@RequiredArgsConstructor
@Slf4j
public class NodoStrutturaDomain extends AbstractDomain {

    private final NodoStrutturaMapper nodoStrutturaMapper;

    private final NodoStrutturaRepository nodoStrutturaRepository;

    @Value("${crittografiaPassword}")
    private String crittografiaPassword;

    @Value("${crittografiaSalt}")
    private String crittografiaSalt;

    public ResponseListDTO<NodoStrutturaVO> listNodoStruttura(RequestListDTO<NodoStrutturaVO> request) throws ApplicationException {

        HashMap<String, Object> hParams = getFilteredQueryMap(request);
        PageInfo pageInfo = new PageInfo();

        List<NodoStrutturaEntity> results = null;
        Long totalCount;
        if (request.getPageInfo() != null) {
            results = nodoStrutturaRepository.findAll(
                    hParams, request.getPageInfo().getPage(), request.getPageInfo().getPageSize(), EnumManagementDomainTypeFunction.GET_ALL_NODO_STRUTTURA_FILTERED
            );
            pageInfo = request.getPageInfo();
            totalCount = nodoStrutturaRepository.count(hParams, EnumManagementDomainTypeFunction.GET_ALL_NODO_STRUTTURA_FILTERED_COUNT);
        }else{
            results = nodoStrutturaRepository.findAll(hParams, EnumManagementDomainTypeFunction.GET_ALL_NODO_STRUTTURA_FILTERED);
            totalCount = (long)results.size();
        }

        ResponseListDTO<NodoStrutturaVO> response = new ResponseListDTO<>();

        response.setList(nodoStrutturaMapper.mapTo(results));
        response.setPageInfo(pageInfo);
        response.getPageInfo().setTotalCount(totalCount);
        return response;
    }

    public List<NodoStrutturaVO> listNodoStrutturaByParams(NodoStrutturaVO nodoStrutturaVO){
        HashMap<String, Object> hParams = new HashMap<>();

        if(!ControlloCampi.campoVuoto(nodoStrutturaVO.getKey())){
            hParams.put("idNodo", nodoStrutturaVO.getKey());
            hParams.put("idNodoSearchType", SearchTypeEnum.EQUALS.getSearchType());
        }

        if(!ControlloCampi.campoVuoto(nodoStrutturaVO.getIdStruttura())){
            hParams.put("idStruttura", nodoStrutturaVO.getIdStruttura());
            hParams.put("idStrutturaSearchType", SearchTypeEnum.EQUALS.getSearchType());
        }

        if(!ControlloCampi.campoVuoto(nodoStrutturaVO.getIdNodoPadre())){
            hParams.put("idNodoPadre", nodoStrutturaVO.getIdNodoPadre());
            hParams.put("cognomeSearchType", SearchTypeEnum.EQUALS.getSearchType());
        }

        if(!ControlloCampi.campoVuoto(nodoStrutturaVO.getCdNodo())){
            hParams.put("cdNodo", nodoStrutturaVO.getCdNodo());
            hParams.put("cdNodoSearchType", SearchTypeEnum.EQUALS.getSearchType());
        }

        if(!ControlloCampi.campoVuoto(nodoStrutturaVO.getNmNodo())){
            hParams.put("nmNodo", nodoStrutturaVO.getNmNodo());
            hParams.put("nmNodoSearchType", SearchTypeEnum.EQUALS.getSearchType());
        }

        if(!ControlloCampi.campoVuoto(nodoStrutturaVO.getDsNodo())){
            hParams.put("dsNodo", nodoStrutturaVO.getDsNodo());
            hParams.put("dsNodoSearchType", SearchTypeEnum.EQUALS.getSearchType());
        }

        List<NodoStrutturaEntity> results = nodoStrutturaRepository.findAll(hParams, EnumManagementDomainTypeFunction.GET_ALL_NODO_STRUTTURA_FILTERED);

        return nodoStrutturaMapper.mapTo(results);
    }

    @Transactional(propagation = Propagation.REQUIRED)
    public NodoStrutturaVO createNodoStruttura(InserisciNodoStrutturaVO request) throws ApplicationException {
         
        NodoStrutturaEntity entity = nodoStrutturaMapper.mapFrom(request);
        HashMap<String, Object> hParams = new HashMap<>();

        hParams.put("cdNodo", entity.getCdNodo());
        NodoStrutturaEntity nodoStruttura = nodoStrutturaRepository.findEntity(
                hParams,
                EnumManagementDomainTypeFunction.GET_NODO_STRUTTURA_BY_COD_NODO
        );
        if (nodoStruttura != null) {
            throw new ApplicationException("Esiste già un nodo con codice nodo: " + entity.getCdNodo());
        }

        hParams.clear();
        
        hParams.put("nmNodo", entity.getNmNodo());
        nodoStruttura = nodoStrutturaRepository.findEntity(
                hParams,
                EnumManagementDomainTypeFunction.GET_NODO_STRUTTURA_BY_NOME_NODO
        );
        if (nodoStruttura != null) {
            throw new ApplicationException("Esiste già un nodo con nome nodo: " + entity.getNmNodo());
        }

        nodoStrutturaRepository.create(entity);

        return nodoStrutturaMapper.mapTo(entity);
    }


    @Transactional(propagation = Propagation.REQUIRED)
    public NodoStrutturaVO updateNodoStruttura(NodoStrutturaVO request) throws ApplicationException {
        if (ControlloCampi.campoVuoto(request)) {
            throw new ApplicationException(EnumMessage.DATO_OBBLIGATORIO, "payload");
        }
        if (ControlloCampi.campoVuoto(request.getKey())) {
            throw new ApplicationException(EnumMessage.DATO_OBBLIGATORIO, "ID Nodo");
        }

        // Recupera l'entità esistente dal database
        NodoStrutturaEntity entity;
        try {
            entity = nodoStrutturaRepository.findById(request.getKey());
        } catch (ObjectNotFoundException e) {
            throw new ApplicationException("Nessun utente trovato con id: " + request.getKey());
        }

        // Aggiorna l'entità esistente con i valori del VO (preserva i campi non presenti nel VO)
        nodoStrutturaMapper.updateEntityFromVO(request, entity);

        nodoStrutturaRepository.update(entity);

        // Mappatura dell'entità aggiornata a VO da restituire
        return nodoStrutturaMapper.mapTo(entity);
    }


    @Transactional(propagation = Propagation.REQUIRED)
    public Boolean deleteNodoStruttura(Long id) throws ApplicationException {

        if (ControlloCampi.campoVuoto(id)) {
            throw new ApplicationException(EnumMessage.DATO_OBBLIGATORIO, "Id Utente");
        }

        try {
            nodoStrutturaRepository.findById(id);
        } catch (ObjectNotFoundException e) {
            throw new ApplicationException("Nessun nodo trovato con id:" + id);
        }

        try {

            nodoStrutturaRepository.removeById(id);
        } catch (ApplicationException e) {
            log.error("Errore nella cancellazione dell'utente con id: {}", id);
            log.error("Exception: ", e);
            return false;
        }

        return true;
    }
}
