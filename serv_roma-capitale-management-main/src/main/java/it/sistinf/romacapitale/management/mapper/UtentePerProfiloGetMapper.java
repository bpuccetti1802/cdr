package it.sistinf.romacapitale.management.mapper;

import it.sistinf.romacapitale.core.mapper.IFromToMapper;
import it.sistinf.romacapitale.core.mapper.ToEntity;
import it.sistinf.romacapitale.core.mapper.ToVO;
import it.sistinf.romacapitale.integration.management.vo.UtentePerProfiloGetVO;
import it.sistinf.romacapitale.management.entity.UtentePerProfiloGetEntity;
import org.mapstruct.InjectionStrategy;
import org.mapstruct.Mapper;

@Mapper(componentModel = "spring", injectionStrategy = InjectionStrategy.CONSTRUCTOR, uses = {ProfiloMapper.class, StrutturaOrganizzativaGetMapper.class})
public interface UtentePerProfiloGetMapper extends IFromToMapper<UtentePerProfiloGetVO, UtentePerProfiloGetEntity> {

    @Override
    @ToEntity
    UtentePerProfiloGetEntity mapFrom(UtentePerProfiloGetVO from);

    @Override
    @ToVO
    UtentePerProfiloGetVO mapTo(UtentePerProfiloGetEntity from);

}
