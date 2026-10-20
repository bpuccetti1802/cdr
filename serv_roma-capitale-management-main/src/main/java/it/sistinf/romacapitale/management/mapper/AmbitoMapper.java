package it.sistinf.romacapitale.management.mapper;

import it.sistinf.romacapitale.core.mapper.IFromToMapper;
import it.sistinf.romacapitale.core.mapper.ToEntity;
import it.sistinf.romacapitale.core.mapper.ToVO;
import it.sistinf.romacapitale.management.entity.AmbitoEntity;
import it.sistinf.romacapitale.integration.management.vo.AmbitoVO;
import org.mapstruct.InjectionStrategy;
import org.mapstruct.Mapper;

@Mapper(componentModel = "spring", injectionStrategy = InjectionStrategy.CONSTRUCTOR)
public interface AmbitoMapper extends IFromToMapper<AmbitoVO, AmbitoEntity> {

    @Override
    @ToEntity
    AmbitoEntity mapFrom(AmbitoVO from);

    @Override
    @ToVO
    AmbitoVO mapTo(AmbitoEntity from);

}
