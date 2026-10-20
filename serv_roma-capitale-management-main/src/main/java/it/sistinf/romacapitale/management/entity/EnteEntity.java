package it.sistinf.romacapitale.management.entity;

import jakarta.persistence.*;
import lombok.*;

import java.io.Serializable;
import java.util.Date;


@ToString
@EqualsAndHashCode(callSuper = false)
@Entity
@Data
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "ente")
public class EnteEntity implements Serializable {

    private static final long serialVersionUID = 1L;

    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "ente_seq_generator")
    @SequenceGenerator(name = "ente_seq_generator", sequenceName = "ente_id_ente_seq", allocationSize = 1)
    @Column(name = "id_ente")
    private Long id;

    @Column(name = "cd_ente", nullable = false)
    private Long cdEnte;

    @Column(name = "ds_ente", length = 250)
    private String dsEnte;


}
