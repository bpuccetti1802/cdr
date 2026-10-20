package it.sistinf.romacapitale.management.entity;

import it.sistinf.romacapitale.core.persistence.sql.AbstractPostgresEntity;
import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.NotFound;
import org.hibernate.annotations.NotFoundAction;

import java.io.Serializable;

/**
 * Entity AbilitazioneEntity
 */
@ToString
@EqualsAndHashCode(callSuper=false)
@Entity
@Data
@NoArgsConstructor
@AllArgsConstructor
@Table(name="abilitazione")
public class AbilitazioneEntity extends AbstractPostgresEntity implements Serializable {

    private static final long serialVersionUID = 1L;

    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "abilitazione_seq_generator")
    @SequenceGenerator(name = "abilitazione_seq_generator", sequenceName = "abilitazione_id_abilitazione_seq", allocationSize = 1)
    @Column(name = "id_abilitazione")
    private Long id;

    @Column(name = "cd_ambito", nullable = false)
    private String cdAmbito;

    @Column(name = "cd_applicazione", nullable = false)
    private String cdApplicazione;

    @Column(name = "cd_abilitazione", nullable = false)
    private String cdAbilitazione;

    @Column(name = "ds_abilitazione", nullable = false, length = 10)
    private String descAbilitazione;

    @Column(name = "cd_esterno", length = 100)
    private String cdEsterno;

    @Column(name = "id_menu")
    private Long idMenu;

//    @OneToMany(fetch= FetchType.EAGER)
//    @JoinColumns(
//            {
//                    @JoinColumn(name="cd_ambito", referencedColumnName="cd_ambito",updatable=false,insertable=false),
//                    @JoinColumn(name="cd_applicazione", referencedColumnName="cd_applicazione",updatable=false,insertable=false),
//                    @JoinColumn(name="cd_abilitazione", referencedColumnName="cd_abilitazione",updatable=false,insertable=false)
//            })
//    private List<ProfiloPerAbilitazioneEntity> profiloPerAbilitazioneList;


    @OneToOne(fetch = FetchType.EAGER)
    @NotFound(action = NotFoundAction.IGNORE)
    @JoinColumns(
            {
                    @JoinColumn(name="cd_ambito", referencedColumnName="cd_ambito",updatable=false,insertable=false),
                    @JoinColumn(name="cd_applicazione", referencedColumnName="cd_applicazione",updatable=false,insertable=false),
            })
    private ApplicazioneEntity applicazione;

    @ManyToOne(fetch = FetchType.EAGER)
    @NotFound(action = NotFoundAction.IGNORE)
    @JoinColumn(name = "id_menu", referencedColumnName = "id_menu", insertable = false, updatable = false)
    private MenuEntity menu;


}

