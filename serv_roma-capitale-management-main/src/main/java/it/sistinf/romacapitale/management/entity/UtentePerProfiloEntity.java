package it.sistinf.romacapitale.management.entity;

import it.sistinf.romacapitale.core.persistence.sql.AbstractPostgresEntity;
import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.NotFound;
import org.hibernate.annotations.NotFoundAction;

import java.io.Serializable;

/**
 * Entity UtentePerProfiloEntity
 */
@ToString
@EqualsAndHashCode(callSuper = false)
@Entity
@Data
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "utente_per_profilo")
public class UtentePerProfiloEntity extends AbstractPostgresEntity implements Serializable {


    private static final long serialVersionUID = 1L;

    @EmbeddedId
    private UtentePerProfiloEntityPK id;

    // attributi per servizio PMAN

    @Column(name = "id_nodo")
    private Long idNodo;


    @ManyToOne(fetch = FetchType.EAGER)
    @NotFound(action = NotFoundAction.IGNORE)
    @JoinColumn(name = "id_nodo", referencedColumnName = "id_nodo", insertable = false, updatable = false)
    private NodoStrutturaEntity nodoStruttura;


    @ManyToOne(fetch = FetchType.EAGER)
    @NotFound(action = NotFoundAction.IGNORE)
    @JoinColumn(name = "id_profilo", referencedColumnName = "id_profilo", insertable = false, updatable = false)
    private ProfiloEntity profilo;


}
