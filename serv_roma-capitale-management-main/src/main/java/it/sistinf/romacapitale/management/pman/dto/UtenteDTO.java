package it.sistinf.romacapitale.management.pman.dto;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonRootName;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.ToString;

import java.math.BigDecimal;
import java.util.Date;
import java.util.List;

/**
 * Classe UtenteVO
 */
@Data
@ToString
@NoArgsConstructor
@JsonRootName("PmUtentiDTO")
public class UtenteDTO {

    @JsonProperty("idUtente")
    private Long id;

    @JsonProperty("abilitato")
    private Character flagUtenteAttivo;

    @JsonProperty("capRcp")
    private BigDecimal capRcp;

    @JsonProperty("capRes")
    private BigDecimal capRes;

    @JsonProperty("cellulare")
    private String cellulare;

    @JsonProperty("cerCommonName")
    private String cerCommonName;

    @JsonProperty("cerOrganizationUnit")
    private String cerOrganizationUnit;

    @JsonProperty("civRcp")
    private BigDecimal civRcp;

    @JsonProperty("civRes")
    private BigDecimal civRes;

    @JsonProperty("codCnt")
    private BigDecimal cdCnt;

    @JsonProperty("codComNas")
    private String codComNas;

    @JsonProperty("codComRcp")
    private String codComRcp;

    @JsonProperty("codComRes")
    private String codComRes;

    @JsonProperty("codFis")
    private String codiceFiscale;

    @JsonProperty("codFisRl")
    private String codFisRl;

    @JsonProperty("codIndRcp")
    private BigDecimal codIndRcp;

    @JsonProperty("codIndRes")
    private BigDecimal codIndRes;

    @JsonProperty("codiceAttivazione")
    private String codiceAttivazione;

    @JsonProperty("cognome")
    private String cognome;

    @JsonProperty("contatto")
    private String contatto;

    @JsonProperty("datIns")
    private String datIns;

    @JsonProperty("datNas")
    private String datNas;

    @JsonProperty("datScadAccount")
    private String datScadAccount;

    @JsonProperty("datUpd")
    private String datUpd;

    @JsonProperty("datUpdPasswd")
    private Date tsAggiornamentoPass;

    @JsonProperty("dataUltimoLogin")
    private Date ultimoLogin;

    @JsonProperty("desComNas")
    private String desComNas;

    @JsonProperty("desComRcp")
    private String desComRcp;

    @JsonProperty("desComRes")
    private String desComRes;

    @JsonProperty("desIndRcp")
    private String desIndRcp;

    @JsonProperty("desIndRes")
    private String desIndRes;

    @JsonProperty("descrizione")
    private String descrizione;

    @JsonProperty("domanda")
    private String domanda;

    @JsonProperty("email")
    private String email;

    @JsonProperty("espCivRcp")
    private String espCivRcp;

    @JsonProperty("espCivRes")
    private String espCivRes;

    @JsonProperty("fax")
    private String fax;

    @JsonProperty("forzaCambioPasswd")
    private String fgCambioPassword;

    @JsonProperty("idApplicazioneIns")
    private BigDecimal idApplicazioneIns;

    @JsonProperty("idApplicazioneUpd")
    private BigDecimal idApplicazioneUpd;

    @JsonProperty("login")
    private String login;

    @JsonProperty("loginNumerica")
    private String loginNumerica;

    @JsonProperty("nazNas")
    private String nazNas;

    @JsonProperty("nazRcp")
    private String nazRcp;

    @JsonProperty("nazRes")
    private String nazRes;

    @JsonProperty("noScadAccount")
    private String fgScadenzaAccount;

    @JsonProperty("noScadPasswd")
    private String fgScadenzaPassword;

    @JsonProperty("nome")
    private String nome;

    @JsonProperty("numTentativiLogin")
    private Long nmTentativiLogin;

    @JsonProperty("numTentativiPin")
    private Long nmTentativiPin;

    @JsonProperty("parIva")
    private BigDecimal parIva;

    @JsonProperty("passwd")
    private String password;

    @JsonProperty("passwdNumerica")
    private String passwdNumerica;

    @JsonProperty("pressoRcp")
    private String pressoRcp;

    @JsonProperty("provNas")
    private String provNas;

    @JsonProperty("provRcp")
    private String provRcp;

    @JsonProperty("provRes")
    private String provRes;

    @JsonProperty("ragSoc")
    private String ragSoc;

    @JsonProperty("risposta")
    private String risposta;

    @JsonProperty("sesso")
    private String sesso;

    @JsonProperty("stato")
    private String cdStato;

    @JsonProperty("telefono")
    private String numeroTelefono;

    @JsonProperty("tipoUtente")
    private String tipoUtente;

    @JsonProperty("web")
    private String web;

    @JsonProperty("lstPmUtentiRuoliDto")
    private List<UtentePerProfiloDTO> utentePerProfiloList;

    @JsonProperty("pmEnteDto")
    private EnteDTO ente;

    @JsonIgnore
    private Long idEnte;





}