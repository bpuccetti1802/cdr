package it.sistinf.romacapitale.management.mapper;

import it.sistinf.romacapitale.core.mapper.IFromToMapper;
import it.sistinf.romacapitale.integration.management.vo.InserisciNodoStrutturaVO;
import it.sistinf.romacapitale.integration.management.vo.NodoStrutturaVO;
import it.sistinf.romacapitale.management.entity.NodoStrutturaEntity;
import org.mapstruct.*;

@Mapper(componentModel = "spring", injectionStrategy = InjectionStrategy.CONSTRUCTOR, uses = {NodoPerVisibilitaMapper.class, StrutturaMapper.class})
public interface NodoStrutturaMapper extends IFromToMapper<NodoStrutturaVO, NodoStrutturaEntity> {

    @Override
    @Mapping(source = "key", target = "id")
    NodoStrutturaEntity mapFrom(NodoStrutturaVO from);

    @Override
    @Mapping(source = "id", target = "key")
    NodoStrutturaVO mapTo(NodoStrutturaEntity from);

    NodoStrutturaEntity mapFrom(InserisciNodoStrutturaVO from);

    /**
     * Aggiorna un'entità esistente con i valori del VO.
     * I campi null nel VO NON sovrascrivono i valori esistenti nell'entità.
     */
    @Named("updateNodoStrutturaFromVO")
    @BeanMapping(nullValuePropertyMappingStrategy = NullValuePropertyMappingStrategy.IGNORE)
    void updateEntityFromVO(NodoStrutturaVO source, @MappingTarget NodoStrutturaEntity target);

}
