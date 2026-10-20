package it.sistinf.romacapitale.management.entity;

import it.sistinf.romacapitale.core.persistence.sql.AbstractPostgresEntity;
import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.NotFound;
import org.hibernate.annotations.NotFoundAction;

import java.io.Serializable;

/**
 * Entity UtentePerProfiloGetEntity
 */
@ToString
@EqualsAndHashCode(callSuper = false)
@Entity
@Data
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "utente_per_profilo_get")
public class UtentePerProfiloGetEntity extends AbstractPostgresEntity implements Serializable {


    private static final long serialVersionUID = 1L;

    @EmbeddedId
    private UtentePerProfiloGetEntityPK id;

    @ManyToOne(fetch = FetchType.EAGER)
    @NotFound(action = NotFoundAction.IGNORE)
    @JoinColumn(name = "id_profilo", referencedColumnName = "id_profilo", insertable = false, updatable = false)
    private ProfiloEntity profilo;

    @ManyToOne(fetch = FetchType.EAGER)
    @NotFound(action = NotFoundAction.IGNORE)
    @JoinColumn(name = "codice_struttura_ged", referencedColumnName = "codice", insertable = false, updatable = false)
    private StrutturaOrganizzativaGetEntity strutturaOrganizzativaGetEntity;

}
