package it.sistinf.romacapitale.auth.api;

import it.sistinf.romacapitale.auth.domain.LoginDomain;
import it.sistinf.romacapitale.auth.dto.ErrorResponseDTO;
import it.sistinf.romacapitale.auth.dto.TokenRequestDTO;
import it.sistinf.romacapitale.integration.auth.vo.TokenResponseDTO;
import it.sistinf.romacapitale.auth.utils.PkceUtils;
import it.sistinf.romacapitale.core.dto.ResponseDTO;
import it.sistinf.romacapitale.core.exceptions.ApplicationException;
import it.sistinf.romacapitale.core.security.CurrentUser;
import it.sistinf.romacapitale.core.vo.auth.LoginVO;
import it.sistinf.romacapitale.integration.management.vo.IdTokenDecodificato;
import it.sistinf.romacapitale.integration.management.vo.OidcVO;
import it.sistinf.romacapitale.integration.management.vo.ProfileUserVO;
import it.sistinf.romacapitale.integration.management.vo.requestVO.SelezionaStrutturaRequestVO;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.env.Environment;
import org.springframework.http.*;
import org.springframework.util.MultiValueMap;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.util.UriComponentsBuilder;

import java.net.URI;
import java.util.UUID;

@Slf4j
@RestController
@RequiredArgsConstructor
@RequestMapping("/api/v1/autenticazione")
public class LoginV1 extends AbstractLoginApi {

    @Value("${auth.cookie.secure}")
    private Boolean cookieSecure;

    @Value("${auth.cookie.domain}")
    private String cookieDomain;

    @Value("${auth.cookie.samesite}")
    private String cookieSamesite;

    @Value("${iam.config.issuer}")
    private String iamIssuer;

    @Value("${iam.config.accessTokenUrl}")
    private String accessTokenUrl;

    @Value("${iam.config.userInfoUrl}")
    private String userInfoUrl;

    private final Environment env;
    private final LoginDomain loginDomain;


    @PostMapping("/login")
    public ResponseEntity<ResponseDTO<ProfileUserVO>> login(@Valid @RequestBody LoginVO loginForm) {
        ProfileUserVO profileUserVO = loginDomain.localLogin(loginForm, true, false);
        String token = profileUserVO.getToken()+"";
        profileUserVO.setToken(token);
        ResponseDTO<ProfileUserVO> response = new ResponseDTO(profileUserVO);
//        return ResponseEntity.ok().header("Authorization", new String[]{"Bearer "+token}).body(response);
        ResponseCookie bearerCookie = ResponseCookie.from("Bearer", token)
                .httpOnly(true)
                .secure(Boolean.TRUE.equals(cookieSecure))
                .domain(cookieDomain)
                .sameSite(cookieSamesite)
                .path("/")
                .maxAge(-1)
                .build();

        return ResponseEntity
                .status(HttpStatus.OK)
                .header(HttpHeaders.SET_COOKIE, bearerCookie.toString())
//                .header(HttpHeaders.AUTHORIZATION, "Bearer " + token)
                .body(response);
    }

    @GetMapping("/loginSist")
    @Deprecated
    public ResponseEntity<ResponseDTO<ProfileUserVO>> loginSist(@RequestParam("username") String username) {
        ProfileUserVO profileUserVO = loginDomain.localLoginSist(username, null, false, false);
        String token = profileUserVO.getToken()+"";
        profileUserVO.setToken(null);
        ResponseDTO<ProfileUserVO> response = new ResponseDTO(profileUserVO);
        return ResponseEntity.ok().header("Authorization", new String[]{"Bearer "+token}).body(response);
    }

    @PostMapping("/oauth/token")
    public ResponseEntity<?> loginSist(@RequestBody TokenRequestDTO request) {
        try {
            TokenResponseDTO response = loginDomain.loginSist(request);
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            ErrorResponseDTO error = new ErrorResponseDTO("error", e.getMessage());
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(error);
        }
    }

