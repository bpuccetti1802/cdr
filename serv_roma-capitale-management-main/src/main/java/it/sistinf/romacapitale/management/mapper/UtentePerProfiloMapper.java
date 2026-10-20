package it.sistinf.romacapitale.management.mapper;

import it.sistinf.romacapitale.core.mapper.IFromToMapper;
import it.sistinf.romacapitale.core.mapper.ToEntity;
import it.sistinf.romacapitale.core.mapper.ToVO;
import it.sistinf.romacapitale.integration.management.vo.UtentePerProfiloVO;
import it.sistinf.romacapitale.management.entity.UtentePerProfiloEntity;
import org.mapstruct.InjectionStrategy;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.MappingTarget;

@Mapper(componentModel = "spring", injectionStrategy = InjectionStrategy.CONSTRUCTOR, uses = {NodoStrutturaMapper.class, ProfiloMapper.class})
public interface UtentePerProfiloMapper extends IFromToMapper<UtentePerProfiloVO, UtentePerProfiloEntity> {

    @Override
    @ToEntity
    UtentePerProfiloEntity mapFrom(UtentePerProfiloVO from);

    @Override
    @ToVO
    UtentePerProfiloVO mapTo(UtentePerProfiloEntity from);

    @Override
    @Mapping(target = "nodoStruttura", qualifiedByName = "updateNodoStrutturaFromVO")
    UtentePerProfiloEntity mapFromTo(UtentePerProfiloVO from, @MappingTarget UtentePerProfiloEntity to);

}
