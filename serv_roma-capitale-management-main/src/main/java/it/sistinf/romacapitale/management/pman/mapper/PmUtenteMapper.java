package it.sistinf.romacapitale.management.pman.mapper;

import it.sistinf.romacapitale.core.mapper.IFromToMapper;
import it.sistinf.romacapitale.management.entity.UtenteEntity;
import it.sistinf.romacapitale.management.pman.dto.UtenteDTO;
import org.mapstruct.InjectionStrategy;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;

@Mapper(componentModel = "spring", injectionStrategy = InjectionStrategy.CONSTRUCTOR, uses = {PmUtentePerProfiloMapper.class, PmEnteMapper.class})
public interface PmUtenteMapper extends IFromToMapper<UtenteDTO, UtenteEntity> {

    @Override
    @Mapping(source = "id", target = "id")
    UtenteEntity mapFrom(UtenteDTO from);

    @Override
    @Mapping(source = "id", target = "id")
    UtenteDTO mapTo(UtenteEntity from);

}
