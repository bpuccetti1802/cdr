package it.sistinf.romacapitale.management.entity;

import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.NotFound;
import org.hibernate.annotations.NotFoundAction;

import java.io.Serializable;


@ToString
@EqualsAndHashCode(callSuper = false)
@Entity
@Data
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "nodo_per_visibilita")
public class NodoPerVisibilitaEntity implements Serializable {

    private static final long serialVersionUID = 1L;

    @EmbeddedId
    private NodoPerVisibilitaEntityPK id;

    @ManyToOne(fetch = FetchType.EAGER)
    @NotFound(action = NotFoundAction.IGNORE)
    @JoinColumn(name = "id_visibilita", referencedColumnName = "id_visibilita", insertable = false, updatable = false)
    private VisibilitaEntity visibilita;


}
