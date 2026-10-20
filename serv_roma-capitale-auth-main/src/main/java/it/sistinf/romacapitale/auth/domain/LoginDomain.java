package it.sistinf.romacapitale.auth.domain;

import com.fasterxml.jackson.databind.ObjectMapper;
import it.sistinf.romacapitale.auth.dto.TokenRequestDTO;
import it.sistinf.romacapitale.integration.auth.vo.TokenResponseDTO;
import it.sistinf.romacapitale.auth.utils.TokenBuilder;
import it.sistinf.romacapitale.core.domain.AbstractDomain;
import it.sistinf.romacapitale.core.dto.RequestDTO;
import it.sistinf.romacapitale.core.dto.ResponseDTO;
import it.sistinf.romacapitale.core.exceptions.ApplicationException;
import it.sistinf.romacapitale.core.exceptions.ApplicationExceptionBuilder;
import it.sistinf.romacapitale.core.security.CurrentUser;
import it.sistinf.romacapitale.core.security.JwtManager;
import it.sistinf.romacapitale.core.utils.AESEncryptionUtils;
import it.sistinf.romacapitale.core.utils.ControlloCampi;
import it.sistinf.romacapitale.core.utils.DateUtils;
import it.sistinf.romacapitale.core.vo.auth.LoginVO;
import it.sistinf.romacapitale.integration.auth.vo.EnumTipoUtenteTecnico;
import it.sistinf.romacapitale.integration.auth.vo.UtenteTecnicoVO;
import it.sistinf.romacapitale.integration.management.api.ApplicazioneClient;
import it.sistinf.romacapitale.integration.management.api.UtenteClient;
import it.sistinf.romacapitale.integration.management.vo.*;
import it.sistinf.romacapitale.integration.management.vo.requestVO.SelezionaStrutturaRequestVO;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.security.oauth2.core.OAuth2AuthenticationException;
import org.springframework.security.oauth2.core.OAuth2Error;
import org.springframework.stereotype.Service;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.util.StringUtils;
import org.springframework.web.client.RestTemplate;

import java.util.*;


/**
 * Classe LoginDomain
 */
@Service
@RequiredArgsConstructor
@Slf4j
public class LoginDomain extends AbstractDomain {

    private final JwtManager jwtManager;

    private final UtenteClient utenteClient;
    private final ApplicazioneClient applicazioneClient;
  //private AuditClient auditClient;

    private final TokenBuilder tokenBuilder;
    private final RestTemplate restTemplate;

    @Value("${crittografiaPassword}")
    private String crittografiaPassword;

    @Value("${crittografiaSalt}")
    private String crittografiaSalt;

    @Value("${jwt.expirationTimeMinutes}")
    private String jwtExpirationTimeMinutes;

    @Value("${jwt.max.lenght}")
    private int jwtMaxLenght;

    private UUID generateUUID() {
        return UUID.randomUUID();
    }

    public ProfileUserVO localLogin(LoginVO loginVO, boolean checkPassword, boolean redirect) {
        // Autenticazione
        UtenteVO utenteVO = new UtenteVO();
        ResponseDTO<ProfileUserVO> response;
        //cerca l'utente su management
        response = getUtenteFromManagement(loginVO);

        // Set profilo in cache
        ProfileUserVO profileUser = response.getPayload();
        profileUser.setSessionId(generateUUID() + "");
        //writeCache("profile_session_id_" + profileUser.getSessionId(), profileUser);
         profileUser.setCdAmbito(loginVO.getCdAmbito());
        profileUser.setCdApplicazione(loginVO.getCdApplicazione());
        generateTokenAndSetProfile(profileUser);

//        trackauditLogin(profileUser);
        return response.getPayload();
    }

    private ProfileUserVO generateTokenAndSetProfile(ProfileUserVO profileUser) {
        // Generazione token JWT
        profileUser.setFlagTokenReduced("N");
        String token = tokenBuilder.prepareToken(profileUser, false);
        //Se il token jwt è più grande della property jwtMaxLenght
        if (token.length() >= jwtMaxLenght) {
            profileUser.setFlagTokenReduced("S");
            writeCache("token_session_id_" + profileUser.getSessionId(), token);
            String tokenReduced = tokenBuilder.prepareToken(profileUser, true);
            profileUser.setToken(tokenReduced);
        }else{
            profileUser.setToken(token);
        }
        return profileUser;
    }

