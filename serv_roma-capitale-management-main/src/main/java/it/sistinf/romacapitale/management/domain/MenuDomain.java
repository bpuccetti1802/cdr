package it.sistinf.romacapitale.management.domain;

import it.sistinf.romacapitale.core.domain.AbstractDomain;
import it.sistinf.romacapitale.core.dto.PageInfo;
import it.sistinf.romacapitale.core.dto.RequestListDTO;
import it.sistinf.romacapitale.core.dto.ResponseListDTO;
import it.sistinf.romacapitale.core.exceptions.ApplicationException;
import it.sistinf.romacapitale.core.messages.EnumMessage;
import it.sistinf.romacapitale.core.utils.ControlloCampi;
import it.sistinf.romacapitale.integration.management.vo.MenuVO;
import it.sistinf.romacapitale.management.entity.MenuEntity;
import it.sistinf.romacapitale.management.enums.EnumManagementDomainTypeFunction;
import it.sistinf.romacapitale.management.mapper.MenuMapper;
import it.sistinf.romacapitale.management.repository.MenuRepository;
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
public class MenuDomain extends AbstractDomain {

    private final MenuMapper menuMapper;
    private final MenuRepository menuRepository;

    public ResponseListDTO<MenuVO> listMenus(RequestListDTO<MenuVO> request) throws ApplicationException {

        HashMap<String, Object> hParams = getFilteredQueryMap(request);
        PageInfo pageInfo = new PageInfo();

        List<MenuEntity> results;
        Long totalCount;
        if (request.getPageInfo() != null) {
            results = menuRepository.findAll(
                    hParams,
                    request.getPageInfo().getPage(),
                    request.getPageInfo().getPageSize(),
                    EnumManagementDomainTypeFunction.GET_ALL_MENU_FILTERED
            );
            pageInfo = request.getPageInfo();
            totalCount = menuRepository.count(hParams, EnumManagementDomainTypeFunction.GET_ALL_MENU_FILTERED_COUNT);
        } else {
            results = menuRepository.findAll(hParams, EnumManagementDomainTypeFunction.GET_ALL_MENU_FILTERED);
            totalCount = (long) results.size();
        }

        ResponseListDTO<MenuVO> response = new ResponseListDTO<>();
        response.setList(menuMapper.mapTo(results));
        response.setPageInfo(pageInfo);
        response.getPageInfo().setTotalCount(totalCount);
        return response;
    }

    public MenuVO getMenu(Long id) throws ApplicationException {
        return menuMapper.mapTo(menuRepository.findById(id));
    }

    @Transactional(propagation = Propagation.REQUIRED)
    public MenuVO createMenu(MenuVO request) throws ApplicationException {
        if (ControlloCampi.campoVuoto(request)) {
            throw new ApplicationException(EnumMessage.DATO_OBBLIGATORIO, "payload");
        }
        if (ControlloCampi.campoVuoto(request.getCdMenu())) {
            throw new ApplicationException(EnumMessage.DATO_OBBLIGATORIO, "cdMenu");
        }
        if (ControlloCampi.campoVuoto(request.getDsMenu())) {
            throw new ApplicationException(EnumMessage.DATO_OBBLIGATORIO, "dsMenu");
        }

        MenuEntity entity = menuMapper.mapFrom(request);
        menuRepository.create(entity);
        return menuMapper.mapTo(entity);
    }

    @Transactional(propagation = Propagation.REQUIRED)
    public MenuVO updateMenu(MenuVO request) throws ApplicationException {

        MenuEntity entity = menuMapper.mapFrom(request);
        menuRepository.update(entity);
        return menuMapper.mapTo(entity);
    }

    @Transactional(propagation = Propagation.REQUIRED)
    public Boolean deleteMenu(Long id) throws ApplicationException {
        
        menuRepository.removeById(id); 
        return true;
    }
}

