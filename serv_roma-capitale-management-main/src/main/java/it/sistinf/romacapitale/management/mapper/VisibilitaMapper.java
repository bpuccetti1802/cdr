package it.sistinf.romacapitale.management.mapper;

import it.sistinf.romacapitale.core.mapper.IFromToMapper;
import it.sistinf.romacapitale.management.entity.VisibilitaEntity;
import it.sistinf.romacapitale.integration.management.vo.VisibilitaVO;
import org.mapstruct.InjectionStrategy;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;

@Mapper(componentModel = "spring", injectionStrategy = InjectionStrategy.CONSTRUCTOR)
public interface VisibilitaMapper extends IFromToMapper<VisibilitaVO, VisibilitaEntity> {

    @Override
    @Mapping(source = "key", target = "id")
    VisibilitaEntity mapFrom(VisibilitaVO from);

    @Override
    @Mapping(source = "id", target = "key")
    VisibilitaVO mapTo(VisibilitaEntity from);

}
