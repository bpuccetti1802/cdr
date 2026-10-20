package it.sistinf.romacapitale.management.entity;

import jakarta.persistence.*;
import lombok.*;

import java.io.Serializable;


@ToString
@EqualsAndHashCode(callSuper = false)
@Entity
@Data
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "struttura")
public class StrutturaEntity implements Serializable {

    private static final long serialVersionUID = 1L;

    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "struttura_seq_generator")
    @SequenceGenerator(name = "struttura_seq_generator", sequenceName = "struttura_id_struttura_seq", allocationSize = 1)
    @Column(name = "id_struttura")
    private Long id;

    @Column(name = "nm_struttura", nullable = false, length = 200)
    private String nmStruttura;

    @Column(name = "ds_struttura", nullable = false, length = 1000)
    private String dsStruttura;


}
