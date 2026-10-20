package it.sistinf.romacapitale.management.entity;

import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.NotFound;
import org.hibernate.annotations.NotFoundAction;

import java.io.Serializable;


@ToString
@EqualsAndHashCode(callSuper = false)
@Entity
@Data
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "visibilita")
public class VisibilitaEntity implements Serializable {

    private static final long serialVersionUID = 1L;

    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "visibilita_seq_generator")
    @SequenceGenerator(name = "visibilita_seq_generator", sequenceName = "visibilita_id_visibilita_seq", allocationSize = 1)
    @Column(name = "id_visibilita")
    private Long id;

    @Column(name = "nm_tabella", length = 250)
    private String nmTabella;

    @Column(name = "nm_colonna", nullable = false, length = 100)
    private String nmColonna;

    @Column(name = "ds_valore", nullable = false, length = 1000)
    private String dsValore;

    @Column(name = "ds_visibilita", nullable = false, length = 1000)
    private String dsVisibilita;

    @Column(name = "ds_breve", nullable = false, length = 50)
    private String dsBreve;

    @Column(name = "dipendenza")
    private Long idDipendenza;

    @ManyToOne(fetch = FetchType.EAGER)
    @NotFound(action = NotFoundAction.IGNORE)
    @JoinColumn(name = "dipendenza", referencedColumnName = "id_visibilita", insertable = false, updatable = false)
    private VisibilitaEntity dipendenza;

}
