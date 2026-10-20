package it.sistinf.romacapitale.management.pman.mapper;

import it.sistinf.romacapitale.core.mapper.IFromToMapper;
import it.sistinf.romacapitale.management.entity.EnteEntity;
import it.sistinf.romacapitale.management.pman.dto.EnteDTO;
import org.mapstruct.InjectionStrategy;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;

@Mapper(componentModel = "spring", injectionStrategy = InjectionStrategy.CONSTRUCTOR)
public interface PmEnteMapper extends IFromToMapper<EnteDTO, EnteEntity> {

    @Override
    @Mapping(source = "id", target = "id")
    EnteEntity mapFrom(EnteDTO from);

    @Override
    @Mapping(source = "id", target = "id")
    EnteDTO mapTo(EnteEntity from);

}
