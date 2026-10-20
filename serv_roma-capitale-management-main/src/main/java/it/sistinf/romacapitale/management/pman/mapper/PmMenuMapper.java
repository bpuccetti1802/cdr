package it.sistinf.romacapitale.management.pman.mapper;

import it.sistinf.romacapitale.core.mapper.IFromToMapper;
import it.sistinf.romacapitale.management.entity.MenuEntity;
import it.sistinf.romacapitale.management.pman.dto.MenuDTO;
import org.mapstruct.InjectionStrategy;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;

@Mapper(componentModel = "spring", injectionStrategy = InjectionStrategy.CONSTRUCTOR)
public interface PmMenuMapper extends IFromToMapper<MenuDTO, MenuEntity> {

    @Override
    @Mapping(source = "id", target = "id")
    MenuEntity mapFrom(MenuDTO from);

    @Override
    @Mapping(source = "id", target = "id")
    MenuDTO mapTo(MenuEntity from);

}
