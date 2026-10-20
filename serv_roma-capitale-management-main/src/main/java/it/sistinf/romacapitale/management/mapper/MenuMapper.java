package it.sistinf.romacapitale.management.mapper;

import it.sistinf.romacapitale.core.mapper.IFromToMapper;
import it.sistinf.romacapitale.integration.management.vo.MenuVO;
import it.sistinf.romacapitale.management.entity.MenuEntity;
import org.mapstruct.InjectionStrategy;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;

@Mapper(componentModel = "spring", injectionStrategy = InjectionStrategy.CONSTRUCTOR)
public interface MenuMapper extends IFromToMapper<MenuVO, MenuEntity> {

    @Override
    @Mapping(source = "key", target = "id")
    MenuEntity mapFrom(MenuVO from);

    @Override
    @Mapping(source = "id", target = "key")
    MenuVO mapTo(MenuEntity from);

}