    @GetMapping("/loginIAM")
    public ResponseEntity<Void> loginIAM(@RequestParam("cd_ambito") String ambito, @RequestParam("cd_applicazione") String applicazione, @RequestParam(name = "useTrueIAM", defaultValue = "false") boolean useTrueIAM,
                                         @RequestParam(name = "useHomeUri", defaultValue = "false") boolean useHomeUri, @RequestParam(name = "use_eidas", defaultValue = "false") boolean useEidas) {
        return getAuthorizeUrlIAM(ambito, applicazione, useTrueIAM, useHomeUri,useEidas);
    }

    private ResponseEntity<Void> getAuthorizeUrlIAM(String ambito, String applicazione, boolean useTrueIAM, boolean useHomeUri, boolean useEidas) {
        String prefix = "";
        String codeVerifier = "";
        String codeChallenge = "";
        String codeChallengeMethod = "S256";
        ResponseCookie cookie = null;
//   EiDas non ancora in produzione
//        if ("06".equals(ambito) && "GET-FO".equals(applicazione)) {
//            useEidas = true;
//        } else {
//            useEidas = false;
//        }

        if (useTrueIAM) {
            //Caso senza simulator: si creano code verifier e code challenge
            prefix = String.format("iam.config.%s.%s", ambito, applicazione);

            try {
                // code challenge
                PkceUtils pkce = new PkceUtils();
                codeVerifier = pkce.generateCodeVerifier();
                codeChallenge = pkce.generateCodeChallange(codeVerifier);
            } catch (Exception e) {
                throw new ApplicationException("Errore durante la generazione del code challenge", e);
            }

            // cookie di sessione per persistere l'id client
            String randomId = "E" + UUID.randomUUID().toString();
            cookie = ResponseCookie.from("idClient", codeVerifier)
                    .httpOnly(true)
                    .secure(Boolean.TRUE.equals(cookieSecure))
                    .sameSite(cookieSamesite)
                    .domain(".comune.roma.it")
                    .path("/")
                    .maxAge(-1)
                    .build();
        } else {
            prefix = String.format("iam.config.%s.%s.simulator", ambito, applicazione);
        }

        String clientId = env.getProperty(prefix + ".client.id");
        String redirectUrl = env.getProperty(prefix + ".redirect.uri");
        String scope = env.getProperty(prefix + ".scope");
        if (useHomeUri){
            scope = env.getProperty(prefix + ".scope2");
        }
        String nonce = UUID.randomUUID().toString();
        String redirectUrlBase = env.getProperty(prefix + ".authorizeUrl");
        UriComponentsBuilder builder = UriComponentsBuilder
                .fromHttpUrl(redirectUrlBase)
                .queryParam("client_id", clientId)
                .queryParam("redirect_uri", redirectUrl)
                .queryParam("scope", scope)
                .queryParam("tipo_utente", (Object) null)
                .queryParam("response_type", "code")
                .queryParam("response_mode", "form_post")
                .queryParam("nonce", nonce);
        if (useTrueIAM) {
            builder.queryParam("code_challenge", codeChallenge)
                    .queryParam("code_challenge_method", codeChallengeMethod);
        }
        if (useEidas) {
            builder.queryParam("acr_values", "eidas");
//            builder.queryParam("acr_values", "urn:comune:roma:auth:eidas");
        }
        String authorizeUrl = builder.build().toUriString();
        HttpHeaders headers = new HttpHeaders();
        headers.setLocation(URI.create(authorizeUrl));
        if (useTrueIAM) {
            headers.add(HttpHeaders.SET_COOKIE, cookie.toString());
        }
        if (useHomeUri){
            ResponseCookie cookieHomeUri = ResponseCookie.from("useHomeUri", "true")
                    .httpOnly(true)
                    .secure(Boolean.TRUE.equals(cookieSecure))
                    .sameSite(cookieSamesite)
                    .domain(".comune.roma.it")
                    .path("/")
                    .maxAge(-1)
                    .build();
            headers.add(HttpHeaders.SET_COOKIE, cookieHomeUri.toString());
        }
        return new ResponseEntity<>(headers, HttpStatus.FOUND);
    }

