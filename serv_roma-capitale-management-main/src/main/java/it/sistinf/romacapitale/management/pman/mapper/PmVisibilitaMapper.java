package it.sistinf.romacapitale.management.pman.mapper;

import it.sistinf.romacapitale.core.mapper.IFromToMapper;
import it.sistinf.romacapitale.management.entity.VisibilitaEntity;
import it.sistinf.romacapitale.management.pman.dto.VisibilitaDTO;
import org.mapstruct.InjectionStrategy;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;

@Mapper(componentModel = "spring", injectionStrategy = InjectionStrategy.CONSTRUCTOR)
public interface PmVisibilitaMapper extends IFromToMapper<VisibilitaDTO, VisibilitaEntity> {

    @Override
    @Mapping(source = "id", target = "id")
    VisibilitaEntity mapFrom(VisibilitaDTO from);

    @Override
    @Mapping(source = "id", target = "id")
    VisibilitaDTO mapTo(VisibilitaEntity from);

}
