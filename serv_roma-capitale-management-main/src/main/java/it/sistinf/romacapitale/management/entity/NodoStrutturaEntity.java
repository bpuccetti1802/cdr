package it.sistinf.romacapitale.management.entity;

import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.NotFound;
import org.hibernate.annotations.NotFoundAction;

import java.io.Serializable;
import java.util.List;


@ToString
@EqualsAndHashCode(callSuper = false)
@Entity
@Data
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "nodo_struttura")
public class NodoStrutturaEntity implements Serializable {

    private static final long serialVersionUID = 1L;

    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "nodoStruttura_seq_generator")
    @SequenceGenerator(name = "nodoStruttura_seq_generator", sequenceName = "nodoStruttura_id_nodo_seq", allocationSize = 1)
    @Column(name = "id_nodo")
    private Long id;

    @Column(name = "id_struttura", nullable = false)
    private Long idStruttura;

    @Column(name = "id_nodo_padre")
    private Long idNodoPadre;

    @Column(name = "cd_nodo", nullable = false, length = 50)
    private String cdNodo;

    @Column(name = "nm_nodo", nullable = false, length = 200)
    private String nmNodo;

    @Column(name = "ds_nodo", length = 1000)
    private String dsNodo;


    @ManyToOne(fetch = FetchType.EAGER)
    @NotFound(action = NotFoundAction.IGNORE)
    @JoinColumn(name = "id_struttura", referencedColumnName = "id_struttura", insertable = false, updatable = false)
    private StrutturaEntity struttura;


    @OneToMany(fetch = FetchType.EAGER)
    @JoinColumn(name = "id_nodo", referencedColumnName = "id_nodo", insertable = false, updatable = false)
    private List<NodoPerVisibilitaEntity> nodoPerVisibilitaList;


}