    //CALLBACK AMBITO 06 SPORTELLI
    @RequestMapping(
            value = "/oidc_get_fo/callback",
            method = {RequestMethod.GET, RequestMethod.POST},
            consumes = {MediaType.APPLICATION_FORM_URLENCODED_VALUE, MediaType.ALL_VALUE}
    )
    public ResponseEntity<ResponseDTO<ProfileUserVO>> callbackGetFo(
            @RequestParam MultiValueMap<String, String> formParams,
            @CookieValue(value = "useHomeUri", required = false) String useHomeUri,
            @CookieValue(value = "idClient", required = false) String idClient) throws Exception {

        String clientId = formParams.getFirst("client_id");
        String code = formParams.getFirst("code");
        String issuer = formParams.getFirst("iss");
        String scope = formParams.getFirst("scope");

        log.info("Entrato in callBack oidc_get_fo");
        if (formParams.isEmpty()) {
            log.info("Nessun parametro ricevuto nella request di callback");
        } else {
            log.info("Parametri ricevuti:");
            formParams.forEach((key, values) -> {
                log.info("  -> {} = {}", key, values);
            });
            log.info("  -> {} = {}", "useHomeUri", useHomeUri);
        }
//        log.info("code=" + code);
//        log.info("scope=" + scope);
//        log.info("issuer=" + issuer);
//        log.info("client_id=" + clientId);
//        log.info("idClient cookie=" + idClient);
        String cdAmbito = "06";
        String codApplicazione = "GET-FO";

        boolean simulator = "iam_simulator".equals(issuer);
        return makeResponseCallback(code, clientId, cdAmbito, codApplicazione, idClient, simulator, useHomeUri);
    }

    @GetMapping("/oidc_get_fo/home")
    public ResponseEntity<Void> homeServiceGetFo() {
        String cdAmbito = "06";
        String codApplicazione = "GET-FO";
        return getAuthorizeUrlIAM(cdAmbito, codApplicazione, true, true, false);
    }

    @RequestMapping(
            value = "/oidc_get_bo/callback",
            method = {RequestMethod.GET, RequestMethod.POST},
            consumes = {MediaType.APPLICATION_FORM_URLENCODED_VALUE, MediaType.ALL_VALUE})
    public ResponseEntity<ResponseDTO<ProfileUserVO>> callbackGetBo(
            @RequestParam MultiValueMap<String, String> formParams,
            @CookieValue(value = "useHomeUri", required = false) String useHomeUri,
            @CookieValue(value = "idClient", required = false) String idClient) throws Exception {

        String clientId = formParams.getFirst("client_id");
        String code = formParams.getFirst("code");
        String issuer = formParams.getFirst("iss");
        String scope = formParams.getFirst("scope");

        log.info("Entrato in callBack oidc_get_bo");
        log.info("code=" + code);
        log.info("scope=" + scope);
        log.info("issuer=" + issuer);
        log.info("client_id=" + clientId);
        log.info("idClient cookie=" + idClient);
        String cdAmbito = "06";
        String codApplicazione = "GET-BO";
        boolean simulator = "iam_simulator".equals(issuer);
        return makeResponseCallback(code, clientId, cdAmbito, codApplicazione, idClient, simulator, useHomeUri);

    }

