package it.sistinf.romacapitale.management.mapper;

import it.sistinf.romacapitale.core.mapper.IFromToMapper;
import it.sistinf.romacapitale.integration.management.vo.InserisciUtenteVO;
import it.sistinf.romacapitale.integration.management.vo.ModificaUtenteVO;
import it.sistinf.romacapitale.integration.management.vo.UtenteVO;
import it.sistinf.romacapitale.management.entity.UtenteEntity;
import org.mapstruct.*;

@Mapper(componentModel = "spring", injectionStrategy = InjectionStrategy.CONSTRUCTOR, uses = {UtentePerProfiloMapper.class, EnteMapper.class})
public interface UtenteMapper extends IFromToMapper<UtenteVO, UtenteEntity> {

    @Override
    @Mapping(source = "key", target = "id")
    UtenteEntity mapFrom(UtenteVO from);

    @Mapping(source = "key", target = "id")
    @Mapping(target = "utentePerProfiloList", ignore = true)
    @Mapping(target = "flagUtenteAttivo", expression = "java(from.getFlagUtenteAttivo() != null ? from.getFlagUtenteAttivo() : 'S')")
    @Mapping(target = "nmTentativiPin", expression = "java(from.getNmTentativiPin() != null ? from.getNmTentativiPin() : 0L)")
    @Mapping(target = "nmTentativiLogin", expression = "java(from.getNmTentativiLogin() != null ? from.getNmTentativiLogin() : 0L)")
    @Mapping(target = "fgScadenzaAccount", expression = "java(from.getFgScadenzaAccount() != null ? from.getFgScadenzaAccount() : \"N\")")
    @Mapping(target = "fgScadenzaPassword", expression = "java(from.getFgScadenzaPassword() != null ? from.getFgScadenzaPassword() : \"N\")")
    @Mapping(target = "fgCambioPassword", expression = "java(from.getFgCambioPassword() != null ? from.getFgCambioPassword() : \"N\")")
    UtenteEntity mapFrom(InserisciUtenteVO from);

    @Override
    @Mapping(source = "id", target = "key")
    UtenteVO mapTo(UtenteEntity from);

    /**
     * Aggiorna un'entità esistente con i valori del VO.
     * I campi null nel VO NON sovrascrivono i valori esistenti nell'entità.
     */
    @Mapping(target = "id", ignore = true)
    @Mapping(target = "utenteInserimento", ignore = true)
    @Mapping(target = "timestampInserimento", ignore = true)
    @Mapping(target = "password", ignore = true)
    @BeanMapping(nullValuePropertyMappingStrategy = NullValuePropertyMappingStrategy.IGNORE)
    void updateEntityFromVO(ModificaUtenteVO source, @MappingTarget UtenteEntity target);

    /**
     * Converte i campi in maiuscolo solo quando si mappa DA VO verso Entity (insert/update).
     * NON viene eseguito durante mapTo() per evitare loop infiniti.
     */
    @AfterMapping
    default void normalizeFieldsToUpperCase(@MappingTarget UtenteEntity target) {
        // Questo metodo viene chiamato solo per mapFrom() e updateEntityFromVO()
        // Non viene chiamato per mapTo() perché il target è diverso
        if (target.getUsername() != null) {
            target.setUsername(target.getUsername().toUpperCase());
        }
        if (target.getNome() != null) {
            target.setNome(target.getNome().toUpperCase());
        }
        if (target.getCognome() != null) {
            target.setCognome(target.getCognome().toUpperCase());
        }
        if (target.getCodiceFiscale() != null) {
            target.setCodiceFiscale(target.getCodiceFiscale().toUpperCase());
        }
        if (target.getEmail() != null) {
            target.setEmail(target.getEmail().toUpperCase());
        }
        if (target.getFgScadenzaAccount() != null) {
            target.setFgScadenzaAccount(target.getFgScadenzaAccount().toUpperCase());
        }
        if (target.getFgScadenzaPassword() != null) {
            target.setFgScadenzaPassword(target.getFgScadenzaPassword().toUpperCase());
        }
        if (target.getFgCambioPassword() != null) {
            target.setFgCambioPassword(target.getFgCambioPassword().toUpperCase());
        }
        if (target.getCdStato() != null) {
            target.setCdStato(target.getCdStato().toUpperCase());
        }
        if (target.getTipoUtente() != null) {
            target.setTipoUtente(target.getTipoUtente().toUpperCase());
        }
    }

}
