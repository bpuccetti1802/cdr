package it.sistinf.romacapitale.auth.api;

import it.sistinf.romacapitale.auth.interceptor.HeaderInterceptor;
import it.sistinf.romacapitale.core.api.AbstractSqlAPI;
import it.sistinf.romacapitale.core.dto.ResponseDTO;
import it.sistinf.romacapitale.core.exceptions.ApplicationException;
import it.sistinf.romacapitale.core.exceptions.TokenExpiredException;
import it.sistinf.romacapitale.core.messages.EnumMessage;
import it.sistinf.romacapitale.integration.management.vo.IdTokenDecodificato;
import it.sistinf.romacapitale.integration.management.vo.ProfileUserVO;
import jakarta.servlet.http.Cookie;
import jakarta.servlet.http.HttpServletRequest;
import lombok.NoArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.jose4j.jwk.PublicJsonWebKey;
import org.jose4j.jwk.RsaJsonWebKey;
import org.jose4j.jwt.JwtClaims;
import org.jose4j.jwt.MalformedClaimException;
import org.jose4j.jwt.consumer.InvalidJwtException;
import org.jose4j.jwt.consumer.JwtConsumer;
import org.jose4j.jwt.consumer.JwtConsumerBuilder;
import org.jose4j.lang.JoseException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseCookie;
import org.springframework.http.ResponseEntity;
import org.springframework.web.context.request.RequestContextHolder;
import org.springframework.web.context.request.ServletRequestAttributes;
import org.springframework.web.servlet.support.ServletUriComponentsBuilder;

import java.security.interfaces.RSAPublicKey;
import java.util.Arrays;
import java.util.Collections;
import java.util.Map;
import java.util.stream.Collectors;

@Slf4j
@NoArgsConstructor(force = true)
public class AbstractLoginApi extends AbstractSqlAPI {

    @Value("${auth.relative.path}")
    private final String authRelativePath;

    @Value("${auth.logoff.path}")
    private final String authLogoffPath;

    @Value("${auth.cookie.secure}")
    private final Boolean cookieSecure;

    @Value("${auth.cookie.domain}")
    private final String cookieDomain;

    @Value("${auth.cookie.samesite}")
    private String cookieSamesite;

    @Value("${jwt.iam.key}")
    private String iamJwtKey;

    @Autowired
    protected HeaderInterceptor headerInterceptor;

    @Autowired
    private HttpServletRequest request;

    private String callerBaseUrl;
    private String protocol;

    protected ResponseEntity<ResponseDTO<ProfileUserVO>> cleanAllCookies(ResponseDTO<ProfileUserVO> response, Boolean logoff) {
        HttpHeaders newHeaders = new HttpHeaders();
        String targetDomain= cookieDomain;
        Map<String, String> cookies = parseCookiesFromHeaders();
        if (cookies != null && !cookies.isEmpty()) {
            getCallerBaseUrl();

            for (Map.Entry<String, String> entry : cookies.entrySet()) {
                if (cookies.containsKey("ssoprecomune") || cookies.containsKey("ssocomune")) { //cookie IAM in preprod e prod
                    log.info("Logout - Trovato cookie di accesso ad IAM ");
                    //logout da accesso IAM
                    targetDomain = ".comune.roma.it";
                    //TODO capire come gestire endSession IAM
                }
                if (entry.getKey().equals("idClient") || entry.getKey().equals("Bearer") || entry.getKey().equals("useHomeUri")  || entry.getKey().equals("ssoprecomune") || entry.getKey().equals("ssocomune")) {
                    ResponseCookie cookie = ResponseCookie.from(entry.getKey(), "")
                            .httpOnly(true)
                            .secure(Boolean.TRUE.equals(cookieSecure))
                            .domain(targetDomain)
                            .sameSite(cookieSamesite)
                            .path("/")
                            .maxAge(0)
                            .build();

                    newHeaders.add(HttpHeaders.SET_COOKIE, String.valueOf(cookie));
                }
            }
        }
        // Recupero la request e l'header Referer
        ServletRequestAttributes sra = (ServletRequestAttributes) RequestContextHolder.getRequestAttributes();
        HttpServletRequest request = (sra != null) ? sra.getRequest() : null;

        if (logoff) {
            String targetUrl = (request != null) ? request.getHeader("Referer") : null;
            //se il Referer è vuoto, costruiamo l'URL base
            if (targetUrl == null || targetUrl.isEmpty()) {
                targetUrl = ServletUriComponentsBuilder.fromCurrentContextPath().toUriString();
            }
            newHeaders.add(HttpHeaders.LOCATION, targetUrl);
//            log.info("Headers Set Cookie inviati dal backend per logout: {}", newHeaders.get(HttpHeaders.SET_COOKIE));
//            newHeaders.add(HttpHeaders.LOCATION, protocol + "://" + callerBaseUrl + authLogoffPath);
            return ResponseEntity
                    .status(HttpStatus.FOUND)
                    .headers(newHeaders)
                    .body(null);
        }
        return ResponseEntity
                .status(HttpStatus.OK)
                .headers(newHeaders)
                .body(response);

    }

