package it.romaCapitale.sipo.verificaHeaderIam;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Enumeration;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpSession;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;

import it.romaCapitale.profilazioneUtente.dao.ConfRuoloVO;
import it.romaCapitale.profilazioneUtente.model.User;

/**
 * Pagina di diagnosi: stampa le variabili di header che l'Access Manager di IAM
 * inietta nella richiesta, e le confronta con quello che SIPO ha in sessione.
 *
 * Serve a rispondere a tre domande che le sole specifiche non chiudono:
 *   1. iv-codfis arriva anche per i dipendenti? (il manuale IAM lo dichiara
 *      "garantito", ma le variabili disponibili dipendono dalla policy
 *      configurata per ciascuna applicazione);
 *   2. iv-portal-groups arriva a SIPO? Con quali nomi di gruppo?
 *   3. nome, cognome e codice fiscale dell'header coincidono con quelli che
 *      ProfilazioneUtente legge da UTENTI?
 *
 * Il manuale IAM suggerisce lui stesso di prevedere una pagina come questa in
 * fase di sviluppo (par. 3.2).
 *
 * ⚠️ NON va lasciata attiva in produzione. È spenta per difetto: si accende con
 *    verifica.header.iam.abilitata=true
 * e va rimossa, o rispenta, appena fatta la verifica. Ogni apertura viene
 * registrata nel log applicativo con l'utente che l'ha chiesta.
 *
 * ⚠️ I valori personali sono mascherati per difetto. Con ?completo=1 si vedono
 *    in chiaro: da usare solo se serve davvero e su un ambiente di collaudo.
 */
@Controller
@ConditionalOnProperty(name = "verifica.header.iam.abilitata", havingValue = "true")
public class VerificaHeaderIamController {

	private static final Logger logger = LoggerFactory.getLogger(VerificaHeaderIamController.class);

	/** Le variabili su cui si gioca il disegno: si evidenziano in pagina. */
	private static final List<String> ATTESE = java.util.Arrays.asList(
			"iv-user", "iv-codfis", "iv-nome", "iv-cognome", "iv-fullname",
			"iv-portal-groups", "sysgroup", "iv-tipoutente",
			"x-real-ip", "x-client-sn-sipo");

	/** Header che non vanno mai stampati: trasportano credenziali o sessione. */
	private static final List<String> MAI = java.util.Arrays.asList(
			"authorization", "cookie", "proxy-authorization", "set-cookie");

	@GetMapping("/verificaHeaderIam")
	public String pagina(HttpServletRequest request, HttpSession sessione, Model model,
			@RequestParam(name = "completo", required = false, defaultValue = "0") String completo) {

		boolean inChiaro = "1".equals(completo);
		User utente = (User) sessione.getAttribute("LOGIN_USER");

		logger.warn("verificaHeaderIam aperta da {} (in chiaro: {})",
				utente != null ? utente.getUsername() : "sessione senza LOGIN_USER", inChiaro);

		model.addAttribute("tutti", raccogliHeader(request, inChiaro));
		model.addAttribute("attese", raccogliAttese(request, inChiaro));
		model.addAttribute("gruppi", gruppiLdap(request.getHeader("iv-portal-groups")));
		model.addAttribute("grezzoGruppi", request.getHeader("iv-portal-groups"));
		model.addAttribute("confronto", confronto(request, utente, inChiaro));
		model.addAttribute("sessione", datiSessione(utente, inChiaro));
		model.addAttribute("inChiaro", inChiaro);
		return "verificaHeaderIam";
	}