    private ResponseDTO<ProfileUserVO> getUtenteFromManagement(LoginVO loginVO) {

        //Get utente e abilitazioni da Management
        ResponseDTO<ProfileUserVO> profileUserResp = utenteClient.getUtenteAndAbilitazioniByUsername(makeRequestDTO(loginVO));
        if (profileUserResp.getPayload() != null) {
            UtenteVO utente = profileUserResp.getPayload().getUtente();

            //Check password
            if (utente.getPassword() != null) {
                String passDecrypted = AESEncryptionUtils.decrypt(utente.getPassword(), crittografiaPassword, crittografiaSalt);
                if (!passDecrypted.equals(loginVO.getPassword())) {
                    throw new ApplicationException("Errore di Autenticazione: Password errata");
                }
            } else {
                throw new ApplicationException("Errore di Autenticazione: Password non impostata per l'utente " + utente.getUsername());

            }

            ResponseDTO<UtenteVO> utenteResp = controlliUtenteAttivo(utente);

            profileUserResp.getPayload().setUtente(utenteResp.getPayload());

        }

        return profileUserResp;
    }

    private ResponseDTO<UtenteVO> controlliUtenteAttivo(UtenteVO utente) {
            //Controllo se l'utente è attivo
            if ('S' != utente.getFlagUtenteAttivo()) {
                throw new ApplicationException("Utente non attivo, contattare l’amministratore");
            }
            //Check ultimo login
            Date currentDate = DateUtils.today();
            if (utente.getUltimoLogin() != null) {
                //ultimo login + 6 mesi deve essere < data corrente
                Date dataScadenza = DateUtils.add(utente.getUltimoLogin(), Calendar.MONTH, 6);
                if (dataScadenza.before(currentDate)) {
                    utente.setFlagUtenteAttivo('N');
                    utenteClient.updateUtenteForLogin(makeRequestDTO(utente));
                    throw new ApplicationException("Utente non attivo, contattare l’amministratore");
                }
            }

            //Aggiorno il campo dt ultimo login con data corrente
            utente.setUltimoLogin(currentDate);
            ResponseDTO<UtenteVO> utenteResp = utenteClient.updateUtenteForLogin(makeRequestDTO(utente));
        return utenteResp;
    }

    public UtenteTecnicoVO loginUtenteTecnico(String tipoUtenteTecnico, String cdAmbito, String cdApplicazione) {

        UtenteTecnicoVO utenteTecnicoVO = new UtenteTecnicoVO();

        //Get utente e abilitazioni da Management
        LoginVO loginVO = new LoginVO();
        loginVO.setCdAmbito(cdAmbito);
        loginVO.setCdApplicazione(cdApplicazione);
        loginVO.setUsername(EnumTipoUtenteTecnico.getUsernameByTipo(tipoUtenteTecnico));

        ResponseDTO<ProfileUserVO> profileUserResp = utenteClient.getUtenteAndAbilitazioniByUsername(makeRequestDTO(loginVO));
        if (profileUserResp.getPayload() != null) {
            UtenteVO utente = profileUserResp.getPayload().getUtente();

            ResponseDTO<UtenteVO> utenteResp = controlliUtenteAttivo(utente);

            profileUserResp.getPayload().setUtente(utenteResp.getPayload());

            // Set profilo in cache
            ProfileUserVO profileUser = profileUserResp.getPayload();
            profileUser.setSessionId(generateUUID() + "");
            //writeCache("profile_session_id_" + profileUser.getSessionId(), profileUser);
            profileUser.setCdAmbito(cdAmbito);
            profileUser.setCdApplicazione(cdApplicazione);
            generateTokenAndSetProfile(profileUser);

            //trackauditLogin(profileUser);

            utenteTecnicoVO.setUsername(utente.getUsername());
            utenteTecnicoVO.setAbilitazioni(profileUser.getAbilitazioni());
            utenteTecnicoVO.setSessionId(profileUser.getSessionId());
            utenteTecnicoVO.setToken(profileUser.getToken());

        }

        return utenteTecnicoVO;
    }


    /////LOGIN MOCK

    public ProfileUserVO localLoginSist(String userName, String password, boolean checkPassword, boolean redirect) {
        UtenteVO utenteVO = new UtenteVO();
        utenteVO.setUsername(userName);
        utenteVO.setPassword(password);
        RequestDTO<UtenteVO> req = makeRequestDTO(utenteVO);

        ProfileUserVO profilo = mockUtente(req).getPayload();
        UtenteVO user = profilo.getUtente();

        profilo.setSessionId(generateUUID() + "");
        //CacheUtils.writeCache("profile_session_id_" + userVO.getSessionId(), userVO, cacheHost, cachePort, cachePwd, cacheTimeout, cacheSentinelSN, cacheSentinelPort);

        // Generazione token JWT
        String token = prepareTokenMock(user);
        profilo.setToken(token);

        //CacheUtils.writeCache("token_session_id_" + cu.getSessionId(), token, cacheHost, cachePort, cachePwd, cacheTimeout, cacheSentinelSN, cacheSentinelPort);
//        trackauditLogin();
        return profilo;
    }

