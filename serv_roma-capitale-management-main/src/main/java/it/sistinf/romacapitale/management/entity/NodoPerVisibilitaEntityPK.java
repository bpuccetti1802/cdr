package it.sistinf.romacapitale.management.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Embeddable;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;

import java.io.Serializable;


@Embeddable
@Data
@NoArgsConstructor
@EqualsAndHashCode
public class NodoPerVisibilitaEntityPK implements Serializable {

    private static final long serialVersionUID = 1L;

    @Column(name = "id_nodo", nullable = false)
    private Long idNodo;

    @Column(name = "id_visibilita", nullable = false)
    private Long idVisibilita;

}
