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
@Table(name = "menu")
public class MenuEntity implements Serializable {

    private static final long serialVersionUID = 1L;

    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "menu_seq_generator")
    @SequenceGenerator(name = "menu_seq_generator", sequenceName = "menu_id_menu_seq", allocationSize = 1)
    @Column(name = "id_menu")
    private Long id;

    @Column(name = "cd_menu", nullable = false, length = 50)
    private String cdMenu;

    @Column(name = "ds_menu", length = 100)
    private String dsMenu;

    @Column(name = "id_applicazione_sa")
    private Long idApplicazioneSa;


}