    private Map<String, String> parseCookiesFromHeaders() {
        ServletRequestAttributes sra = (ServletRequestAttributes) RequestContextHolder.getRequestAttributes();
        if (sra == null) return Collections.emptyMap();

        HttpServletRequest request = sra.getRequest();
        Cookie[] rawCookies = request.getCookies();

        if (rawCookies == null) {
            return Collections.emptyMap();
        }


        return Arrays.stream(rawCookies)
                .collect(Collectors.toMap(
                        Cookie::getName,
                        Cookie::getValue,
                        (v1, v2) -> v1 // In caso di duplicati, tiene il primo
                ));
    }

    private void getCallerBaseUrl() {
        // Ottieni gli attributi della richiesta dal RequestContextHolder
        ServletRequestAttributes sra = (ServletRequestAttributes) RequestContextHolder.getRequestAttributes();

        if (sra == null) {
            throw new ApplicationException(EnumMessage.INTERNAL_ERROR);
        }

        HttpServletRequest currentRequest = sra.getRequest();

        // Logica per determinare il basePath dinamico
        callerBaseUrl = currentRequest.getHeader("X-Forwarded-Host");
        if (callerBaseUrl == null || callerBaseUrl.isEmpty()) {
            callerBaseUrl = currentRequest.getServerName();
        }

        // Recupera il protocollo (http o https)
        protocol = currentRequest.getHeader("X-Forwarded-Proto");
        if (protocol == null || protocol.isEmpty()) {
            protocol = currentRequest.getScheme();
        }
    }


    public IdTokenDecodificato consumeTokenIAM(String jwtToken) {
        try {
            RsaJsonWebKey rsaJsonWebKey = new RsaJsonWebKey(
                    (RSAPublicKey) PublicJsonWebKey.Factory.newPublicJwk(iamJwtKey).getPublicKey());

            JwtConsumer consumer = new JwtConsumerBuilder().setVerificationKey(rsaJsonWebKey.getKey())
                    .setSkipDefaultAudienceValidation() // salta controllo audience
                    .setRequireExpirationTime()         // Verifica sempre la scadenza
                    .setAllowedClockSkewInSeconds(30)   // Tolleranza per sfasamento time
                    .build();
            JwtClaims claims = consumer.processToClaims(jwtToken);
            return mapClaimsToIdToken(claims);
        } catch (InvalidJwtException | JoseException | MalformedClaimException e) {
            throw new TokenExpiredException(e);
        }
    }

