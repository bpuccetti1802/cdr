package it.sistinf.romacapitale.management.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Embeddable;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;

import java.io.Serial;
import java.io.Serializable;

/**
 * Entity ApplicazioneEntityPK
 */
@Embeddable
@Data
@NoArgsConstructor
@AllArgsConstructor
@EqualsAndHashCode
public class ApplicazioneEntityPK implements Serializable {

    @Serial
    private static final long serialVersionUID = 1L;

    @Column(name = "cd_ambito", nullable = false, length = 2)
    private String cdAmbito;

    @Column(name = "cd_applicazione", nullable = false, length = 10)
    private String cdApplicazione;

}