    //CALLBACK AMBITO 02 TRIBUTI
    @RequestMapping(
            value = "/oidc_gerico/callback",
            method = {RequestMethod.GET, RequestMethod.POST},
            consumes = {MediaType.APPLICATION_FORM_URLENCODED_VALUE, MediaType.ALL_VALUE})
    public ResponseEntity<ResponseDTO<ProfileUserVO>> callbackGerico(
            @RequestParam MultiValueMap<String, String> formParams,
            @CookieValue(value = "useHomeUri", required = false) String useHomeUri,
            @CookieValue(value = "idClient", required = false) String idClient) throws Exception {

        String clientId = formParams.getFirst("client_id");
        String code = formParams.getFirst("code");
        String issuer = formParams.getFirst("iss");
        String scope = formParams.getFirst("scope");

        log.info("Entrato in callBack oidc_gerico");
        log.info("code=" + code);
        log.info("scope=" + scope);
        log.info("issuer=" + issuer);
        log.info("client_id=" + clientId);
        log.info("idClient cookie=" + idClient);
        String cdAmbito = "02";
        String codApplicazione = "GERICO";
        boolean simulator = "iam_simulator".equals(issuer);
        return makeResponseCallback(code, clientId, cdAmbito, codApplicazione, idClient, simulator, useHomeUri);
    }

    @GetMapping("/oidc_gerico/home")
    public ResponseEntity<Void> homeServiceGerico() {
        String cdAmbito = "02";
        String codApplicazione = "GERICO";
        return getAuthorizeUrlIAM(cdAmbito, codApplicazione, true, true, false);
    }

    @RequestMapping(
            value = "/oidc_gescan_fe/callback",
            method = {RequestMethod.GET, RequestMethod.POST},
            consumes = {MediaType.APPLICATION_FORM_URLENCODED_VALUE, MediaType.ALL_VALUE})
    public ResponseEntity<ResponseDTO<ProfileUserVO>> callbackGescanFe(
            @RequestParam MultiValueMap<String, String> formParams,
            @CookieValue(value = "useHomeUri", required = false) String useHomeUri,
            @CookieValue(value = "idClient", required = false) String idClient) throws Exception {

        String clientId = formParams.getFirst("client_id");
        String code = formParams.getFirst("code");
        String issuer = formParams.getFirst("iss");
        String scope = formParams.getFirst("scope");

        log.info("Entrato in callBack oidc_gescan_fe");
        log.info("code=" + code);
        log.info("scope=" + scope);
        log.info("issuer=" + issuer);
        log.info("client_id=" + clientId);
        log.info("idClient cookie=" + idClient);
        String cdAmbito = "02";
        String codApplicazione = "GESCAN";
        boolean simulator = "iam_simulator".equals(issuer);
        return makeResponseCallback(code, clientId, cdAmbito, codApplicazione, idClient, simulator, useHomeUri);

    }

    @RequestMapping(
            value = "/oidc_tributi_bo/callback",
            method = {RequestMethod.GET, RequestMethod.POST},
            consumes = {MediaType.APPLICATION_FORM_URLENCODED_VALUE, MediaType.ALL_VALUE})
    public ResponseEntity<ResponseDTO<ProfileUserVO>> callbackBoTributi(
            @RequestParam MultiValueMap<String, String> formParams,
            @CookieValue(value = "useHomeUri", required = false) String useHomeUri,
            @CookieValue(value = "idClient", required = false) String idClient) throws Exception {

        String clientId = formParams.getFirst("client_id");
        String code = formParams.getFirst("code");
        String issuer = formParams.getFirst("iss");
        String scope = formParams.getFirst("scope");

        log.info("Entrato in callBack oidc_gescan_fe");
        log.info("code=" + code);
        log.info("scope=" + scope);
        log.info("issuer=" + issuer);
        log.info("client_id=" + clientId);
        log.info("idClient cookie=" + idClient);
        String cdAmbito = "02";
        String codApplicazione = "BO_TRIBUTI";
        boolean simulator = "iam_simulator".equals(issuer);
        return makeResponseCallback(code, clientId, cdAmbito, codApplicazione,idClient, simulator,useHomeUri);
    }

