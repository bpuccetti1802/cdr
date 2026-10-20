package it.sistinf.romacapitale.management.pman.mapper;

import it.sistinf.romacapitale.core.mapper.IFromToMapper;
import it.sistinf.romacapitale.management.entity.NodoStrutturaEntity;
import it.sistinf.romacapitale.management.mapper.NodoPerVisibilitaMapper;
import it.sistinf.romacapitale.management.pman.dto.NodoStrutturaDTO;
import org.mapstruct.InjectionStrategy;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;

@Mapper(componentModel = "spring", injectionStrategy = InjectionStrategy.CONSTRUCTOR, uses = {PmNodoPerVisibilitaMapper.class,PmStrutturaMapper.class})
public interface PmNodoStrutturaMapper extends IFromToMapper<NodoStrutturaDTO, NodoStrutturaEntity> {

    @Override
    @Mapping(source = "id", target = "id")
    NodoStrutturaEntity mapFrom(NodoStrutturaDTO from);

    @Override
    @Mapping(source = "id", target = "id")
    NodoStrutturaDTO mapTo(NodoStrutturaEntity from);

}
