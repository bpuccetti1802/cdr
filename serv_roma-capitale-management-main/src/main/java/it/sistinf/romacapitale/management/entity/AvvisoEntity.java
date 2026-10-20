package it.sistinf.romacapitale.management.entity;

import it.sistinf.romacapitale.core.persistence.sql.AbstractPostgresEntity;
import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.NotFound;
import org.hibernate.annotations.NotFoundAction;

import java.io.Serializable;
import java.sql.Timestamp;

/**
 * Entity AvvisiEntity
 */
@ToString
@EqualsAndHashCode(callSuper=false)
@Entity
@Data
@NoArgsConstructor
@AllArgsConstructor
@Table(name="avviso")
public class AvvisoEntity extends AbstractPostgresEntity implements Serializable {

    private static final long serialVersionUID = 1L;

    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "avvisi_seq_generator")
    @SequenceGenerator(name = "avvisi_seq_generator", sequenceName = "avvisi_id_avviso_seq", allocationSize = 1)
    @Column(name = "id_avviso")
    private Long id;

    @Column(name = "cd_ambito", nullable = false, length = 2)
    private String cdAmbito;

    @Column(name = "cd_applicazione", nullable = false, length = 10)
    private String cdApplicazione;

    @Column(name = "ds_titolo_avviso", nullable = false, length = 100)
    private String dsTitoloAvviso;

    @Column(name = "ds_avviso", nullable = false, columnDefinition = "text")
    private String dsAvviso;

    @Column(name = "dt_inizio", nullable = false)
    private Timestamp dtInizio;

    @Column(name = "dt_fine", nullable = false)
    private Timestamp dtFine;

    @Column(name = "nm_priorita", nullable = false)
    private Short nmPriorita;

    @Column(name = "fl_attivo", nullable = false)
    private Boolean flAttivo;

    @ManyToOne(fetch = FetchType.EAGER)
    @NotFound(action = NotFoundAction.IGNORE)
    @JoinColumns(
        {
            @JoinColumn(name="cd_ambito", referencedColumnName="cd_ambito", updatable=false, insertable=false),
            @JoinColumn(name="cd_applicazione", referencedColumnName="cd_applicazione", updatable=false, insertable=false)
        })
    private ApplicazioneEntity applicazione;

}