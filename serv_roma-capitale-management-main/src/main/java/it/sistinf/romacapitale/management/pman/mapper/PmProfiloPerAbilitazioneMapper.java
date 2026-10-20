package it.sistinf.romacapitale.management.pman.mapper;

import it.sistinf.romacapitale.core.mapper.IFromToMapper;
import it.sistinf.romacapitale.management.entity.ProfiloPerAbilitazioneEntity;
import it.sistinf.romacapitale.management.pman.dto.ProfiloPerAbilitazioneDTO;
import org.mapstruct.InjectionStrategy;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;

@Mapper(componentModel = "spring", injectionStrategy = InjectionStrategy.CONSTRUCTOR)
public interface PmProfiloPerAbilitazioneMapper extends IFromToMapper<ProfiloPerAbilitazioneDTO, ProfiloPerAbilitazioneEntity> {

    @Override
    @Mapping(target = "id.idProfilo", source = "idProfilo")
    @Mapping(target = "id.idAbilitazione", source = "idAbilitazione")
    ProfiloPerAbilitazioneEntity mapFrom(ProfiloPerAbilitazioneDTO from);

    @Override
    @Mapping(target = "idProfilo", source = "id.idProfilo")
    @Mapping(target = "idAbilitazione", source = "id.idAbilitazione")
    ProfiloPerAbilitazioneDTO mapTo(ProfiloPerAbilitazioneEntity from);

}