    public TokenResponseDTO loginSist(TokenRequestDTO request) {

        // Validazione request
        if (request.getGrantType().isEmpty() || request.getClientId().isEmpty() || request.getClientSecret().isEmpty() || request.getScope().isEmpty()) {
            throw new OAuth2AuthenticationException(new OAuth2Error("invalid_request","Errore: Request non valida '" + request + "'", null));
        }

        // Validazione grant type
        if (!"client_credentials".equals(request.getGrantType())) {
            throw new OAuth2AuthenticationException(new OAuth2Error("unsupported_grant_type","Errore: grant type '" + request.getGrantType() + "' non supportato", null));
        }

        // Validazione scope
        if (!"access".equals(request.getScope())) {
            throw new OAuth2AuthenticationException(new OAuth2Error("invalid_scope","Errore: scope '" + request.getScope() + "'.", null));
        }

        //Get utente e abilitazioni da Management
        LoginVO loginVO = new LoginVO();
        loginVO.setUsername(request.getClientId());
        loginVO.setPassword(request.getClientSecret());

        //cdAmbito e cdApplicazione //TODO: Rimuovere UPPERCASE per username "batch", le utenze applicative dovranno corrispondere al cdApplicazione della tabella APPLICAZIONE !
        ApplicazioneVO applicazioneVO = applicazioneClient.getApplicazioneFromCdApplicazione(request.getClientId().toUpperCase()).getPayload();
        loginVO.setCdApplicazione(applicazioneVO.getKey().getCdApplicazione());
        loginVO.setCdAmbito(applicazioneVO.getKey().getCdAmbito());

        ResponseDTO<ProfileUserVO> profileUserVOResponseDTO = null;
        try {
            profileUserVOResponseDTO = utenteClient.getUtenteAndAbilitazioniByUsername(makeRequestDTO(loginVO));
        } catch (Exception e) {
            e.getMessage();
        }

        UtenteVO utenteVO = profileUserVOResponseDTO.getPayload().getUtente();
        //Check password
        if (utenteVO.getPassword() != null) {
            String passDecrypted = AESEncryptionUtils.decrypt(utenteVO.getPassword(), crittografiaPassword, crittografiaSalt);
            if (!passDecrypted.equals(loginVO.getPassword())) {
                throw new OAuth2AuthenticationException(new OAuth2Error("invalid_client", "Errore di Autenticazione: Password errata", null));
            }
        } else {
            throw new OAuth2AuthenticationException(new OAuth2Error("invalid_client", "Errore di Autenticazione: Password non impostata per l'utente " + utenteVO.getUsername(), null));
        }

        ProfileUserVO profileUser = profileUserVOResponseDTO.getPayload();
        profileUser.setSessionId(generateUUID() + "");
        profileUser.setCdAmbito(applicazioneVO.getKey().getCdAmbito());
        profileUser.setCdApplicazione(applicazioneVO.getKey().getCdApplicazione());
        // Generazione token JWT
        profileUser.setFlagTokenReduced("N");
        String token = tokenBuilder.prepareToken(profileUser, false);
        //Se il token jwt è più grande della property jwtMaxLenght
        if (token.length() >= jwtMaxLenght) {
            profileUser.setFlagTokenReduced("S");
            writeCache("token_session_id_" + profileUser.getSessionId(), token);
            String tokenReduced = tokenBuilder.prepareToken(profileUser, true);
            profileUserVOResponseDTO.getPayload().setToken(tokenReduced);
        }else{
            profileUserVOResponseDTO.getPayload().setToken(token);
        }

        //ProfileUserVO profileUserVO = localLoginSist(request.getClientId(), request.getClientSecret(), true, false);

        return new TokenResponseDTO(token, "Bearer", (int) (Integer.parseInt(jwtExpirationTimeMinutes) * 7.5), "access");
    }

    private String prepareTokenMock(UtenteVO utente) {

        //Preparo una classe con i claim del token
        CurrentUser cu = prepareCurrentUserMock(utente);
        String token = jwtManager.createToken(cu);

        return token;
    }
    private CurrentUser prepareCurrentUserMock(UtenteVO authuser) {
        CurrentUser cu = new CurrentUser();
        cu.setUsername(authuser.getUsername());
        cu.getInfo().put("nome", authuser.getNome());
//        cu.getAuthorities().addAll(authuser.getAuthorities());

        return cu;
    }

