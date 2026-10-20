package it.sistinf.romacapitale.management.entity;

import jakarta.persistence.*;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import lombok.ToString;
import org.hibernate.annotations.NotFound;
import org.hibernate.annotations.NotFoundAction;

import java.io.Serial;
import java.io.Serializable;
import java.util.Set;

/**
 * Entity ApplicazioneEntity
 */
@ToString
@EqualsAndHashCode(callSuper = false)
@Entity
@Data
@NoArgsConstructor
@Table(name = "applicazione")
public class ApplicazioneEntity implements Serializable {

    @Serial
    private static final long serialVersionUID = 1L;

    @EmbeddedId
    private ApplicazioneEntityPK id;

    @Column(name = "ds_applicazione", nullable = false, length = 60)
    private String dsApplicazione;

    @Column(name = "ds_endpoint", nullable = false, length = 125)
    private String dsEndpoint;

    @Column(name = "ds_context_root", nullable = false, length = 125)
    private String dsContextRoot;

    @Column(name = "cd_doc_manuale", length = 36)
    private String cdDocManuale;

    @Column(name = "cd_cloud", nullable = false, length = 1)
    private String cdCloud;

    @Column(name = "ds_service", nullable = false, length = 50)
    private String dsService;

    @Column(name = "ds_label", nullable = false, length = 30)
    private String dsLabel;

    @Column(name = "nm_ordine")
    private Long nmOrdine;

    @Column(name = "id_applicazione_sa", nullable = false, unique = true)
    private Long idApplicazioneSa; // identificativo App per servizio PMAN

    @Column(name = "cd_ambito_padre", length = 2)
    private String cdAmbitoPadre;

    @Column(name = "cd_applicazione_padre", length = 10)
    private String cdApplicazionePadre;

    @Column(name = "ty_login", length = 1)
    private String tyLogin;

    @Column(name = "ty_auth", length = 1)
    private String tyAuth;

    @Column(name = "fg_anonymous", length = 1)
    private String fgAnonymous;

    @Column(name = "fg_lista_strutture", length = 1)
    private String fgListaStrutture;

    @ManyToOne(fetch = FetchType.EAGER)
    @NotFound(action = NotFoundAction.IGNORE)
    @JoinColumn(name = "cd_ambito", referencedColumnName = "cd_ambito", insertable = false, updatable = false)
    private AmbitoEntity ambito;

    @ManyToOne(fetch = FetchType.EAGER)
    @NotFound(action = NotFoundAction.IGNORE)
    @JoinColumns({
            @JoinColumn(name = "cd_ambito_padre", referencedColumnName = "cd_ambito", insertable = false, updatable = false),
            @JoinColumn(name = "cd_applicazione_padre", referencedColumnName = "cd_applicazione", insertable = false, updatable = false)
    })
    private ApplicazioneEntity applicazionePadre;

//
//    @OneToMany(mappedBy = "applicazionePadre")
//    private Set<ApplicazioneEntity> applicazionefiglia;
}
