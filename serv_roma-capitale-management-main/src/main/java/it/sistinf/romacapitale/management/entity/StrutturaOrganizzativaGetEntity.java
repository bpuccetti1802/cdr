package it.sistinf.romacapitale.management.entity;

import jakarta.persistence.*;
import lombok.*;

import java.io.Serializable;


@ToString
@EqualsAndHashCode(callSuper = false)
@Entity
@Data
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "v_str_organizzativa")
public class StrutturaOrganizzativaGetEntity implements Serializable {

    private static final long serialVersionUID = 1L;

    @Id
    @Column(name = "codice", nullable = false  , length = 25)
    private String codice;

    @Column(name = "descrizione", length = 255)
    private String descrizione;

    @Column(name = "descrizione_breve", length = 255)
    private String descBreve;

    @Column(name = "codice_str_padre", length = 25)
    private String codStrutturaPadre;

    @Column(name = "ordine_organigramma", length = 50)
    private String ordineOrganigramma;

    @Column(name = "codice_responsabile")
    private Long codiceResponsabile;

}
