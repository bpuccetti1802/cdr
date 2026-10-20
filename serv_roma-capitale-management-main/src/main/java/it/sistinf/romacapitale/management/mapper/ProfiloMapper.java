package it.sistinf.romacapitale.management.mapper;

import it.sistinf.romacapitale.core.mapper.IFromToMapper;
import it.sistinf.romacapitale.integration.management.vo.ProfiloVO;
import it.sistinf.romacapitale.management.entity.ProfiloEntity;
import org.mapstruct.InjectionStrategy;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;

@Mapper(componentModel = "spring", injectionStrategy = InjectionStrategy.CONSTRUCTOR, uses = ProfiloPerAbilitazioneMapper.class)
public interface ProfiloMapper extends IFromToMapper<ProfiloVO, ProfiloEntity> {

    @Override
    @Mapping(source = "key", target = "id")
    ProfiloEntity mapFrom(ProfiloVO from);

    @Override
    @Mapping(source = "id", target = "key")
    ProfiloVO mapTo(ProfiloEntity from);

}