    private ResponseDTO<ProfileUserVO> mockUtente(RequestDTO<UtenteVO> req) {
        ProfileUserVO response = new ProfileUserVO();
        //Utente
        UtenteVO vo = req.getPayload();
        if ("ERR".equals(vo.getUsername())) {
            throw new ApplicationException("Errore!"); //per testare 401
        }
        vo.setKey(1L);
        vo.setUsername(vo.getUsername());
        vo.setCognome("ROMA");
        vo.setNome("CAPITALE");
        vo.setCodiceFiscale("RMACPT66R06H501V");
        vo.setEmail("roma@sistinf.it");
        vo.setNumeroTelefono("335998877666");
        vo.setUfficio("Ufficio1: Via Po");
//
//        vo.getAuthorities().add("ROLE1");
//        vo.getAuthorities().add("ROLE2");
//        vo.getAuthorities().add("ROLE3");
        response.setUtente(vo);
        //Profilo
        ProfiloVO profilo = new ProfiloVO();
        profilo.setKey(1L);
        profilo.setDescrizione("Super utente");
        response.setProfilo(profilo);

        return new ResponseDTO<>(response);
    }

    public OidcVO createAccessToken(String code, String redirectUri, String clientId, String clientSecret, String accessTokenUrl, String idClient, boolean simulator, String userInfoUrl) throws Exception {
        log.info( "code: " + code);
        log.info("idClient: " +idClient);
        OidcVO token = new OidcVO();

        if (simulator) {
            //Caso simulator: mi arrivano i claim in Base64 direttamente sul parametro code
            token.setId_token(code);
        }else{
            //faccio la chiamata ad accesToken di IAM solo se presente url (caso senza simulator) mi arriva sul parametro code l'access code per chiamare l'endpoint access token
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_FORM_URLENCODED);

            MultiValueMap<String, String> body = new LinkedMultiValueMap<>();
            body.add("client_id", clientId);
            body.add("client_secret", clientSecret);
            body.add("grant_type", "authorization_code");
            body.add("redirect_uri", redirectUri);
            body.add("code", code);
            body.add("code_verifier",idClient);

            HttpEntity<MultiValueMap<String, String>> request = new HttpEntity<>(body, headers);

            ResponseEntity<String> response = restTemplate.postForEntity(accessTokenUrl, request, String.class);

            if (response.getStatusCode().is2xxSuccessful()) {
                ObjectMapper mapper = new ObjectMapper();
                OidcVO parsedToken = mapper.readValue(response.getBody(), OidcVO.class);
                log.info("AccessToken: "+ parsedToken.getAccess_token());
                token.setAccess_token(parsedToken.getAccess_token());
                token.setRefresh_token(parsedToken.getRefresh_token());
                token.setScope(parsedToken.getScope());
                token.setId_token(parsedToken.getId_token());
                token.setToken_type(parsedToken.getToken_type());
                token.setExpires_in(parsedToken.getExpires_in());
                token.setNonce(parsedToken.getNonce());
                token.setIdTokenDecodificato(parsedToken.getIdTokenDecodificato());

                //UserInfo
//                ResponseEntity<String> responseUserInfo = restTemplate.postForEntity(userInfoUrl, request, String.class);
//                log.info(responseUserInfo.toString());
                log.info("OidcVO: "+token.toString());
                return token;
            } else {
                throw new Exception("Errore nella chiamata token: HTTP " + response.getStatusCode() +" body: "+ response.getBody());
            }
        }
        return token;
    }


    public ProfileUserVO createIamProfileUserVO(OidcVO oidcVO, String cdAmbito, String codApplicazione, boolean simulator) throws Exception {

        // Set profilo in cache
        ProfileUserVO profileUser = new ProfileUserVO();
        oidcVO.decodificaToken(simulator);
        profileUser.setOidcVO(oidcVO);
        IdTokenDecodificato datiIAM = profileUser.getOidcVO().getIdTokenDecodificato();
        //Set abilitazione utente IAM
        List<String> abilitazioniList = new ArrayList<>();
        abilitazioniList.add("IAM_USER");
        profileUser.setAbilitazioni(abilitazioniList);

        //Recupero l'applicazione dal db per impostare il flag lista struttura
        ApplicazioneVO applicazioneVO = applicazioneClient.getApplicazione(cdAmbito, codApplicazione).getPayload();
        if (applicazioneVO != null && applicazioneVO.getFgListaStrutture() != null) {
            profileUser.setFgListaStrutture(applicazioneVO.getFgListaStrutture());
        }
        UtenteVO utenteVO = new UtenteVO();
        if (ControlloCampi.campoPieno(datiIAM.getIV_PG_CODFIS()) || ControlloCampi.campoPieno(datiIAM.getIV_PG_PIVA())) {
            utenteVO.setUsername(datiIAM.getIV_PG_CODFIS());
            utenteVO.setCodiceFiscale(datiIAM.getIV_PG_CODFIS());
            profileUser.setUtente(utenteVO);
        } else if (datiIAM.getIV_USER() != null && !datiIAM.getIV_USER().isBlank()) {
            //Se non è presente IV-USER imposto come username (obbligatorio) il codice fiscale in IV-CODFIS
            //utenteVO.setUsername(datiIAM.getIV_USER());
            //Recupero utente e abilitazioni dal db di Management relativi all'username
            LoginVO loginVO = new LoginVO();
            loginVO.setCdAmbito(cdAmbito);
            loginVO.setCdApplicazione(codApplicazione);
            loginVO.setUsername(datiIAM.getIV_USER());
            loginVO.setCodiceFiscale(StringUtils.trimAllWhitespace(datiIAM.getIV_CODFIS()));
            try {
                ProfileUserVO profileUserResp = utenteClient.getUtenteAndAbilitazioniByCodFiscale(makeRequestDTO(loginVO)).getPayload();
                profileUser.setUtente(profileUserResp.getUtente());
                profileUser.setAbilitazioni(profileUserResp.getAbilitazioni());
                if ("GET-BO".equals(codApplicazione)){
                    //controllo abilitazione superUser : se AMMINISTRATORE_GET non deve chiamare la lista strutture
                    List<String> abilitazioni = profileUser.getAbilitazioni();
                    boolean isSuperUtente = abilitazioni.stream()
                            .anyMatch("AMMINISTRATORE_GET"::equals);
                    if (isSuperUtente){
                        profileUser.setFgListaStrutture("N");
                        StrutturaVO strutturaVO = new StrutturaVO(); //set della struttura di default per superUtente
                        strutturaVO.setNmStruttura("QHAR");
                        strutturaVO.setDsStruttura("U.O.Sportello Unico Attivita' Produttive");
                        profileUser.setStruttura(strutturaVO);

                    }
                }
            } catch (Exception e) {
                log.error("Nessun utente trovato sul db di management con CodFiscale: " + loginVO.getCodiceFiscale(), e);
                utenteVO.setUsername(datiIAM.getIV_USER());
                profileUser.setUtente(utenteVO);
                ApplicazioniIAMEnum app = ApplicazioniIAMEnum.fromCodApplicazione(codApplicazione);
                if (!app.isLoginAnonimoConsentito()) {
                    throw new ApplicationException("Utente non autorizzato");
                }
            }
            if (profileUser.getUtente() != null) {
				ApplicazioniIAMEnum app = ApplicazioniIAMEnum.fromCodApplicazione(codApplicazione);
                if (!app.isLoginAnonimoConsentito()) {
                   ResponseDTO<UtenteVO> utenteResp = controlliUtenteAttivo(profileUser.getUtente());
                   profileUser.setUtente(utenteResp.getPayload());
                }
            }
        } else {
            utenteVO.setUsername(datiIAM.getIV_CODFIS());
            profileUser.setUtente(utenteVO);
        }


        //set Proprietà
        profileUser.setSessionId(generateUUID() + "");
        //writeCache("profile_session_id_" + profileUser.getSessionId(), profileUser);
        profileUser.setCdAmbito(cdAmbito);
        profileUser.setCdApplicazione(codApplicazione);
        generateTokenAndSetProfile(profileUser);

//        trackauditLogin(profileUser);
        return profileUser;
    }

    public ProfileUserVO selezionaStruttura(@Valid SelezionaStrutturaRequestVO request, String strCookie) {

        CurrentUser currentUser = jwtManager.consumeToken(strCookie);
//        // lettura token da cache se reduced
//        String sessionId = currentUser.getSessionId();
//        String tokenCompleto = null;
//        if ("S".equals(currentUser.getFlagTokenReduced())){
//            //Se il token è ridotto leggo il token completo tramite sessionId e riconsumo il token per avere tutte le abilitazioni
//            try {
//                tokenCompleto = readFromCache("token_session_id_" + sessionId);
//                currentUser = jwtManager.consumeToken(tokenCompleto);
//                currentUser.setToken(tokenCompleto);
//            }catch (Exception e){
//                log.error("Nessun token completo trovato in cache con sessionId: "+ sessionId);
//                throw ApplicationExceptionBuilder.builder().cause(e).build();
//            }
//        }
        ProfileUserVO profileUserVO =  prepareProfileUserVO(currentUser,request);

        if (request.getStruttura() != null){
            profileUserVO.setStruttura(request.getStruttura());
            currentUser.setCodStruttura(request.getStruttura().getNmStruttura());
            currentUser.setDescStruttura(request.getStruttura().getDsStruttura());
            currentUser.setFgListaStrutture("N");
            profileUserVO.setFgListaStrutture("N");
        }

        if (request.getUfficio() != null){
            profileUserVO.setUfficio(request.getUfficio());
            currentUser.setCodUfficio(request.getUfficio().getNmUfficio());
            currentUser.setDescUfficio(request.getUfficio().getDsUfficio());
        }

        if(request.getTributo() != null){
            profileUserVO.setTributo(request.getTributo());
            currentUser.setCodTributo(request.getTributo().getNmTributo());
            currentUser.setDescTributo(request.getTributo().getDsTributo());
        }

        generateTokenAndSetProfile(profileUserVO);
//        String tokenResp = jwtManager.createToken(currentUser);
        currentUser.setToken(profileUserVO.getToken());
        profileUserVO.setToken(profileUserVO.getToken());
        return profileUserVO;
    }

    public ProfileUserVO refreshToken(String strCookie) {

        CurrentUser currentUser = jwtManager.consumeToken(strCookie);
        // lettura token da cache se reduced
        String sessionId = currentUser.getSessionId();
        String tokenCompleto = null;
        if ("S".equals(currentUser.getFlagTokenReduced())){
            //Se il token è ridotto leggo il token completo tramite sessionId e riconsumo il token per avere tutte le abilitazioni
            try {
                tokenCompleto = readFromCache("token_session_id_" + sessionId);
                currentUser = jwtManager.consumeToken(tokenCompleto);
                currentUser.setToken(tokenCompleto);
            }catch (Exception e){
                log.error("Nessun token completo trovato in cache con sessionId: "+ sessionId);
                throw ApplicationExceptionBuilder.builder().cause(e).build();
            }
        }
        ProfileUserVO profileUserVO =  prepareProfileUserVO(currentUser, null);
        profileUserVO.setSessionId(sessionId);
        generateTokenAndSetProfile(profileUserVO);
//        String tokenResp = jwtManager.createToken(currentUser);
        currentUser.setToken(profileUserVO.getToken());
        return profileUserVO;
    }


    public ProfileUserVO prepareProfileUserVO(CurrentUser cu, SelezionaStrutturaRequestVO strutturaRequestVO) {
        ProfileUserVO authuser = new ProfileUserVO();
        /*
         * gestione del token ridotto
         */
        if (cu.getFlagTokenReduced() != null && cu.getFlagTokenReduced().equals("S")) {
            if (cu.getSessionId() != null){
                try {
                    String tokenCompleto = readFromCache("token_session_id_" + cu.getSessionId());
                    cu = jwtManager.consumeToken(tokenCompleto);
                } catch (Exception e) {
                    log.error("Non si riesce a decodificare il token in cache", e);
                    throw ApplicationExceptionBuilder.builder().cause(e).build();
                }
            } else {
                log.info("Il current user ha il sessionId a null per "+cu.getUsername());
            }
        }

        // UTENTE
        if (cu.getUsername() != null
                || cu.getNome() != null
                || cu.getCognome() != null
                || cu.getCodiceFiscale() != null) {

            //Get utente e abilitazioni da Management
            LoginVO loginVO = new LoginVO();
            loginVO.setUsername(cu.getUsername());
            loginVO.setCdAmbito(cu.getCdAmbito());
            loginVO.setCdApplicazione(cu.getCdApplicazione());
            if (cu.getIV_CODFIS() != null) {
                loginVO.setCodiceFiscale(StringUtils.trimAllWhitespace(cu.getIV_CODFIS()));
            }

            //Set dell'utente senza abilitazioni (nel caso in cui viene trovato sul db management sarà sovrascritto)
            UtenteVO utente = new UtenteVO();
            utente.setUsername(cu.getUsername());
            utente.setNome(cu.getNome());
            utente.setCognome(cu.getCognome());
            if (cu.getCodiceFiscale() != null) {
                utente.setCodiceFiscale(cu.getCodiceFiscale());
            }
            authuser.setUtente(utente);

            //Caso seleziona struttura GET
            if (strutturaRequestVO != null && cu.getFgListaStrutture() != null && "S".equals(cu.getFgListaStrutture()) && "GET-BO".equals(cu.getCdApplicazione())) {
                log.info("Se GET-BO recupero le abilitazioni per la struttura selezionata");
                try {
                    String codStrutturaGet = strutturaRequestVO.getStruttura().getNmStruttura();
                    ResponseDTO<ProfileUserVO> profileUserResp = utenteClient.getUtenteAndAbilitazioniByCodFiscaleAndStruttura(makeRequestDTO(loginVO), codStrutturaGet);
                    if (profileUserResp.getPayload() != null) {
                        authuser = profileUserResp.getPayload();
                        cu.setAuthorities(profileUserResp.getPayload().getAbilitazioni());
                    }
                } catch (Exception e) {
                    log.error("Errore durante la ricerca abilitazioni utente per struttura GET sul db di management con CodFiscale: " + cu.getIV_CODFIS(), e);
                }
            } else {
                log.info("Se Non GET-BO recupero le abilitazioni");
                try {
                    if (!"GET-BO".equals(cu.getCdApplicazione()) && loginVO.getCodiceFiscale() != null) {
                        ResponseDTO<ProfileUserVO> profileUserResp = utenteClient.getUtenteAndAbilitazioniByCodFiscale(makeRequestDTO(loginVO));
                        if (profileUserResp.getPayload() != null) {
                            authuser = profileUserResp.getPayload();
                        } else {
                            log.error("Errore!! Risposta a null da management su utente con cf: "+loginVO.getCodiceFiscale() );
                        }
                    }
                } catch (Exception e) {
                    log.error("Errore durante la ricerca utente sul db di management con CodFiscale: " + loginVO.getCodiceFiscale() + " " + e.getMessage());
                }
            }
        } else {
            log.error("Utente senza attributi: "+cu.toString());
        }

        if (cu.getCdAmbito() != null){
            log.info("CdAmbito: "+cu.getCdAmbito()+" per utente "+cu.getUsername());
            authuser.setCdAmbito(cu.getCdAmbito());
        }
        if (cu.getCdApplicazione() != null){
            log.info("CdApplicazione: "+cu.getCdApplicazione()+" per utente "+cu.getUsername());
            authuser.setCdApplicazione(cu.getCdApplicazione());
        }

        // PROFILO
//        if (cu.getIdProfilo() != null) {
//            ProfiloVO profilo = new ProfiloVO();
//            profilo.setKey(Long.valueOf(cu.getIdProfilo()));
//            authuser.setProfilo(profilo);
//        }

        // LISTA STRUTTURE
        if (cu.getFgListaStrutture() != null) {
            authuser.setFgListaStrutture(cu.getFgListaStrutture());
        }

        if (cu.getSessionId() != null){
            authuser.setSessionId(cu.getSessionId());
        }

        // Flag reduced
        if (cu.getFlagTokenReduced() != null) {
            authuser.setFlagTokenReduced(cu.getFlagTokenReduced());
        }

        // STRUTTURA
        if (cu.getCodStruttura() != null || cu.getDescStruttura() != null) {
            StrutturaVO struttura = new StrutturaVO();
            struttura.setNmStruttura(cu.getCodStruttura());
            struttura.setDsStruttura(cu.getDescStruttura());
            authuser.setStruttura(struttura);
        }

        // UFFICIO
        if (cu.getCodUfficio() != null || cu.getDescUfficio() != null) {
            UfficioVO ufficio = new UfficioVO();
            ufficio.setNmUfficio(cu.getCodUfficio());
            ufficio.setDsUfficio(cu.getDescUfficio());
            authuser.setUfficio(ufficio);
        }

        // TRIBUTO
        if (cu.getCodTributo() != null || cu.getDescTributo() != null) {
            TributoVO tributo = new TributoVO();
            tributo.setNmTributo(cu.getCodTributo());
            tributo.setDsTributo(cu.getDescTributo());
            authuser.setTributo(tributo);
        }

        // IAM (IdTokenDecodificato dentro OidcVO)
        if (hasIAMFields(cu)) {
            IdTokenDecodificato idToken = new IdTokenDecodificato();

            idToken.setIV_ASS_UID(cu.getIV_ASS_UID());
            idToken.setIV_ASS_CODFIS(cu.getIV_ASS_CODFIS());
            idToken.setIV_PG_CODFIS(cu.getIV_PG_CODFIS());
            idToken.setIV_PG_PIVA(cu.getIV_PG_PIVA());
            idToken.setIV_PG_RAG_SOC(cu.getIV_PG_RAG_SOC());
            idToken.setIV_PG_NATURA(cu.getIV_PG_NATURA());
            idToken.setIV_PG_NREA(cu.getIV_PG_NREA());
            idToken.setIV_PG_CCIAA(cu.getIV_PG_CCIAA());
            idToken.setIV_PG_UID(cu.getIV_PG_UID());
            idToken.setIV_PG_INDIRIZZO(cu.getIV_PG_INDIRIZZO());
            idToken.setIV_PG_CIV_IND(cu.getIV_PG_CIV_IND());
            idToken.setIV_PG_ESP_IND(cu.getIV_PG_ESP_IND());
            idToken.setIV_PG_COM_IND(cu.getIV_PG_COM_IND());
            idToken.setIV_PG_CAP_IND(cu.getIV_PG_CAP_IND());
            idToken.setIV_PG_PROV_IND(cu.getIV_PG_PROV_IND());
            idToken.setIV_PG_MAIL(cu.getIV_PG_MAIL());
            idToken.setIV_PG_MAIL_PEC(cu.getIV_PG_MAIL_PEC());
            idToken.setIV_PG_TELEFONO(cu.getIV_PG_TELEFONO());
            idToken.setIV_PG_MOBILE(cu.getIV_PG_MOBILE());
            idToken.setIV_PG_RUOLO(cu.getIV_PG_RUOLO());
            idToken.setIV_PG_CONSENSO_GDPR(cu.getIV_PG_CONSENSO_GDPR());
            idToken.setIV_PG_CATEGORIA(cu.getIV_PG_CATEGORIA());

            idToken.setIV_CODFIS(cu.getIV_CODFIS());
            idToken.setIV_NOME(cu.getIV_NOME());
            idToken.setIV_COGNOME(cu.getIV_COGNOME());
            idToken.setIV_NASCITA_DATA(cu.getIV_NASCITA_DATA());
            idToken.setIV_SEX(cu.getIV_SEX());
            idToken.setIV_NASCITA_COMUNE(cu.getIV_NASCITA_COMUNE());
            idToken.setIV_NASCITA_NAZIONE(cu.getIV_NASCITA_NAZIONE());

            idToken.setIV_RES_VIA(cu.getIV_RES_VIA());
            idToken.setIV_RES_CIVICO(cu.getIV_RES_CIVICO());
            idToken.setIV_RES_EDIFICIO(cu.getIV_RES_EDIFICIO());
            idToken.setIV_RES_LOTTO(cu.getIV_RES_LOTTO());
            idToken.setIV_RES_COMUNE(cu.getIV_RES_COMUNE());
            idToken.setIV_RES_PROV(cu.getIV_RES_PROV());
            idToken.setIV_RES_CAP(cu.getIV_RES_CAP());
            idToken.setIV_RES_NAZIONE(cu.getIV_RES_NAZIONE());

            idToken.setIV_EMAIL(cu.getIV_EMAIL());
            idToken.setIV_MAILP(cu.getIV_MAILP());
            idToken.setIV_TEL(cu.getIV_TEL());
            idToken.setIV_CELL(cu.getIV_CELL());
            idToken.setIV_USER(cu.getIV_USER());
            idToken.setCd_ambito(cu.getCdAmbito());
            // --- scope anagrafica ---
            idToken.setIv_nascita_prov(cu.getIv_nascita_prov());

            // --- persona giuridica ---
            idToken.setIv_pg_delega(cu.getIv_pg_delega());
            idToken.setIv_pg_ruolo_cod(cu.getIv_pg_ruolo_cod());
            idToken.setIv_pg_categoria_cod(cu.getIv_pg_categoria_cod());

            // --- attributi delega ---
            idToken.setIv_dg_iat(cu.getIv_dg_iat());
            idToken.setIv_dg_exp(cu.getIv_dg_exp());
            idToken.setIv_dg_nbf(cu.getIv_dg_nbf());
            idToken.setIv_dg_services(cu.getIv_dg_services());
            idToken.setIv_dg_id(cu.getIv_dg_id());
            idToken.setIv_dg_cognome(cu.getIv_dg_cognome());
            idToken.setIv_dg_codfis(cu.getIv_dg_codfis());
            idToken.setIv_dg_nome(cu.getIv_dg_nome());
            idToken.setIv_dg_telefono(cu.getIv_dg_telefono());

            // --- residenza ---
            idToken.setIv_res_int(cu.getIv_res_int());
            idToken.setIv_res_scala(cu.getIv_res_scala());

            // --- domicilio ---
            idToken.setIv_dom_via(cu.getIv_dom_via());
            idToken.setIv_dom_comune(cu.getIv_dom_comune());
            idToken.setIv_dom_prov(cu.getIv_dom_prov());
            idToken.setIv_dom_cap(cu.getIv_dom_cap());

            // --- assistito ---
            idToken.setIv_ass_rag_soc(cu.getIv_ass_rag_soc());

            OidcVO oidcVO = new OidcVO();
            oidcVO.setIdTokenDecodificato(idToken);
            authuser.setOidcVO(oidcVO);
        }

        // ABILITAZIONI
        authuser.setAbilitazioni(new ArrayList<>(cu.getAuthorities()));
        log.info("Metodo prepareProfileUserVO completato per utente: "+cu.getUsername());
        return authuser;
    }

    /**
     * Controlla se ci sono campi IAM valorizzati
     */
    private boolean hasIAMFields(CurrentUser cu) {
        return cu.getIV_NOME() != null
                || cu.getIV_COGNOME() != null
                || cu.getIV_USER() != null
                || cu.getIV_CODFIS() != null;
    }

}
