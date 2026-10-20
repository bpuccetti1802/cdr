package it.sistinf.romacapitale.management.domain;

import it.sistinf.romacapitale.core.domain.AbstractDomain;
import it.sistinf.romacapitale.core.dto.PageInfo;
import it.sistinf.romacapitale.core.dto.RequestListDTO;
import it.sistinf.romacapitale.core.dto.ResponseListDTO;
import it.sistinf.romacapitale.core.exceptions.ApplicationException;
import it.sistinf.romacapitale.core.messages.EnumMessage;
import it.sistinf.romacapitale.core.utils.ControlloCampi;
import it.sistinf.romacapitale.integration.management.vo.StrutturaVO;
import it.sistinf.romacapitale.management.entity.StrutturaEntity;
import it.sistinf.romacapitale.management.enums.EnumManagementDomainTypeFunction;
import it.sistinf.romacapitale.management.mapper.StrutturaMapper;
import it.sistinf.romacapitale.management.repository.StrutturaRepository;
import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Propagation;
import org.springframework.transaction.annotation.Transactional;

import java.util.HashMap;
import java.util.List;

@Service
@AllArgsConstructor
@Slf4j
public class StrutturaDomain extends AbstractDomain {

    private final StrutturaMapper strutturaMapper;
    private final StrutturaRepository strutturaRepository;

    public ResponseListDTO<StrutturaVO> listStrutture(RequestListDTO<StrutturaVO> request) throws ApplicationException {

        HashMap<String, Object> hParams = getFilteredQueryMap(request);
        PageInfo pageInfo = new PageInfo();

        List<StrutturaEntity> results;
        Long totalCount;
        if (request.getPageInfo() != null) {
            results = strutturaRepository.findAll(
                    hParams,
                    request.getPageInfo().getPage(),
                    request.getPageInfo().getPageSize(),
                    EnumManagementDomainTypeFunction.GET_ALL_STRUTTURA_FILTERED
            );
            pageInfo = request.getPageInfo();
            totalCount = strutturaRepository.count(hParams, EnumManagementDomainTypeFunction.GET_ALL_STRUTTURA_FILTERED_COUNT);
        } else {
            results = strutturaRepository.findAll(hParams, EnumManagementDomainTypeFunction.GET_ALL_STRUTTURA_FILTERED);
            totalCount = (long) results.size();
        }

        ResponseListDTO<StrutturaVO> response = new ResponseListDTO<>();
        response.setList(strutturaMapper.mapTo(results));
        response.setPageInfo(pageInfo);
        response.getPageInfo().setTotalCount(totalCount);
        return response;
    }

    public StrutturaVO getStruttura(Long id) throws ApplicationException {
        return strutturaMapper.mapTo(strutturaRepository.findById(id));
    }

    @Transactional(propagation = Propagation.REQUIRED)
    public StrutturaVO createStruttura(StrutturaVO request) throws ApplicationException {
        if (ControlloCampi.campoVuoto(request)) {
            throw new ApplicationException(EnumMessage.DATO_OBBLIGATORIO, "payload");
        }
        if (ControlloCampi.campoVuoto(request.getNmStruttura())) {
            throw new ApplicationException(EnumMessage.DATO_OBBLIGATORIO, "nmStruttura");
        }
        if (ControlloCampi.campoVuoto(request.getDsStruttura())) {
            throw new ApplicationException(EnumMessage.DATO_OBBLIGATORIO, "dsStruttura");
        }

        StrutturaEntity entity = strutturaMapper.mapFrom(request);
        strutturaRepository.create(entity);
        return strutturaMapper.mapTo(entity);
    }

    @Transactional(propagation = Propagation.REQUIRED)
    public StrutturaVO updateStruttura(StrutturaVO request) throws ApplicationException {
    
        StrutturaEntity entity = strutturaMapper.mapFrom(request);
        strutturaRepository.update(entity);
        return strutturaMapper.mapTo(entity);
    }

    @Transactional(propagation = Propagation.REQUIRED)
    public Boolean deleteStruttura(Long id) throws ApplicationException {
        
        strutturaRepository.removeById(id); 
        return true;
    }
}

