package it.sistinf.romacapitale.management.mapper;

import it.sistinf.romacapitale.core.mapper.IFromToMapper;
import it.sistinf.romacapitale.management.entity.EnteEntity;
import it.sistinf.romacapitale.management.vo.EnteVO;
import org.mapstruct.InjectionStrategy;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;

@Mapper(componentModel = "spring", injectionStrategy = InjectionStrategy.CONSTRUCTOR)
public interface EnteMapper extends IFromToMapper<EnteVO, EnteEntity> {

    @Override
    @Mapping(source = "key", target = "id")
    EnteEntity mapFrom(EnteVO from);

    @Override
    @Mapping(source = "id", target = "key")
    EnteVO mapTo(EnteEntity from);

}
