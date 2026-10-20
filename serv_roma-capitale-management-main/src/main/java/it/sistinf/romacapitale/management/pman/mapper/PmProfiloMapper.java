package it.sistinf.romacapitale.management.pman.mapper;

import it.sistinf.romacapitale.core.mapper.IFromToMapper;
import it.sistinf.romacapitale.management.entity.ProfiloEntity;
import it.sistinf.romacapitale.management.pman.dto.ProfiloDTO;
import org.mapstruct.InjectionStrategy;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;

@Mapper(componentModel = "spring", injectionStrategy = InjectionStrategy.CONSTRUCTOR, uses = PmProfiloPerAbilitazioneMapper.class)
public interface PmProfiloMapper extends IFromToMapper<ProfiloDTO, ProfiloEntity> {

    @Override
    @Mapping(source = "id", target = "id")
    ProfiloEntity mapFrom(ProfiloDTO from);

    @Override
    @Mapping(source = "id", target = "id")
    ProfiloDTO mapTo(ProfiloEntity from);

}
