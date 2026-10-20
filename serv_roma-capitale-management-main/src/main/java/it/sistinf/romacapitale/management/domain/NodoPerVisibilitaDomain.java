package it.sistinf.romacapitale.management.domain;

import it.sistinf.romacapitale.core.domain.AbstractDomain;
import it.sistinf.romacapitale.integration.management.vo.NodoPerVisibilitaVO;
import it.sistinf.romacapitale.integration.management.vo.NodoStrutturaVO;
import it.sistinf.romacapitale.integration.management.vo.VisibilitaVO;
import it.sistinf.romacapitale.management.mapper.NodoStrutturaMapper;
import it.sistinf.romacapitale.management.repository.NodoStrutturaRepository;
import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;


@Service
@AllArgsConstructor
@Slf4j
public class NodoPerVisibilitaDomain extends AbstractDomain {


    private NodoStrutturaRepository nodoStrutturaRepository;

    private NodoStrutturaMapper nodoStrutturaMapper;


    public HashMap<String, String> getVisibilitaUfficioMap(Long idNodoStruttura) {

        HashMap<String, String> vOMap = new HashMap<String, String>();

        NodoStrutturaVO nodoStruttura = nodoStrutturaMapper
                .mapTo(nodoStrutturaRepository.findById(idNodoStruttura));

        for (NodoPerVisibilitaVO nVVO : nodoStruttura.getNodoPerVisibilitaList()) {
            VisibilitaVO v = nVVO.getVisibilita();

            String colonna = v.getNmColonna();

            if (vOMap.isEmpty()) {
                vOMap.put(colonna, v.getDsValore());
            } else {
                if (vOMap.containsKey(colonna)) {
                    vOMap.replace(colonna, (vOMap.get(colonna) + "," + v.getDsValore()));
                } else {
                    vOMap.put(colonna, v.getDsValore());
                }
            }
        }
        return vOMap;
    }

    public List<VisibilitaVO> listVisibilitaByNodo(Long idNodoStruttura) {
        NodoStrutturaVO nodoStruttura = nodoStrutturaMapper
                .mapTo(nodoStrutturaRepository.findById(idNodoStruttura));

        List<NodoPerVisibilitaVO> nodoPerVisibilitaList = nodoStruttura.getNodoPerVisibilitaList() != null ? nodoStruttura.getNodoPerVisibilitaList() : new ArrayList<>()   ;
        List<VisibilitaVO> visibilitaList = new ArrayList<>();

        if (nodoPerVisibilitaList == null) {
            return visibilitaList;
        }

        for (NodoPerVisibilitaVO nVVO : nodoPerVisibilitaList) {
            if (nVVO.getVisibilita() != null) {
                visibilitaList.add(nVVO.getVisibilita());
            }
        }

        return visibilitaList;
    }




}
