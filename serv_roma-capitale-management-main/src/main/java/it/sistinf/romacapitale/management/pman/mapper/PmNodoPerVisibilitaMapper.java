package it.sistinf.romacapitale.management.pman.mapper;

import it.sistinf.romacapitale.core.mapper.IFromToMapper;
import it.sistinf.romacapitale.integration.management.vo.NodoPerVisibilitaVO;
import it.sistinf.romacapitale.management.entity.NodoPerVisibilitaEntity;
import it.sistinf.romacapitale.management.mapper.VisibilitaMapper;
import it.sistinf.romacapitale.management.pman.dto.NodoPerVisibilitaDTO;
import org.mapstruct.InjectionStrategy;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;

@Mapper(componentModel = "spring", injectionStrategy = InjectionStrategy.CONSTRUCTOR, uses = PmVisibilitaMapper.class)
public interface PmNodoPerVisibilitaMapper extends IFromToMapper<NodoPerVisibilitaDTO, NodoPerVisibilitaEntity> {

    @Override
    @Mapping(target = "id.idNodo", source = "idNodo")
    @Mapping(target = "id.idVisibilita", source = "idVisibilita")
    NodoPerVisibilitaEntity mapFrom(NodoPerVisibilitaDTO from);

    @Override
    @Mapping(target = "idNodo", source = "id.idNodo")
    @Mapping(target = "idVisibilita", source = "id.idVisibilita")
    NodoPerVisibilitaDTO mapTo(NodoPerVisibilitaEntity from);

}
