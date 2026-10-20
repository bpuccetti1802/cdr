package it.sistinf.romacapitale.auth.domain;

import java.util.Arrays;
public enum ApplicazioniIAMEnum {
    GET_FO("GET-FO", true),
    GET_BO("GET-BO", false),
    GECOS_FO("GECOS-FO", true),
    GECOS_BO("GECOS", false),
    GESCAN("GESCAN", false),
    TRIBUTI_FO("GERICO", true),
    TRIBUTI_BO("BO_TRIBUTI", false);

    private final String codApplicazione;
    private final boolean loginAnonimoConsentito;

    ApplicazioniIAMEnum(String codApplicazione, boolean loginAnonimoConsentito) {
        this.codApplicazione = codApplicazione;
        this.loginAnonimoConsentito = loginAnonimoConsentito;
    }

    public String getCodApplicazione() {
        return this.codApplicazione;
    }

    public boolean isLoginAnonimoConsentito() {
        return this.loginAnonimoConsentito;
    }

    public static ApplicazioniIAMEnum fromCodApplicazione(String nome) {
        return Arrays.stream(values())
                .filter(a -> a.codApplicazione.equalsIgnoreCase(nome))
                .findFirst()
                .orElseThrow(() -> new IllegalArgumentException("Applicazione non trovata: " + nome));
    }

}