	/** La stessa cosa in testo semplice: comoda da incollare in una segnalazione. */
	@GetMapping(value = "/verificaHeaderIam.txt", produces = "text/plain;charset=UTF-8")
	@ResponseBody
	public String testo(HttpServletRequest request, HttpSession sessione,
			@RequestParam(name = "completo", required = false, defaultValue = "0") String completo) {

		boolean inChiaro = "1".equals(completo);
		User utente = (User) sessione.getAttribute("LOGIN_USER");
		logger.warn("verificaHeaderIam.txt aperta da {}",
				utente != null ? utente.getUsername() : "sessione senza LOGIN_USER");

		StringBuilder sb = new StringBuilder();
		sb.append("VARIABILI ATTESE\n");
		for (Map.Entry<String, String> e : raccogliAttese(request, inChiaro).entrySet()) {
			sb.append(String.format("  %-22s %s%n", e.getKey(), e.getValue()));
		}
		sb.append("\nGRUPPI LDAP (da iv-portal-groups)\n");
		List<String> gruppi = gruppiLdap(request.getHeader("iv-portal-groups"));
		if (gruppi.isEmpty()) {
			sb.append("  (nessuno: la variabile non arriva oppure è vuota)\n");
		} else {
			for (String g : gruppi) {
				sb.append("  ").append(g).append('\n');
			}
		}
		sb.append("\nCONFRONTO HEADER / SESSIONE\n");
		for (Map.Entry<String, String> e : confronto(request, utente, inChiaro).entrySet()) {
			sb.append(String.format("  %-22s %s%n", e.getKey(), e.getValue()));
		}
		sb.append("\nTUTTI GLI HEADER\n");
		for (Map.Entry<String, String> e : raccogliHeader(request, inChiaro).entrySet()) {
			sb.append(String.format("  %-28s %s%n", e.getKey(), e.getValue()));
		}
		return sb.toString();
	}

	// ------------------------------------------------------------------ raccolta

	private Map<String, String> raccogliHeader(HttpServletRequest request, boolean inChiaro) {
		Map<String, String> out = new LinkedHashMap<>();
		Enumeration<String> nomi = request.getHeaderNames();
		List<String> ordinati = new ArrayList<>();
		while (nomi != null && nomi.hasMoreElements()) {
			ordinati.add(nomi.nextElement());
		}
		Collections.sort(ordinati, String.CASE_INSENSITIVE_ORDER);
		for (String nome : ordinati) {
			if (MAI.contains(nome.toLowerCase())) {
				out.put(nome, "(omesso di proposito)");
			} else {
				out.put(nome, valore(nome, request.getHeader(nome), inChiaro));
			}
		}
		return out;
	}

	private Map<String, String> raccogliAttese(HttpServletRequest request, boolean inChiaro) {
		Map<String, String> out = new LinkedHashMap<>();
		for (String nome : ATTESE) {
			String v = request.getHeader(nome);
			out.put(nome, v == null ? "ASSENTE"
					: (v.trim().isEmpty() ? "PRESENTE MA VUOTO" : valore(nome, v, inChiaro)));
		}
		return out;
	}

	/**
	 * Spezza iv-portal-groups e restituisce i soli nomi di gruppo (il cn=).
	 *
	 * ⚠️ Il formato dichiarato dal manuale IAM è
	 *   cn=gruppo1\,ou=Groups\,dc=cdr\,dc=it,cn=gruppo2\,ou=Groups\,dc=cdr\,dc=it
	 * cioè i gruppi sono separati da VIRGOLA e le componenti del path LDAP dalla
	 * sequenza BACKSLASH-VIRGOLA. Uno split(",") ingenuo spezza ogni gruppo in
	 * quattro pezzi: la virgola da usare è quella NON preceduta da backslash.
	 */
	static List<String> gruppiLdap(String grezzo) {
		List<String> out = new ArrayList<>();
		if (grezzo == null || grezzo.trim().isEmpty()) {
			return out;
		}
		for (String dn : grezzo.split("(?<!\\\\),")) {
			String pulito = dn.replace("\\,", ",").trim();
			if (pulito.isEmpty()) {
				continue;
			}
			String nome = pulito;
			for (String pezzo : pulito.split(",")) {
				String p = pezzo.trim();
				if (p.toLowerCase().startsWith("cn=")) {
					nome = p.substring(3).trim();
					break;
				}
			}
			out.add(nome + "        [" + pulito + "]");
		}
		return out;
	}

