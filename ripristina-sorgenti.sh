#!/bin/bash
# Rimette i sorgenti applicativi che il repository non contiene.
#
# Il repository porta il LAVORO (documenti, generatori, sorgenti documentali); i sorgenti
# applicativi hanno un'origine ufficiale e si riprendono da lì: sono più aggiornati, e
# così chiavi private di produzione, password in chiaro e dati personali non lasciano il
# perimetro dell'ente. Vedi RICOSTRUIRE.md.
#
# ⚠️ I 129 moduli SIPO stanno sul GitLab interno: serve la VPN del Comune.
# ⚠️ Non copiare queste cartelle da una postazione all'altra con una chiavetta o con un
#    servizio di sincronizzazione: contengono PKCS#12 di produzione, le password dei
#    keystore in chiaro e codici fiscali reali. Ogni copia è una copia di quelli.
#
# Uso:  bash ripristina-sorgenti.sh            (tutto)
#       bash ripristina-sorgenti.sh ansc       (solo il repository ANSC, pubblico)
#       bash ripristina-sorgenti.sh sipo       (solo i 129 moduli, serve la VPN)
#
# L'elenco è stato estratto dai remoti reali dei cloni esistenti il 04/10/2026.

set -u
cd "$(dirname "$0")"
scelta="${1:-tutto}"
ok=0; ko=0

prendi() {   # prendi <destinazione> <url>
  if [ -d "$1/.git" ]; then printf '  = %s (già presente)\n' "$1"; return; fi
  if git clone --quiet "$2" "$1" 2>/dev/null; then printf '  + %s\n' "$1"; ok=$((ok+1))
  else printf '  ! %s — clone fallito\n' "$1"; ko=$((ko+1)); fi
}

if [ "$scelta" = tutto ] || [ "$scelta" = ansc ]; then
  echo "== ANSC (pubblico, nessuna VPN) =="
  prendi ansc https://github.com/italia/ansc.git
fi

