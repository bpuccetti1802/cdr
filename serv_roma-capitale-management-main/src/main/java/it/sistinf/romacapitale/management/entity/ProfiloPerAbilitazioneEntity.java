package it.sistinf.romacapitale.management.entity;

import it.sistinf.romacapitale.core.persistence.sql.AbstractPostgresEntity;
import jakarta.persistence.*;
import lombok.*;

import java.io.Serializable;

@ToString
@EqualsAndHashCode(callSuper = false)
@Entity
@Data
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "profilo_per_abilitazione")
public class ProfiloPerAbilitazioneEntity extends AbstractPostgresEntity implements Serializable {
    private static final long serialVersionUID = 1L;

    @EmbeddedId
    private ProfiloPerAbilitazioneEntityPK id;

    @OneToOne(fetch= FetchType.EAGER)
    @JoinColumn(name = "id_abilitazione", referencedColumnName = "id_abilitazione", insertable = false, updatable = false)
    private AbilitazioneEntity abilitazione;


}
