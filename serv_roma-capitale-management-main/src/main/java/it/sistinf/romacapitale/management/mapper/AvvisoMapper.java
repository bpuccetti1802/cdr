package it.sistinf.romacapitale.management.mapper;

import it.sistinf.romacapitale.core.mapper.IFromToMapper;
import it.sistinf.romacapitale.integration.management.vo.AvvisoVO;
import it.sistinf.romacapitale.management.entity.AvvisoEntity;
import org.mapstruct.InjectionStrategy;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;

@Mapper(componentModel = "spring", injectionStrategy = InjectionStrategy.CONSTRUCTOR, uses = ApplicazioneMapper.class)
public interface AvvisoMapper extends IFromToMapper<AvvisoVO, AvvisoEntity> {

    @Override
    @Mapping(source = "key", target = "id")
    AvvisoEntity mapFrom(AvvisoVO from);

    @Override
    @Mapping(source = "id", target = "key")
    AvvisoVO mapTo(AvvisoEntity from);

}
