package it.sistinf.romacapitale.management.pman.mapper;

import it.sistinf.romacapitale.core.mapper.IFromToMapper;
import it.sistinf.romacapitale.management.entity.AbilitazioneEntity;
import it.sistinf.romacapitale.management.pman.dto.AbilitazioneDTO;
import org.mapstruct.InjectionStrategy;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;

@Mapper(componentModel = "spring", injectionStrategy = InjectionStrategy.CONSTRUCTOR, uses = PmApplicazioneMapper.class)
public interface PmAbilitazioneMapper extends IFromToMapper<AbilitazioneDTO, AbilitazioneEntity> {

    @Override
    @Mapping(source = "id", target = "id")
    AbilitazioneEntity mapFrom(AbilitazioneDTO from);

    @Override
    @Mapping(source = "id", target = "id")
    AbilitazioneDTO mapTo(AbilitazioneEntity from);

}
