package it.sistinf.romacapitale.management.entity;

import it.sistinf.romacapitale.core.persistence.sql.AbstractPostgresEntity;
import jakarta.persistence.*;
import lombok.*;

import java.io.Serializable;
import java.util.List;

/**
 * Entity ProfiloEntity
 */
@ToString
@EqualsAndHashCode(callSuper = false)
@Entity
@Data
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "profilo")
public class ProfiloEntity extends AbstractPostgresEntity implements Serializable {


    private static final long serialVersionUID = 1L;

    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "profilo_seq_generator")
    @SequenceGenerator(name = "profilo_seq_generator", sequenceName = "profilo_id_profilo_seq", allocationSize = 1)
    @Column(name = "id_profilo")
    private Long id;

    @Column(name = "ds_profilo", nullable = false, length = 50)
    private String descrizione;

    @Column(name = "fg_profilo_default", nullable = false, length = 1)
    private String fgProfiloDefault;

    @Column(name = "cd_ruolo_profilo", length = 50)
    private String cdRuoloProfilo;

    @Column(name = "nm_valore")
    private Long nmValore;

    @Column(name = "cd_ambito", length = 2)
    private String cdAmbito;

    @Column(name = "cd_applicazione", length = 10)
    private String cdApplicazione;


    @OneToMany(fetch = FetchType.EAGER)
    @JoinColumn(name = "id_profilo", referencedColumnName = "id_profilo", insertable = false, updatable = false)
    private List<ProfiloPerAbilitazioneEntity> profiloPerAbilitazioneList;

//    @OneToMany(fetch=FetchType.EAGER)
//    @JoinColumn(name = "id_profilo", referencedColumnName = "id_profilo", insertable = false, updatable = false)
//    private List<UtentePerProfiloEntity> utentePerProfiloList;

}
