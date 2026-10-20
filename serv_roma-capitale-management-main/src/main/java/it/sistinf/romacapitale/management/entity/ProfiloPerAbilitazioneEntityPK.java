package it.sistinf.romacapitale.management.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Embeddable;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;

import java.io.Serializable;

/**
 * Entity ProfiloPerAbilitazioneEntityPK
 */
@Embeddable
@Data
@NoArgsConstructor
@EqualsAndHashCode
public class ProfiloPerAbilitazioneEntityPK implements Serializable {
    private static final long serialVersionUID = 1L;

    @Column(name = "id_profilo", nullable = false)
    private Long idProfilo;

    @Column(name = "id_abilitazione", nullable = false)
    private Long idAbilitazione;

}
