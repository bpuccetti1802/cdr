package it.sistinf.romacapitale.management.entity;

import it.sistinf.romacapitale.core.persistence.sql.AbstractPostgresEntity;
import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.NotFound;
import org.hibernate.annotations.NotFoundAction;

import java.io.Serializable;
import java.util.Date;
import java.util.List;

/**
 * Entity UtenteEntity
 */
@ToString
@EqualsAndHashCode(callSuper = false)
@Entity
@Data
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "utente")
public class UtenteEntity extends AbstractPostgresEntity implements Serializable {

    private static final long serialVersionUID = 1L;

    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "utente_seq_generator")
    @SequenceGenerator(name = "utente_seq_generator", sequenceName = "utente_id_utente_seq", allocationSize = 1)
    @Column(name = "id_utente")
    private Long id;

    @Column(name = "ds_username", nullable = false, length = 50)
    private String username;

    @Column(name = "ds_password", nullable = false, length = 260)
    private String password;

    @Column(name = "ds_nome", nullable = false, length = 60)
    private String nome;

    @Column(name = "ds_cognome", nullable = false, length = 60)
    private String cognome;

    @Column(name = "cd_fiscale", nullable = false, length = 16)
    private String codiceFiscale;

    @Column(name = "nm_telefono", nullable = false, length = 20)
    private String numeroTelefono;

    @Column(name = "ds_email", nullable = false, length = 255)
    private String email;

    @Column(name = "ds_ufficio", nullable = false, length = 255)
    private String ufficio;

    @Column(name = "dt_ultimo_login")
    private Date ultimoLogin;

    @Column(name = "fg_attivo_sn", nullable = false, length = 1)
    private Character flagUtenteAttivo;

    //    attributi PMAN-Management

    @Column(name = "nm_tentativi_pin")
    private Long nmTentativiPin;

    @Column(name = "nm_tentativi_login")
    private Long nmTentativiLogin;

    @Column(name = "fg_scad_account", length = 1)
    private String fgScadenzaAccount;

    @Column(name = "fg_scad_password", length = 1)
    private String fgScadenzaPassword;

    @Column(name = "fg_cambio_password", length = 1)
    private String fgCambioPassword;

    @Column(name = "ts_agg_password")
    private Date tsAggiornamentoPass;

    @Column(name = "cd_cnt")
    private Long cdCnt;

    @Column(name = "cd_stato", length = 1)
    private String cdStato;

    @Column(name = "ty_utente", length = 1)
    private String tipoUtente;

    @Column(name = "id_ente")
    private Long idEnte;


    @OneToMany(fetch = FetchType.EAGER)
    @JoinColumn(name = "id_utente", referencedColumnName = "id_utente", insertable = false, updatable = false)
    private List<UtentePerProfiloEntity> utentePerProfiloList;


    @ManyToOne(fetch = FetchType.EAGER)
    @NotFound(action = NotFoundAction.IGNORE)
    @JoinColumn(name = "id_ente", referencedColumnName = "id_ente", insertable = false, updatable = false)
    private EnteEntity ente;

}
