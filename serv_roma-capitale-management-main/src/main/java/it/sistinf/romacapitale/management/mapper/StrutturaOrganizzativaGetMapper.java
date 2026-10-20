package it.sistinf.romacapitale.management.mapper;

import it.sistinf.romacapitale.core.mapper.IFromToMapper;
import it.sistinf.romacapitale.integration.management.vo.StrutturaOrganizzativaGetVO;
import it.sistinf.romacapitale.management.entity.StrutturaOrganizzativaGetEntity;
import org.mapstruct.InjectionStrategy;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;

@Mapper(componentModel = "spring", injectionStrategy = InjectionStrategy.CONSTRUCTOR)
public interface StrutturaOrganizzativaGetMapper extends IFromToMapper<StrutturaOrganizzativaGetVO, StrutturaOrganizzativaGetEntity> {

    @Override
    @Mapping(source = "key", target = "codice")
    StrutturaOrganizzativaGetEntity mapFrom(StrutturaOrganizzativaGetVO from);

    @Override
    @Mapping(source = "codice", target = "key")
    StrutturaOrganizzativaGetVO mapTo(StrutturaOrganizzativaGetEntity from);

}
