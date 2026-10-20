package it.sistinf.romacapitale.management.pman.mapper;

import it.sistinf.romacapitale.core.mapper.IFromToMapper;
import it.sistinf.romacapitale.management.entity.ApplicazioneEntity;
import it.sistinf.romacapitale.management.pman.dto.ApplicazioneDTO;
import org.mapstruct.InjectionStrategy;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;

@Mapper(componentModel = "spring", injectionStrategy = InjectionStrategy.CONSTRUCTOR)
public interface PmApplicazioneMapper extends IFromToMapper<ApplicazioneDTO, ApplicazioneEntity> {

    @Override
    @Mapping(source = "idApplicazioneSa", target = "idApplicazioneSa")
    ApplicazioneEntity mapFrom(ApplicazioneDTO from);

    @Override
    @Mapping(source = "idApplicazioneSa", target = "idApplicazioneSa")
    ApplicazioneDTO mapTo(ApplicazioneEntity from);

}
