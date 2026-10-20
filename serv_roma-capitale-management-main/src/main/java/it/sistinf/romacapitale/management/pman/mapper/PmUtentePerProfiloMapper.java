package it.sistinf.romacapitale.management.pman.mapper;

import it.sistinf.romacapitale.core.mapper.IFromToMapper;
import it.sistinf.romacapitale.management.entity.UtentePerProfiloEntity;
import it.sistinf.romacapitale.management.pman.dto.UtentePerProfiloDTO;
import org.mapstruct.InjectionStrategy;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;

@Mapper(componentModel = "spring", injectionStrategy = InjectionStrategy.CONSTRUCTOR, uses = {PmNodoStrutturaMapper.class, PmProfiloMapper.class})
public interface PmUtentePerProfiloMapper extends IFromToMapper<UtentePerProfiloDTO, UtentePerProfiloEntity> {

    @Override
    @Mapping(target = "id.idUtente", source = "idUtente")
    @Mapping(target = "id.idProfilo", source = "idProfilo")
    UtentePerProfiloEntity mapFrom(UtentePerProfiloDTO from);

    @Override
    @Mapping(target = "idUtente", source = "id.idUtente")
    @Mapping(target = "idProfilo", source = "id.idProfilo")
    UtentePerProfiloDTO mapTo(UtentePerProfiloEntity from);

}
