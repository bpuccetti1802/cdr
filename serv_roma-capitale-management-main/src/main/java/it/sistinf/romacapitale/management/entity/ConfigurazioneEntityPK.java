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
 * Entity ConfigurazioneEntityPK
 */
@Embeddable
@Data
@NoArgsConstructor
@AllArgsConstructor
@EqualsAndHashCode
public class ConfigurazioneEntityPK implements Serializable {

    @Serial
    private static final long serialVersionUID = 1L;

    @Column(name = "cd_ambito", nullable = false, length = 2)
    private String cdAmbito;

    @Column(name = "cd_applicazione", nullable = false, length = 10)
    private String cdApplicazione;

    @Column(name = "des_nome_parametro", nullable = false, length = 100)
    private String desNomeParametro;
}