    @RequestMapping(
            value = "/oidc_gecos_bo/callback",
            method = {RequestMethod.GET, RequestMethod.POST},
            consumes = {MediaType.APPLICATION_FORM_URLENCODED_VALUE, MediaType.ALL_VALUE})
    public ResponseEntity<ResponseDTO<ProfileUserVO>> callbackGecosBo(
            @RequestParam MultiValueMap<String, String> formParams,
            @CookieValue(value = "useHomeUri", required = false) String useHomeUri,
            @CookieValue(value = "idClient", required = false) String idClient) throws Exception {

        String clientId = formParams.getFirst("client_id");
        String code = formParams.getFirst("code");
        String issuer = formParams.getFirst("iss");
        String scope = formParams.getFirst("scope");

        log.info("Entrato in callBack oidc_gecos_bo");
        log.info("code=" + code);
        log.info("scope=" + scope);
        log.info("issuer=" + issuer);
        log.info("client_id=" + clientId);
        log.info("idClient cookie=" + idClient);
        String cdAmbito = "02";
        String codApplicazione = "GECOS";
        boolean simulator = "iam_simulator".equals(issuer);
        return makeResponseCallback(code, clientId, cdAmbito, codApplicazione,idClient, simulator,useHomeUri);
    }


    @RequestMapping(
            value = "/oidc_gecos_fo/callback",
            method = {RequestMethod.GET, RequestMethod.POST},
            consumes = {MediaType.APPLICATION_FORM_URLENCODED_VALUE, MediaType.ALL_VALUE})
    public ResponseEntity<ResponseDTO<ProfileUserVO>> callbackGecosFo(
            @RequestParam MultiValueMap<String, String> formParams,
            @CookieValue(value = "useHomeUri", required = false) String useHomeUri,
            @CookieValue(value = "idClient", required = false) String idClient) throws Exception {

        String clientId = formParams.getFirst("client_id");
        String code = formParams.getFirst("code");
        String issuer = formParams.getFirst("iss");
        String scope = formParams.getFirst("scope");

        log.info("Entrato in callBack oidc_gecos_fo");
        log.info("code=" + code);
        log.info("scope=" + scope);
        log.info("issuer=" + issuer);
        log.info("client_id=" + clientId);
        log.info("idClient cookie=" + idClient);
        String cdAmbito = "02";
        String codApplicazione = "GECOS-FO";
        boolean simulator = "iam_simulator".equals(issuer);
        return makeResponseCallback(code, clientId, cdAmbito, codApplicazione,idClient, simulator,useHomeUri);
    }

    @GetMapping("/oidc_gecos_fo/home")
    public ResponseEntity<Void> homeServiceGecosFo() {
        String cdAmbito = "02";
        String codApplicazione = "GECOS-FO";
        return getAuthorizeUrlIAM(cdAmbito, codApplicazione, true, true, false);
    }

