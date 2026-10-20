package it.sistinf.romacapitale.management.mapper;

import it.sistinf.romacapitale.core.mapper.IFromToMapper;
import it.sistinf.romacapitale.core.mapper.ToEntity;
import it.sistinf.romacapitale.core.mapper.ToVO;
import it.sistinf.romacapitale.management.entity.ApplicazioneEntity;
import it.sistinf.romacapitale.integration.management.vo.ApplicazioneVO;
import org.mapstruct.*;

@Mapper(componentModel = "spring", injectionStrategy = InjectionStrategy.CONSTRUCTOR, uses = AmbitoMapper.class)
public interface ApplicazioneMapper extends IFromToMapper<ApplicazioneVO, ApplicazioneEntity> {

    @Override
    @ToEntity
    ApplicazioneEntity mapFrom(ApplicazioneVO from);

    @Override
    @ToVO
    ApplicazioneVO mapTo(ApplicazioneEntity from);

    @Named("updateApplicazioneFromVO")
    @BeanMapping(nullValuePropertyMappingStrategy = NullValuePropertyMappingStrategy.IGNORE)
    void updateEntityFromVO(ApplicazioneVO source, @MappingTarget ApplicazioneEntity target);

}
