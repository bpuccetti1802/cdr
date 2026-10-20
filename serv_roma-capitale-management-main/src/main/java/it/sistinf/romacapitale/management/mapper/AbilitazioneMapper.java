package it.sistinf.romacapitale.management.mapper;

import it.sistinf.romacapitale.core.mapper.IFromToMapper;
import it.sistinf.romacapitale.management.entity.AbilitazioneEntity;
import it.sistinf.romacapitale.integration.management.vo.AbilitazioneVO;
import org.mapstruct.InjectionStrategy;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;

@Mapper(componentModel = "spring", injectionStrategy = InjectionStrategy.CONSTRUCTOR, uses = ApplicazioneMapper.class)
public interface AbilitazioneMapper extends IFromToMapper<AbilitazioneVO, AbilitazioneEntity> {

    @Override
    @Mapping(source = "key", target = "id")
    AbilitazioneEntity mapFrom(AbilitazioneVO from);

    @Override
    @Mapping(source = "id", target = "key")
    AbilitazioneVO mapTo(AbilitazioneEntity from);

}