    private ResponseEntity<ResponseDTO<ProfileUserVO>> makeResponseCallback(String code, String clientId, String cdAmbito, String codApplicazione, String idClient, boolean simulator, String useHomeUri) throws Exception {
        String prefix = "";
        if (simulator){
            prefix = String.format("iam.config.%s.%s.simulator", cdAmbito, codApplicazione);

        }else{
            prefix = String.format("iam.config.%s.%s", cdAmbito, codApplicazione);
        }
        String redirectUrl = env.getProperty(prefix + ".redirect.uri");
        String secret = env.getProperty(prefix + ".client.secret");
//        String accessTokenUrl = env.getProperty(prefix + ".accessTokenUrl");
        OidcVO oidcVO = loginDomain.createAccessToken(
                code,
                redirectUrl,
                clientId,
                secret,
                accessTokenUrl,
                idClient,
                simulator,
                userInfoUrl
        );
        //aggiungo i  claim di IAM al CurrentUser e al token di Common
        ProfileUserVO profileUserVO = loginDomain.createIamProfileUserVO(oidcVO, cdAmbito, codApplicazione,simulator);
        String token = profileUserVO.getToken()+"";
        profileUserVO.setToken(token);
        ResponseDTO<ProfileUserVO> response = new ResponseDTO(profileUserVO);
        String homeUrl = env.getProperty(prefix + ".home.uri");
        if ("true".equals(useHomeUri)){
            homeUrl=env.getProperty(prefix + ".home.fe.uri");
        }
        ResponseCookie bearerCookie = null;
        if (simulator) {
             bearerCookie = ResponseCookie.from("Bearer", token)
                    .httpOnly(true)
                    .secure(Boolean.TRUE.equals(cookieSecure))
                    .sameSite(cookieSamesite)
                    .domain(cookieDomain)
                    .path("/")
                    .maxAge(-1)
                    .build();
        }else {
            bearerCookie = ResponseCookie.from("Bearer", token)
                    .httpOnly(true)
                    .secure(Boolean.TRUE.equals(cookieSecure))
                    .sameSite(cookieSamesite)
                    .domain(".comune.roma.it")
                    .path("/")
                    .maxAge(-1)
                    .build();

            //Elimino il cookie di useHomeUri dopo l'utilizzo
            ResponseCookie deleteCookie = ResponseCookie.from("useHomeUri", "")
                    .httpOnly(true)
                    .secure(Boolean.TRUE.equals(cookieSecure))
                    .sameSite(cookieSamesite)
                    .domain(".comune.roma.it")
                    .path("/")
                    .maxAge(0)
                    .build();
        }
        return ResponseEntity
                .status(HttpStatus.FOUND)
                .location(URI.create(homeUrl))
                .header(HttpHeaders.SET_COOKIE, bearerCookie.toString())
                .body(response);
    }

    @PostMapping("/seleziona-struttura")
    public ResponseEntity<ResponseDTO<ProfileUserVO>> selezionaStruttura(@CookieValue("Bearer") String strCookie, @RequestBody SelezionaStrutturaRequestVO request) {
        ProfileUserVO profileUserVO = loginDomain.selezionaStruttura(request,strCookie);
        String token = profileUserVO.getToken();
        ResponseDTO<ProfileUserVO> response = new ResponseDTO(profileUserVO);
//        return ResponseEntity.ok().header("Authorization", new String[]{"Bearer "+token}).body(response);
        ResponseCookie bearerCookie = ResponseCookie.from("Bearer", token)
                .httpOnly(true)
                .secure(Boolean.TRUE.equals(cookieSecure))
                .domain(cookieDomain)
                .sameSite(cookieSamesite)
                .path("/")
                .maxAge(-1)
                .build();

        return ResponseEntity
                .status(HttpStatus.OK)
                .header(HttpHeaders.SET_COOKIE, bearerCookie.toString())
                .body(response);
    }

    @PostMapping("/refresh-token")
    public ResponseEntity<ResponseDTO<ProfileUserVO>> refreshToken(@CookieValue("Bearer") String strCookie) {
        ProfileUserVO profileUserVO = loginDomain.refreshToken(strCookie);
        String token = profileUserVO.getToken();
        ResponseDTO<ProfileUserVO> response = new ResponseDTO(profileUserVO);
//        return ResponseEntity.ok().header("Authorization", new String[]{"Bearer "+token}).body(response);
        ResponseCookie bearerCookie = ResponseCookie.from("Bearer", token)
                .httpOnly(true)
                .secure(Boolean.TRUE.equals(cookieSecure))
                .domain(cookieDomain)
                .sameSite(cookieSamesite)
                .path("/")
                .maxAge(-1)
                .build();

        return ResponseEntity
                .status(HttpStatus.OK)
                .header(HttpHeaders.SET_COOKIE, bearerCookie.toString())
                .body(response);
    }