    public IdTokenDecodificato mapClaimsToIdToken(JwtClaims claims) throws MalformedClaimException {
        IdTokenDecodificato idTokenDecodificato = new IdTokenDecodificato();

        // Campi String
        idTokenDecodificato.setSub(claims.getSubject());
        idTokenDecodificato.setIss(claims.getIssuer());
        idTokenDecodificato.setAzp(claims.getStringClaimValue("azp"));
        idTokenDecodificato.setNonce(claims.getStringClaimValue("nonce"));
        idTokenDecodificato.setAt_hash(claims.getStringClaimValue("at_hash"));
        idTokenDecodificato.setC_hash(claims.getStringClaimValue("c_hash"));
        idTokenDecodificato.setAud(claims.getStringClaimValue("aud"));

        // Campi temporali in secondi (long)
        idTokenDecodificato.setExp(claims.getExpirationTime().getValue());
        idTokenDecodificato.setIat(claims.getIssuedAt().getValue());

        // AuthTime è  un intero
        Long authTime = claims.getNumericDateClaimValue("auth:time").getValue();
        idTokenDecodificato.setAuthTime(authTime != null ? authTime.intValue() : 0);

        //Claims IAM
        idTokenDecodificato.setIv_tipoutente(claims.getStringClaimValue("iv_tipoutente"));
        idTokenDecodificato.setRealm(claims.getStringClaimValue("realm"));
        idTokenDecodificato.setTokenName(claims.getStringClaimValue("tokenName"));
        idTokenDecodificato.setAuditTrackingId(claims.getStringClaimValue("auditTrackingId"));
        idTokenDecodificato.setOrgForgerockOpenidconnectOps(claims.getStringClaimValue("org.forgerock.openidconnect.ops"));
        idTokenDecodificato.setTokenType(claims.getStringClaimValue("tokenType"));

        return idTokenDecodificato;
    }

    protected ResponseEntity<ResponseDTO<ProfileUserVO>> cleanLocalCookies(ResponseDTO<ProfileUserVO> response, Boolean logoff) {
        HttpHeaders newHeaders = new HttpHeaders();
        String targetDomain= cookieDomain;
        String redirectUrl = "";
        Map<String, String> cookies = parseCookiesFromHeaders();
        if (cookies != null && !cookies.isEmpty()) {
            getCallerBaseUrl();

            for (Map.Entry<String, String> entry : cookies.entrySet()) {
                if (cookies.containsKey("ssocomune")) { //cookie IAM
                    redirectUrl = "https://comune.roma.it/web/it/pagina-personale.page"; //redirect sulla pagina personale prod
                    targetDomain = ".comune.roma.it";
                } else if (cookies.containsKey("ssoprecomune")) {
                    redirectUrl = "https://preprod.comune.roma.it/web/it/pagina-personale.page"; //redirect sulla pagina personale preprod
                    targetDomain = ".comune.roma.it";
                }
                if (entry.getKey().equals("idClient") || entry.getKey().equals("Bearer") || entry.getKey().equals("useHomeUri")) {
                    ResponseCookie cookie = ResponseCookie.from(entry.getKey(), "")
                            .httpOnly(true)
                            .secure(Boolean.TRUE.equals(cookieSecure))
                            .domain(targetDomain)
                            .sameSite(cookieSamesite)
                            .path("/")
                            .maxAge(0)
                            .build();

                    newHeaders.add(HttpHeaders.SET_COOKIE, String.valueOf(cookie));
                }
            }
        }
        // Recupero la request e l'header Referer
        ServletRequestAttributes sra = (ServletRequestAttributes) RequestContextHolder.getRequestAttributes();
        HttpServletRequest request = (sra != null) ? sra.getRequest() : null;

        if (logoff) {
//            String targetUrl = (request != null) ? request.getHeader("Referer") : null;
//            //se il Referer è vuoto, costruiamo l'URL base
//            if (targetUrl == null || targetUrl.isEmpty()) {
//                targetUrl = ServletUriComponentsBuilder.fromCurrentContextPath().toUriString();
//            }
            newHeaders.add(HttpHeaders.LOCATION, redirectUrl);
            return ResponseEntity
                    .status(HttpStatus.FOUND)
                    .headers(newHeaders)
                    .body(null);
        }
        return ResponseEntity
                .status(HttpStatus.OK)
                .headers(newHeaders)
                .body(response);

    }

}
