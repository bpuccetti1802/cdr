package it.sistinf.romacapitale.management.domain;

import it.sistinf.romacapitale.core.domain.AbstractDomain;
import it.sistinf.romacapitale.core.dto.PageInfo;
import it.sistinf.romacapitale.core.dto.RequestListDTO;
import it.sistinf.romacapitale.core.dto.ResponseListDTO;
import it.sistinf.romacapitale.integration.management.vo.NodoPerVisibilitaVO;
import it.sistinf.romacapitale.integration.management.vo.UtentePerProfiloVO;
import it.sistinf.romacapitale.integration.management.vo.UtenteVO;
import it.sistinf.romacapitale.integration.management.vo.VisibilitaVO;
import it.sistinf.romacapitale.management.entity.VisibilitaEntity;
import it.sistinf.romacapitale.management.enums.EnumManagementDomainTypeFunction;
import it.sistinf.romacapitale.management.mapper.VisibilitaMapper;
import it.sistinf.romacapitale.management.repository.VisibilitaRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.function.Function;
import java.util.function.Predicate;
import java.util.stream.Collectors;

/**
 * @author Daniele Inferrera
 * @since 24/10/2025
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class VisibilitaDomain extends AbstractDomain {

    private final UtenteDomain utenteDomain;

    private final VisibilitaRepository visibilitaRepository;
    private final VisibilitaMapper visibilitaMapper;

    @Transactional
    public void updateVisibilita(VisibilitaVO toUpdate) {
        visibilitaRepository.update(visibilitaMapper.mapFrom(toUpdate));
    }

    @Transactional
    public void deleteVisibilita(VisibilitaVO toDelete) {
        visibilitaRepository.removeById(toDelete.getKey());
    }

    @Transactional
    public void deleteVisibilitaById(Long id) {
        visibilitaRepository.removeById(id);
    }

    public List<VisibilitaVO> listVisibilita() {
        UtenteVO utente = utenteDomain.getUtenteByUsername(getCurrentUser().getUsername());
        List<VisibilitaVO> visibilita = new ArrayList<>();
        List<UtentePerProfiloVO> listProfili = utente.getUtentePerProfiloList();
        for(UtentePerProfiloVO profilo : listProfili) {
            if(profilo.getNodoStruttura() == null || profilo.getNodoStruttura().getNodoPerVisibilitaList() == null) {
                continue;
            }
            List<NodoPerVisibilitaVO> nodoList = profilo.getNodoStruttura().getNodoPerVisibilitaList();
            for(NodoPerVisibilitaVO nodo : nodoList) {
                if(nodo.getVisibilita() != null) {
                    visibilita.add(nodo.getVisibilita());
                }
            }
        }
        return visibilita.stream().filter(distinctByKey(VisibilitaVO::getKey)).collect(Collectors.toList());
    }

    public ResponseListDTO<VisibilitaVO> listVisibilita(RequestListDTO<VisibilitaVO> request) {
        HashMap<String, Object> hParams = getFilteredQueryMap(request);
        PageInfo pageInfo = new PageInfo();

        List<VisibilitaEntity> results;
        Long totalCount;
        if (request.getPageInfo() != null) {
            results = visibilitaRepository.findAll(
                    hParams, request.getPageInfo().getPage(), request.getPageInfo().getPageSize(), EnumManagementDomainTypeFunction.GET_ALL_VISIBILITA_FILTERED
            );
            pageInfo = request.getPageInfo();
            totalCount = visibilitaRepository.count(hParams, EnumManagementDomainTypeFunction.GET_ALL_VISIBILITA_FILTERED_COUNT);
        } else {
            results = visibilitaRepository.findAll(hParams, EnumManagementDomainTypeFunction.GET_ALL_VISIBILITA_FILTERED);
            totalCount = (long) results.size();
        }

        ResponseListDTO<VisibilitaVO> response = new ResponseListDTO<>();
        response.setList(visibilitaMapper.mapTo(results));
        response.setPageInfo(pageInfo);
        response.getPageInfo().setTotalCount(totalCount);
        return response;
    }

    private <T> Predicate<T> distinctByKey(Function<? super T, ?> keyExtractor) {
        Set<Object> seen = new HashSet<>();
        return t -> seen.add(keyExtractor.apply(t));
    }

}
