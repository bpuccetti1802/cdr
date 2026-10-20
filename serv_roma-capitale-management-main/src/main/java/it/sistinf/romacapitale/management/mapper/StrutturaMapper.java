package it.sistinf.romacapitale.management.mapper;

import it.sistinf.romacapitale.core.mapper.IFromToMapper;
import it.sistinf.romacapitale.management.entity.StrutturaEntity;
import it.sistinf.romacapitale.integration.management.vo.StrutturaVO;
import org.mapstruct.InjectionStrategy;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;

@Mapper(componentModel = "spring", injectionStrategy = InjectionStrategy.CONSTRUCTOR )
public interface StrutturaMapper extends IFromToMapper<StrutturaVO, StrutturaEntity> {

    @Override
    @Mapping(source = "key", target = "id")
    StrutturaEntity mapFrom(StrutturaVO from);

    @Override
    @Mapping(source = "id", target = "key")
    StrutturaVO mapTo(StrutturaEntity from);

}
