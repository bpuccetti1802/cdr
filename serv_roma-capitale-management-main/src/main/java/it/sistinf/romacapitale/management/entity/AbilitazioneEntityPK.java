package it.sistinf.romacapitale.management.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Embeddable;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;

import java.io.Serializable;

/**
 * Entity AbilitazioneEntityPK
 */
@Embeddable
@Data
@NoArgsConstructor
@EqualsAndHashCode
public class AbilitazioneEntityPK implements Serializable {

    private static final long serialVersionUID = 1L;

    @Column(name = "cd_ambito", nullable = false)
    private String cdAmbito;

    @Column(name = "cd_applicazione", nullable = false)
    private String cdApplicazione;

    @Column(name = "cd_abilitazione", nullable = false)
    private String cdAbilitazione;

}
