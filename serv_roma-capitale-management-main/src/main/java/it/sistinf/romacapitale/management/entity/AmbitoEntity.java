package it.sistinf.romacapitale.management.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import lombok.ToString;

import java.io.Serial;
import java.io.Serializable;

/**
 * Entity AmbitoEntity
 */
@ToString
@EqualsAndHashCode(callSuper = false)
@Entity
@Data
@NoArgsConstructor
@Table(name = "ambito")
public class AmbitoEntity implements Serializable {

    @Serial
    private static final long serialVersionUID = 1L;

    @Id
    @Column(name = "cd_ambito", nullable = false, length = 2)
    private String id;

    @Column(name = "ds_ambito", nullable = false, length = 50)
    private String dsAmbito;

}
