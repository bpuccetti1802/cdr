package it.sistinf.romacapitale.management.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Embeddable;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;

import java.io.Serializable;

/**
 * Entity UtentePerProfiloGetEntityPK
 */
@Embeddable
@Data
@NoArgsConstructor
@EqualsAndHashCode
public class UtentePerProfiloGetEntityPK implements Serializable {
    private static final long serialVersionUID = 1L;

    @Column(name = "id_utente", nullable = false)
    private Long idUtente;

    @Column(name = "id_profilo", nullable = false)
    private Long idProfilo;

    @Column(name = "codice_struttura_ged", nullable = false)
    private String codStrutturaGed;

}
