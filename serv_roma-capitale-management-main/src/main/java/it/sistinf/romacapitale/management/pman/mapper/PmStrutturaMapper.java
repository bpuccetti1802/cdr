package it.sistinf.romacapitale.management.pman.mapper;

import it.sistinf.romacapitale.core.mapper.IFromToMapper;
import it.sistinf.romacapitale.management.entity.StrutturaEntity;
import it.sistinf.romacapitale.management.pman.dto.StrutturaDTO;
import org.mapstruct.InjectionStrategy;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;

@Mapper(componentModel = "spring", injectionStrategy = InjectionStrategy.CONSTRUCTOR )
public interface PmStrutturaMapper extends IFromToMapper<StrutturaDTO, StrutturaEntity> {

    @Override
    @Mapping(source = "id", target = "id")
    StrutturaEntity mapFrom(StrutturaDTO from);

    @Override
    @Mapping(source = "id", target = "id")
    StrutturaDTO mapTo(StrutturaEntity from);

}
