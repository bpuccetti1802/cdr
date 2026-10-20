package it.sistinf.romacapitale.management.mapper;

import it.sistinf.romacapitale.core.mapper.IFromToMapper;
import it.sistinf.romacapitale.management.entity.NodoPerVisibilitaEntity;
import it.sistinf.romacapitale.integration.management.vo.NodoPerVisibilitaVO;
import org.mapstruct.InjectionStrategy;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;

@Mapper(componentModel = "spring", injectionStrategy = InjectionStrategy.CONSTRUCTOR, uses = VisibilitaMapper.class)
public interface NodoPerVisibilitaMapper extends IFromToMapper<NodoPerVisibilitaVO, NodoPerVisibilitaEntity> {

    @Override
    @Mapping(source = "key", target = "id")
    NodoPerVisibilitaEntity mapFrom(NodoPerVisibilitaVO from);

    @Override
    @Mapping(source = "id", target = "key")
    NodoPerVisibilitaVO mapTo(NodoPerVisibilitaEntity from);

}