if [ "$scelta" = tutto ] || [ "$scelta" = sipo ]; then
  echo "== SIPO: 129 moduli dal GitLab interno (serve la VPN) =="
  prendi back-end/agendasc-be               https://gitlab.ecaas.datacenter.comune.roma/sipo/back-end/agendasc-be.git
  prendi back-end/aire-be                   https://gitlab.ecaas.datacenter.comune.roma/sipo/back-end/aire-be.git
  prendi back-end/aire-elett-be             https://gitlab.ecaas.datacenter.comune.roma/sipo/back-end/aire-elett-be.git
  prendi back-end/albi-be                   https://gitlab.ecaas.datacenter.comune.roma/sipo/back-end/albi-be.git
  prendi back-end/all-anpr-sipo             https://gitlab.ecaas.datacenter.comune.roma/sipo/back-end/all-anpr-sipo.git
  prendi back-end/all-dec-be                https://gitlab.ecaas.datacenter.comune.roma/sipo/back-end/all-dec-be.git
  prendi back-end/all-matr-be               https://gitlab.ecaas.datacenter.comune.roma/sipo/back-end/all-matr-be.git
  prendi back-end/all-nas-be                https://gitlab.ecaas.datacenter.comune.roma/sipo/back-end/all-nas-be.git
  prendi back-end/anagrafe-be               https://gitlab.ecaas.datacenter.comune.roma/sipo/back-end/anagrafe-be.git
  prendi back-end/annotazioni-be            https://gitlab.ecaas.datacenter.comune.roma/sipo/back-end/annotazioni-be.git
  prendi back-end/cert-be                   https://gitlab.ecaas.datacenter.comune.roma/sipo/back-end/cert-be.git
  prendi back-end/cert-online-be            https://gitlab.ecaas.datacenter.comune.roma/sipo/back-end/cert-online-be.git
  prendi back-end/ci-be                     https://gitlab.ecaas.datacenter.comune.roma/sipo/back-end/ci-be.git
  prendi back-end/cittadinanza-be           https://gitlab.ecaas.datacenter.comune.roma/sipo/back-end/cittadinanza-be.git
  prendi back-end/clientpa                  https://gitlab.ecaas.datacenter.comune.roma/sipo/back-end/clientpa.git
  prendi back-end/commonsc-be               https://gitlab.ecaas.datacenter.comune.roma/sipo/back-end/commonsc-be.git
  prendi back-end/comunicazioni-be          https://gitlab.ecaas.datacenter.comune.roma/sipo/back-end/comunicazioni-be.git
  prendi back-end/conv-be                   https://gitlab.ecaas.datacenter.comune.roma/sipo/back-end/conv-be.git
  prendi back-end/cre-be                    https://gitlab.ecaas.datacenter.comune.roma/sipo/back-end/cre-be.git
  prendi back-end/cri-be                    https://gitlab.ecaas.datacenter.comune.roma/sipo/back-end/cri-be.git
  prendi back-end/cri-on-anpr-be            https://gitlab.ecaas.datacenter.comune.roma/sipo/back-end/cri-on-anpr-be.git
  prendi back-end/cri-on-be                 https://gitlab.ecaas.datacenter.comune.roma/sipo/back-end/cri-on-be.git
  prendi back-end/decessi-be                https://gitlab.ecaas.datacenter.comune.roma/sipo/back-end/decessi-be.git
  prendi back-end/din-be                    https://gitlab.ecaas.datacenter.comune.roma/sipo/back-end/din-be.git
  prendi back-end/divorzi-be                https://gitlab.ecaas.datacenter.comune.roma/sipo/back-end/divorzi-be.git
  prendi back-end/elett-common-be           https://gitlab.ecaas.datacenter.comune.roma/sipo/back-end/elett-common-be.git
  prendi back-end/elettorale-be             https://gitlab.ecaas.datacenter.comune.roma/sipo/back-end/elettorale-be.git
  prendi back-end/esponente-be              https://gitlab.ecaas.datacenter.comune.roma/sipo/back-end/esponente-be.git
  prendi back-end/evidenze-be               https://gitlab.ecaas.datacenter.comune.roma/sipo/back-end/evidenze-be.git
  prendi back-end/fasc-elett-be             https://gitlab.ecaas.datacenter.comune.roma/sipo/back-end/fasc-elett-be.git
  prendi back-end/faxpec-be                 https://gitlab.ecaas.datacenter.comune.roma/sipo/back-end/faxpec-be.git
  prendi back-end/gest-coec-be              https://gitlab.ecaas.datacenter.comune.roma/sipo/back-end/gest-coec-be.git
  prendi back-end/gest-evel-be              https://gitlab.ecaas.datacenter.comune.roma/sipo/back-end/gest-evel-be.git
  prendi back-end/gio-be                    https://gitlab.ecaas.datacenter.comune.roma/sipo/back-end/gio-be.git
  prendi back-end/int-be                    https://gitlab.ecaas.datacenter.comune.roma/sipo/back-end/int-be.git
  prendi back-end/irrep-be                  https://gitlab.ecaas.datacenter.comune.roma/sipo/back-end/irrep-be.git
  prendi back-end/matrim-be                 https://gitlab.ecaas.datacenter.comune.roma/sipo/back-end/matrim-be.git
  prendi back-end/nascita-be                https://gitlab.ecaas.datacenter.comune.roma/sipo/back-end/nascita-be.git
  prendi back-end/not-anpr                  https://gitlab.ecaas.datacenter.comune.roma/sipo/back-end/not-anpr.git
  prendi back-end/pago-cie-be               https://gitlab.ecaas.datacenter.comune.roma/sipo/back-end/pago-cie-be.git
  prendi back-end/prog-be                   https://gitlab.ecaas.datacenter.comune.roma/sipo/back-end/prog-be.git
  prendi back-end/rich_online-be            https://gitlab.ecaas.datacenter.comune.roma/sipo/back-end/rich_online-be.git
  prendi back-end/rich-temp-be              https://gitlab.ecaas.datacenter.comune.roma/sipo/back-end/rich-temp-be.git
  prendi back-end/sad-be                    https://gitlab.ecaas.datacenter.comune.roma/sipo/back-end/sad-be.git
  prendi back-end/statistica-be             https://gitlab.ecaas.datacenter.comune.roma/sipo/back-end/statistica-be.git
  prendi back-end/statocivile-be            https://gitlab.ecaas.datacenter.comune.roma/sipo/back-end/statocivile-be.git
  prendi back-end/territorio-be             https://gitlab.ecaas.datacenter.comune.roma/sipo/back-end/territorio-be.git
  prendi back-end/tessele-be                https://gitlab.ecaas.datacenter.comune.roma/sipo/back-end/tessele-be.git
  prendi back-end/ufficio-canc-be           https://gitlab.ecaas.datacenter.comune.roma/sipo/back-end/ufficio-canc-be.git
  prendi back-end/unidoc                    https://gitlab.ecaas.datacenter.comune.roma/sipo/back-end/unidoc.git
  prendi back-end/unioni-be                 https://gitlab.ecaas.datacenter.comune.roma/sipo/back-end/unioni-be.git
  prendi back-end/varana-be                 https://gitlab.ecaas.datacenter.comune.roma/sipo/back-end/varana-be.git
  prendi back-end/verifica-ele              https://gitlab.ecaas.datacenter.comune.roma/sipo/back-end/verifica-ele.git
  prendi common/aggior-sipo                 https://gitlab.ecaas.datacenter.comune.roma/sipo/common/aggior-sipo.git
  prendi common/anagrafe-entities           https://gitlab.ecaas.datacenter.comune.roma/sipo/common/anagrafe-entities.git
  prendi common/anagrafe-producer           https://gitlab.ecaas.datacenter.comune.roma/sipo/common/anagrafe-producer.git
  prendi common/anpr-client                 https://gitlab.ecaas.datacenter.comune.roma/sipo/common/anpr-client.git
  prendi common/client-sir                  https://gitlab.ecaas.datacenter.comune.roma/sipo/common/client-sir.git
  prendi common/client-sito                 https://gitlab.ecaas.datacenter.comune.roma/sipo/common/client-sito.git
  prendi common/commo-web                   https://gitlab.ecaas.datacenter.comune.roma/sipo/common/commo-web.git
  prendi common/common-fe-be-sc             https://gitlab.ecaas.datacenter.comune.roma/sipo/common/common-fe-be-sc.git
  prendi common/commonsc-entities           https://gitlab.ecaas.datacenter.comune.roma/sipo/common/commonsc-entities.git
  prendi common/decessi-entities            https://gitlab.ecaas.datacenter.comune.roma/sipo/common/decessi-entities.git
  prendi common/divorzi-entities            https://gitlab.ecaas.datacenter.comune.roma/sipo/common/divorzi-entities.git
  prendi common/elett-entities              https://gitlab.ecaas.datacenter.comune.roma/sipo/common/elett-entities.git
  prendi common/email-sender                https://gitlab.ecaas.datacenter.comune.roma/sipo/common/email-sender.git
  prendi common/ext-jar-sc                  https://gitlab.ecaas.datacenter.comune.roma/sipo/common/ext-jar-sc.git
  prendi common/ext-jar                     https://gitlab.ecaas.datacenter.comune.roma/sipo/common/ext-jar.git
  prendi common/matrim-entities             https://gitlab.ecaas.datacenter.comune.roma/sipo/common/matrim-entities.git
  prendi common/pdf-gen-elett               https://gitlab.ecaas.datacenter.comune.roma/sipo/common/pdf-gen-elett.git
  prendi common/pdf-gen-sc                  https://gitlab.ecaas.datacenter.comune.roma/sipo/common/pdf-gen-sc.git
  prendi common/pdf-generator               https://gitlab.ecaas.datacenter.comune.roma/sipo/common/pdf-generator.git
  prendi common/profilazione-utente         https://gitlab.ecaas.datacenter.comune.roma/sipo/common/profilazione-utente.git
  prendi common/protocollo-ged              https://gitlab.ecaas.datacenter.comune.roma/sipo/common/protocollo-ged.git
  prendi common/rest-client                 https://gitlab.ecaas.datacenter.comune.roma/sipo/common/rest-client.git
  prendi common/rest-security               https://gitlab.ecaas.datacenter.comune.roma/sipo/common/rest-security.git
  prendi common/siel                        https://gitlab.ecaas.datacenter.comune.roma/sipo/common/siel.git
  prendi common/statistica-entities         https://gitlab.ecaas.datacenter.comune.roma/sipo/common/statistica-entities.git
  prendi common/unioni-entities             https://gitlab.ecaas.datacenter.comune.roma/sipo/common/unioni-entities.git
  prendi cross/anpr-elett-subentro          https://gitlab.ecaas.datacenter.comune.roma/sipo/cross/anpr-elett-subentro.git
  prendi cross/anpr-generate-xml            https://gitlab.ecaas.datacenter.comune.roma/sipo/cross/anpr-generate-xml.git
  prendi cross/anprvalidator                https://gitlab.ecaas.datacenter.comune.roma/sipo/cross/anprvalidator.git
  prendi cross/buoni-spesa                  https://gitlab.ecaas.datacenter.comune.roma/sipo/cross/buoni-spesa.git
  prendi cross/cert-online-dotnet           https://gitlab.ecaas.datacenter.comune.roma/sipo/cross/cert-online-dotnet.git
  prendi cross/cross-reing                  https://gitlab.ecaas.datacenter.comune.roma/sipo/cross/cross-reing.git
  prendi cross/firma-id-postazione          https://gitlab.ecaas.datacenter.comune.roma/sipo/cross/firma-id-postazione.git
  prendi cross/html-evento_elettorale       https://gitlab.ecaas.datacenter.comune.roma/sipo/cross/html-evento_elettorale.git
  prendi cross/Signps                       https://gitlab.ecaas.datacenter.comune.roma/sipo/cross/Signps.git
  prendi cross/sipo-test-be                 https://gitlab.ecaas.datacenter.comune.roma/sipo/cross/sipo-test-be.git
  prendi cross/verifica-servizi             https://gitlab.ecaas.datacenter.comune.roma/sipo/cross/verifica-servizi.git
  prendi front-end/agendasc-web             https://gitlab.ecaas.datacenter.comune.roma/sipo/front-end/agendasc-web.git
  prendi front-end/aire-elett-web           https://gitlab.ecaas.datacenter.comune.roma/sipo/front-end/aire-elett-web.git
  prendi front-end/aire-web                 https://gitlab.ecaas.datacenter.comune.roma/sipo/front-end/aire-web.git
  prendi front-end/albi-web                 https://gitlab.ecaas.datacenter.comune.roma/sipo/front-end/albi-web.git
  prendi front-end/anagrafe-web             https://gitlab.ecaas.datacenter.comune.roma/sipo/front-end/anagrafe-web.git
  prendi front-end/annotazioni-web          https://gitlab.ecaas.datacenter.comune.roma/sipo/front-end/annotazioni-web.git
  prendi front-end/cert-web                 https://gitlab.ecaas.datacenter.comune.roma/sipo/front-end/cert-web.git
  prendi front-end/ci-web                   https://gitlab.ecaas.datacenter.comune.roma/sipo/front-end/ci-web.git
  prendi front-end/cittadinanza-web         https://gitlab.ecaas.datacenter.comune.roma/sipo/front-end/cittadinanza-web.git
  prendi front-end/commonsc-web             https://gitlab.ecaas.datacenter.comune.roma/sipo/front-end/commonsc-web.git
  prendi front-end/conv-web                 https://gitlab.ecaas.datacenter.comune.roma/sipo/front-end/conv-web.git
  prendi front-end/cr-bo-web                https://gitlab.ecaas.datacenter.comune.roma/sipo/front-end/cr-bo-web.git
  prendi front-end/cr-fo-web                https://gitlab.ecaas.datacenter.comune.roma/sipo/front-end/cr-fo-web.git
  prendi front-end/decessi-web              https://gitlab.ecaas.datacenter.comune.roma/sipo/front-end/decessi-web.git
  prendi front-end/din-web                  https://gitlab.ecaas.datacenter.comune.roma/sipo/front-end/din-web.git
  prendi front-end/divorzi-web              https://gitlab.ecaas.datacenter.comune.roma/sipo/front-end/divorzi-web.git
  prendi front-end/elettorale-web           https://gitlab.ecaas.datacenter.comune.roma/sipo/front-end/elettorale-web.git
  prendi front-end/esponente-web            https://gitlab.ecaas.datacenter.comune.roma/sipo/front-end/esponente-web.git
  prendi front-end/evidenze-web             https://gitlab.ecaas.datacenter.comune.roma/sipo/front-end/evidenze-web.git
  prendi front-end/fasc-elett-web           https://gitlab.ecaas.datacenter.comune.roma/sipo/front-end/fasc-elett-web.git
  prendi front-end/gest-coec-web            https://gitlab.ecaas.datacenter.comune.roma/sipo/front-end/gest-coec-web.git
  prendi front-end/gest-evel-web            https://gitlab.ecaas.datacenter.comune.roma/sipo/front-end/gest-evel-web.git
  prendi front-end/gio-web                  https://gitlab.ecaas.datacenter.comune.roma/sipo/front-end/gio-web.git
  prendi front-end/irrep-web                https://gitlab.ecaas.datacenter.comune.roma/sipo/front-end/irrep-web.git
  prendi front-end/matrim-web               https://gitlab.ecaas.datacenter.comune.roma/sipo/front-end/matrim-web.git
  prendi front-end/nascita-web              https://gitlab.ecaas.datacenter.comune.roma/sipo/front-end/nascita-web.git
  prendi front-end/pago-cie-web             https://gitlab.ecaas.datacenter.comune.roma/sipo/front-end/pago-cie-web.git
  prendi front-end/rich_online-web          https://gitlab.ecaas.datacenter.comune.roma/sipo/front-end/rich_online-web.git
  prendi front-end/statistica-web           https://gitlab.ecaas.datacenter.comune.roma/sipo/front-end/statistica-web.git
  prendi front-end/statocivile-web          https://gitlab.ecaas.datacenter.comune.roma/sipo/front-end/statocivile-web.git
  prendi front-end/territorio-web           https://gitlab.ecaas.datacenter.comune.roma/sipo/front-end/territorio-web.git
  prendi front-end/tessele-web              https://gitlab.ecaas.datacenter.comune.roma/sipo/front-end/tessele-web.git
  prendi front-end/ufficio-canc-web         https://gitlab.ecaas.datacenter.comune.roma/sipo/front-end/ufficio-canc-web.git
  prendi front-end/unioni-web               https://gitlab.ecaas.datacenter.comune.roma/sipo/front-end/unioni-web.git
  prendi front-end/varana-web               https://gitlab.ecaas.datacenter.comune.roma/sipo/front-end/varana-web.git
  prendi sipo-root/rich-temp-web            https://gitlab.ecaas.datacenter.comune.roma/sipo/rich-temp-web.git
  prendi sipo-root/sql                      https://gitlab.ecaas.datacenter.comune.roma/sipo/sql.git
  prendi sipo-root/superset                 https://gitlab.ecaas.datacenter.comune.roma/sipo/superset.git
  prendi sipo-root/unioni-entities          https://gitlab.ecaas.datacenter.comune.roma/sipo/unioni-entities.git
fi

echo
echo "clonati: $ok   falliti: $ko"
if [ "$ko" -gt 0 ]; then
  echo "⚠️ Se tutti i cloni SIPO sono falliti, con ogni probabilità manca la VPN."
fi
cat <<'NOTA'

Non si clona, e va ripreso a parte:
  · anpr-9.2.9/   la documentazione ANPR, dal pacchetto Sogei già in uso
  · Documenti finali/Archivio analisi 2-3.20.zip   archivio delle versioni superate,
    escluso perché pesava un terzo del repository. Resta sulla postazione d'origine.
NOTA