	private Map<String, String> confronto(HttpServletRequest request, User utente, boolean inChiaro) {
		Map<String, String> out = new LinkedHashMap<>();
		out.put("codice fiscale", riga(request.getHeader("iv-codfis"),
				utente == null ? null : utente.getCf(), inChiaro));
		out.put("nome", riga(request.getHeader("iv-nome"),
				utente == null ? null : utente.getNome(), inChiaro));
		out.put("cognome", riga(request.getHeader("iv-cognome"),
				utente == null ? null : utente.getCognome(), inChiaro));
		out.put("username", riga(request.getHeader("iv-user"),
				utente == null ? null : utente.getUsername(), inChiaro));
		return out;
	}

	private String riga(String daHeader, String daSessione, boolean inChiaro) {
		String h = daHeader == null ? "ASSENTE" : daHeader.trim();
		String s = daSessione == null ? "ASSENTE" : daSessione.trim();
		String esito;
		if ("ASSENTE".equals(h) && "ASSENTE".equals(s)) {
			esito = "nessuno dei due";
		} else if ("ASSENTE".equals(h)) {
			esito = "solo in sessione (viene dal database)";
		} else if ("ASSENTE".equals(s)) {
			esito = "solo nell'header";
		} else if (h.equalsIgnoreCase(s)) {
			esito = "COINCIDONO";
		} else {
			esito = "DIVERGONO";
		}
		return String.format("header=%s | sessione=%s -> %s",
				maschera(h, inChiaro), maschera(s, inChiaro), esito);
	}

	private Map<String, String> datiSessione(User utente, boolean inChiaro) {
		Map<String, String> out = new LinkedHashMap<>();
		if (utente == null) {
			out.put("LOGIN_USER", "assente: pagina aperta senza passare dalla login");
			return out;
		}
		out.put("username", String.valueOf(utente.getUsername()));
		out.put("codice fiscale", maschera(utente.getCf(), inChiaro));
		out.put("nome e cognome", maschera(utente.getNome(), inChiaro) + " "
				+ maschera(utente.getCognome(), inChiaro));
		out.put("groupId", String.valueOf(utente.getGroupId()));
		out.put("idOrganizzazione", String.valueOf(utente.getIdOrganizzazione()));
		out.put("ip postazione (x-real-ip)", String.valueOf(utente.getIpPostazione()));
		out.put("serial certificato (x-client-sn-sipo)", String.valueOf(utente.getHostname()));

		StringBuilder ruoli = new StringBuilder();
		if (utente.getRuoli() != null) {
			int i = 0;
			for (ConfRuoloVO r : utente.getRuoli()) {
				ruoli.append(i == 0 ? "[primo, è quello che il FE usa] " : " | ")
						.append(r.getId()).append(' ')
						.append(r.getRuolo()).append(" / profiloBe=").append(r.getRuoloBe())
						.append(" (").append(r.getDescrizione()).append(')');
				i++;
			}
		}
		out.put("ruoli", ruoli.length() == 0 ? "nessuno" : ruoli.toString());
		out.put("aree tematiche", utente.getAreeTematiche() == null ? "nessuna"
				: String.valueOf(utente.getAreeTematiche().size()));
		return out;
	}

	// ------------------------------------------------------------------ mascheratura

	private String valore(String nome, String v, boolean inChiaro) {
		if (v == null) {
			return "ASSENTE";
		}
		String n = nome.toLowerCase();
		boolean personale = n.contains("codfis") || n.contains("nome") || n.contains("cognome")
				|| n.contains("nascita") || n.contains("res-") || n.contains("dom-")
				|| n.contains("email") || n.contains("tel") || n.contains("fullname")
				|| n.equals("iv-user");
		return personale ? maschera(v, inChiaro) : v;
	}

	/** Prime e ultime due lettere: basta a dire "c'è e ha la forma giusta". */
	private String maschera(String v, boolean inChiaro) {
		if (v == null || v.trim().isEmpty()) {
			return "ASSENTE";
		}
		if (inChiaro) {
			return v;
		}
		String s = v.trim();
		if (s.length() <= 4) {
			return "***(" + s.length() + " caratteri)";
		}
		return s.substring(0, 2) + "***" + s.substring(s.length() - 2)
				+ "(" + s.length() + " caratteri)";
	}
}
