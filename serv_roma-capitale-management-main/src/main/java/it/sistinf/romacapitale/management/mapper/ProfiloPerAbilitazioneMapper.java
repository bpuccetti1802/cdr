package it.sistinf.romacapitale.management.mapper;

import it.sistinf.romacapitale.core.mapper.IFromToMapper;
import it.sistinf.romacapitale.integration.management.vo.ProfiloPerAbilitazioneVO;
import it.sistinf.romacapitale.management.entity.ProfiloPerAbilitazioneEntity;
import org.mapstruct.InjectionStrategy;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;

@Mapper(componentModel = "spring", injectionStrategy = InjectionStrategy.CONSTRUCTOR)
public interface ProfiloPerAbilitazioneMapper extends IFromToMapper<ProfiloPerAbilitazioneVO, ProfiloPerAbilitazioneEntity> {

    @Override
    @Mapping(source = "key", target = "id")
    ProfiloPerAbilitazioneEntity mapFrom(ProfiloPerAbilitazioneVO from);

    @Override
    @Mapping(source = "id", target = "key")
    ProfiloPerAbilitazioneVO mapTo(ProfiloPerAbilitazioneEntity from);

}