    @PostMapping("/decode-iam-token")
    public ResponseEntity<ResponseDTO<ProfileUserVO>> decodificaTokenIAM(@RequestParam("cd_ambito") String cdAmbito,
                                                                         @RequestParam("cd_applicazione") String cdApplicazione, @RequestBody OidcVO oidcVO) throws Exception {
        //validazione del token IAM
        IdTokenDecodificato idTokenDecodificato = consumeTokenIAM(oidcVO.getId_token());
        //aggiungo i  claim di IAM al CurrentUser e al token di Common
        ProfileUserVO profileUserVO = loginDomain.createIamProfileUserVO(oidcVO, cdAmbito, cdApplicazione, false);
        ResponseDTO<ProfileUserVO> response = new ResponseDTO(profileUserVO);
//        return ResponseEntity.ok().header("Authorization", new String[]{"Bearer "+token}).body(response);
        ResponseCookie bearerCookie = ResponseCookie.from("Bearer", profileUserVO.getToken())
                .httpOnly(true)
                .secure(Boolean.TRUE.equals(cookieSecure))
                .domain(cookieDomain)
                .sameSite(cookieSamesite)
                .path("/")
                .maxAge(-1)
                .build();

        return ResponseEntity
                .status(HttpStatus.OK)
                .header(HttpHeaders.SET_COOKIE, bearerCookie.toString())
                .body(response);
    }

    @GetMapping("/logout")
    public ResponseEntity<ResponseDTO<ProfileUserVO>> logout() {
        ProfileUserVO profileUserVO = new ProfileUserVO();
        ResponseDTO<ProfileUserVO> response = new ResponseDTO(profileUserVO);
        return cleanAllCookies(response,true);
    }

    @GetMapping("/local-logout")
    public ResponseEntity<ResponseDTO<ProfileUserVO>> localLogout() {
        ProfileUserVO profileUserVO = new ProfileUserVO();
        ResponseDTO<ProfileUserVO> response = new ResponseDTO(profileUserVO);
        return cleanLocalCookies(response,true);
    }
    @GetMapping(value = "/decodifica")
    public ResponseEntity<ResponseDTO<ProfileUserVO>> decodifica(@CookieValue(value = "Bearer",required = false) String strCookie) {

        ProfileUserVO profileUserVO = new ProfileUserVO();
        ResponseDTO<ProfileUserVO> response = new ResponseDTO(profileUserVO);

        //Aggiunto per la prima chiamata
        if (strCookie == null || strCookie.isBlank()) {
//            String idClient = getIdClientFromCookie();
//            if (idClient != null && !idClient.isBlank()) {
//               return makeResponseNotAuthorized();
//                throw  new UserUnauthorizedException("");
//            }
            log.info("Decodifica: no Bearer cookie present");
            response.setPayload(null);
            return ResponseEntity
                    .status(HttpStatus.OK)
                    .body(response);
        }
        CurrentUser currentUser = null;
        try {
             currentUser = jwtManager.consumeToken(strCookie);
        } catch (Exception e) {
            log.error("Decodifica: Token non valido : " + strCookie, e);
            //Non deve mandare messaggi di errore, 200 con payload null quando il token non è valido
            response.setPayload(null);
            return ResponseEntity
                        .status(HttpStatus.OK)
                        .body(response);

        }

        // Costruisco la response con user, profilo e token preso dal cookie
        try {
            log.info("Decodifica: chiamo prepareProfileUserVO per "+ currentUser.getUsername());
            profileUserVO =  loginDomain.prepareProfileUserVO(currentUser, null);
            profileUserVO.setToken(strCookie);
            response.setPayload(profileUserVO);
            return ResponseEntity
                    .status(HttpStatus.OK)
                    .body(response);
        } catch (ApplicationException e) {
            log.error("Decodifica: Errore Login", e);
            throw new ApplicationException("Errore durante la decodifica del token",e);
        }
    }

    private String getIdClientFromCookie() {

        String idClient = null;
        String cookieHeader = headerInterceptor.getHeaders().getFirst("Cookie");
        if (cookieHeader != null) {
            String[] cookies = cookieHeader.split("; ");
            for (String cookie : cookies) {
                if (cookie.startsWith("idClient=")) {
                    idClient = cookie.substring("idClient=".length());
                    break;
                }
            }
        }
        return idClient;

    }

}
