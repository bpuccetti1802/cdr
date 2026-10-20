package it.sistinf.romacapitale.management.domain;

import it.sistinf.romacapitale.core.domain.AbstractDomain;
import it.sistinf.romacapitale.core.dto.PageInfo;
import it.sistinf.romacapitale.core.dto.RequestListDTO;
import it.sistinf.romacapitale.core.dto.ResponseListDTO;
import it.sistinf.romacapitale.core.exceptions.ApplicationException;
import it.sistinf.romacapitale.core.messages.EnumMessage;
import it.sistinf.romacapitale.core.utils.ControlloCampi;
import it.sistinf.romacapitale.integration.management.vo.AmbitoVO;
import it.sistinf.romacapitale.management.entity.AmbitoEntity;
import it.sistinf.romacapitale.management.enums.EnumManagementDomainTypeFunction;
import it.sistinf.romacapitale.management.mapper.AmbitoMapper;
import it.sistinf.romacapitale.management.repository.AmbitoRepository;
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
public class AmbitoDomain extends AbstractDomain {

    private final AmbitoMapper ambitoMapper;

    private AmbitoRepository ambitoRepository;

    public ResponseListDTO<AmbitoVO> listAmbiti(RequestListDTO<AmbitoVO> request) throws ApplicationException {
        
        HashMap<String, Object> hParams = getFilteredQueryMap(request);
        PageInfo pageInfo = new PageInfo();

        List<AmbitoEntity> results = null;
        Long totalCount;
        if (request.getPageInfo() != null) {
            results = ambitoRepository.findAll(
                    hParams, request.getPageInfo().getPage(), request.getPageInfo().getPageSize(), EnumManagementDomainTypeFunction.GET_ALL_AMBITI_FILTERED
            );
            pageInfo = request.getPageInfo();
            totalCount = ambitoRepository.count(hParams, EnumManagementDomainTypeFunction.GET_ALL_AMBITI_FILTERED_COUNT);
        } else {
            results = ambitoRepository.findAll(hParams, EnumManagementDomainTypeFunction.GET_ALL_AMBITI_FILTERED);
            totalCount = (long)results.size();
        }


        ResponseListDTO<AmbitoVO> response = new ResponseListDTO<>();

        response.setList(ambitoMapper.mapTo(results));
        response.setPageInfo(pageInfo);
        response.getPageInfo().setTotalCount(totalCount);
        return response;
    }

    public AmbitoVO getAmbito(String codice) throws ApplicationException {
        return ambitoMapper.mapTo(ambitoRepository.findById(codice));
    }




    @Transactional(propagation = Propagation.REQUIRED)
    public AmbitoVO createAmbito(AmbitoVO ambitoVO) {
        if (ControlloCampi.campoVuoto(ambitoVO)) {
            throw new ApplicationException(EnumMessage.DATO_OBBLIGATORIO, "payload");
        }
        if (ControlloCampi.campoVuoto(ambitoVO.getKey())) {
            throw new ApplicationException(EnumMessage.DATO_OBBLIGATORIO, "cdAmbito");
        }

        AmbitoEntity entity = ambitoMapper.mapFrom(ambitoVO);
        ambitoRepository.create(entity);
        return ambitoMapper.mapTo(entity);
    }


    @Transactional(propagation = Propagation.REQUIRED)
    public AmbitoVO updateAmbito(AmbitoVO ambitoVO) throws ApplicationException {
        if (ControlloCampi.campoVuoto(ambitoVO)) {
            throw new ApplicationException(EnumMessage.DATO_OBBLIGATORIO, "payload");
        }
        if (ControlloCampi.campoVuoto(ambitoVO.getKey())) {
            throw new ApplicationException(EnumMessage.DATO_OBBLIGATORIO, "cdAmbito");
        }

        AmbitoEntity entity = ambitoMapper.mapFrom(ambitoVO);
        ambitoRepository.update(entity);
        return ambitoMapper.mapTo(entity);
    }


    @Transactional(propagation = Propagation.REQUIRED)
    public AmbitoVO deleteAmbito(String cdAmbito) throws ApplicationException {
        if (ControlloCampi.campoVuoto(cdAmbito)) {
            throw new ApplicationException(EnumMessage.DATO_OBBLIGATORIO, "cdAmbito");
        }
        AmbitoEntity entity = ambitoRepository.findById(cdAmbito);

        ambitoRepository.removeById(entity.getId());
        return ambitoMapper.mapTo(entity);
    }

}
