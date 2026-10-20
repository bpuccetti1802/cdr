package it.sistinf.romacapitale.management.mapper;

import it.sistinf.romacapitale.core.mapper.IFromToMapper;
import it.sistinf.romacapitale.core.mapper.ToEntity;
import it.sistinf.romacapitale.core.mapper.ToVO;
import it.sistinf.romacapitale.management.entity.ConfigurazioneEntity;
import it.sistinf.romacapitale.management.vo.ConfigurazioneVO;
import org.mapstruct.InjectionStrategy;
import org.mapstruct.Mapper;

@Mapper(componentModel = "spring", injectionStrategy = InjectionStrategy.CONSTRUCTOR, uses = {ApplicazioneMapper.class})
public interface ConfigurazioneMapper extends IFromToMapper<ConfigurazioneVO, ConfigurazioneEntity> {

    @Override
    @ToEntity
    ConfigurazioneEntity mapFrom(ConfigurazioneVO from);

    @Override
    @ToVO
    ConfigurazioneVO mapTo(ConfigurazioneEntity from);

}
