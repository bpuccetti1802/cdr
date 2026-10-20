package it.sistinf.romacapitale.management.entity;

import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.NotFound;
import org.hibernate.annotations.NotFoundAction;

import java.io.Serial;
import java.io.Serializable;

/**
 * Entity ConfigurazioneEntity
 */
@ToString
@EqualsAndHashCode(callSuper = false)
@Entity
@Data
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "configurazione")
public class ConfigurazioneEntity implements Serializable {

    @Serial
    private static final long serialVersionUID = 1L;

    @EmbeddedId
    private ConfigurazioneEntityPK id;

    @Column(name = "des_val_parametro", nullable = false, columnDefinition = "TEXT")
    private String desValParametro;

    @Column(name = "ty_parametro", length = 1)
    private String tyParametro;


    @ManyToOne(fetch = FetchType.EAGER)
    @NotFound(action = NotFoundAction.IGNORE)
    @JoinColumns({
            @JoinColumn(name = "cd_ambito", referencedColumnName = "cd_ambito", insertable = false, updatable = false),
            @JoinColumn(name = "cd_applicazione", referencedColumnName = "cd_applicazione", insertable = false, updatable = false),
    })
    private ApplicazioneEntity applicazione;
}
