package it.sistinf.romacapitale.servicemesh.domain;

import it.sistinf.romacapitale.core.domain.AbstractDomain;
import it.sistinf.romacapitale.core.dto.ResponseDTO;
import it.sistinf.romacapitale.core.exceptions.TokenExpiredException;
import it.sistinf.romacapitale.core.security.CurrentUser;
import it.sistinf.romacapitale.core.security.JwtManager;
import it.sistinf.romacapitale.integration.auth.api.LoginUtenteTecnicoClient;
import it.sistinf.romacapitale.integration.auth.vo.InputLoginUtenteTecnicoVO;
import it.sistinf.romacapitale.integration.auth.vo.UtenteTecnicoVO;
import it.sistinf.romacapitale.integration.management.vo.ApplicazioneVO;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.slf4j.MDC;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.http.server.ServletServerHttpRequest;
import org.springframework.stereotype.Service;
import org.springframework.web.client.HttpStatusCodeException;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.multipart.MultipartHttpServletRequest;
import org.springframework.web.util.UriComponentsBuilder;

import javax.naming.AuthenticationException;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.URI;
import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;
import java.util.Collections;
import java.util.Optional;
import java.util.function.Function;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
@Slf4j
public class ForwardDomain extends AbstractDomain {

    @Value("${cdAmbito}")
    private String cdAmbito;

    @Value("${cdApplicazione}")
    private String cdApplicazione;

    @Value("${cd.cloud:}")
    private String cdCloud;

    @Value("${management.internal.url:}")
    private String managementInternalUrl;

    @Value("${auth.endpoint.url:}")
    private String authEndpointUrl;

    @Value("${management.external.url:}")
    private String managementEndpointUrl;

    @Value("${service-mesh.1.endpoint.url:}")
    private String serviceMesh1EndpointUrl;

    @Value("${service-mesh.2.endpoint.url:}")
    private String serviceMesh2EndpointUrl;

    @Autowired
    private RestTemplate restTemplate;

    @Autowired
    @Qualifier("restTemplateExternal")
    private RestTemplate externalRestTemplate;

    @Autowired
    @Qualifier("restTemplateInternal")
    private RestTemplate internalRestTemplate;

    @Autowired
    private JwtManager jwtManager;

    private final LoginUtenteTecnicoClient loginUtenteTecnicoClient;

    private final String AUTHORIZATION_2 = "Authorization-2";

    public void forwardServiceMesh(String serviceContextRoot,
                                     HttpServletRequest request, HttpServletResponse response, boolean external) {
        log.info("serviceMesh: cdCloud = "+cdCloud);
        log.info("serviceMesh: authEndpointUrl = "+authEndpointUrl);
        log.info("serviceMesh: managementEndpointUrl = "+managementEndpointUrl);
        log.info("serviceMesh: serviceMesh1EndpointUrl = "+serviceMesh1EndpointUrl);
        log.info("serviceMesh: serviceMesh2EndpointUrl = "+serviceMesh2EndpointUrl);

        HttpHeaders httpHeaders = new ServletServerHttpRequest(request).getHeaders();

        String token = null;
        try {
            token = getToken(httpHeaders);
        } catch (TokenExpiredException | AuthenticationException e) {
            if (external) {
                handleUnauthorized(response, e);
                return;
            }
            token = getServiceMeshToken();
        }

        if (external) {
            if (!httpHeaders.containsKey(HttpHeaders.AUTHORIZATION)) {
                httpHeaders.add(HttpHeaders.AUTHORIZATION, "Bearer " + token);
            }
            httpHeaders.remove(AUTHORIZATION_2);
        } else {
            if (!httpHeaders.containsKey(AUTHORIZATION_2)) {
                httpHeaders.add(AUTHORIZATION_2, "Bearer " + token);
            }
        }

        //Discovery dal contextroot risalire all'endpoint del servizio. possiamo usare la cache
        HttpHeaders headers1 = new HttpHeaders();
//        headers1.setBearerAuth(token);
        HttpEntity<String> requestEntity = new HttpEntity<>(headers1);
        ParameterizedTypeReference<ResponseDTO<ApplicazioneVO>> responseType = new ParameterizedTypeReference<>() {};

        String endpoint;

        String serviceMeshEndpoint = null;

        boolean internalCall = false;

        //Le url degli altri service mesh vanno nel configMap roma-capitale-env
        //Management e Auth sono dei casi particolari, le url vanno prese dal configmap roma-capitale-env
        if("roma-capitale-service-management".equalsIgnoreCase(serviceContextRoot)){
            endpoint = managementEndpointUrl;
        }else if("roma-capitale-service-auth".equalsIgnoreCase(serviceContextRoot)){
            endpoint = authEndpointUrl;
        }else {
            ResponseEntity<ResponseDTO<ApplicazioneVO>> responseEntity = internalRestTemplate.exchange(managementInternalUrl +"/applicazione/context-root/"+serviceContextRoot,
                    HttpMethod.GET, requestEntity, responseType);

            if (responseEntity.getBody() == null || responseEntity.getBody().getPayload() == null) {
                log.error("Applicazione non trovata per context root: " + serviceContextRoot);
                response.setStatus(HttpServletResponse.SC_BAD_REQUEST);
                response.setContentType("text/plain;charset=UTF-8");
                try {
                    response.getWriter().write("Applicazione non trovata per context root: " + serviceContextRoot);
                    response.getWriter().flush();
                } catch (IOException e) {
                    log.error("Errore durante la scrittura della risposta di errore", e);
                }
                return;
            }

            String cdCloudServizio = responseEntity.getBody().getPayload().getCdCloud();
            //Se la chiamata è interna si usa sempre ds_endpoint, invece se è esterna sempre quella del service mesh di riferimento
            //Se cdCloud del servizio da richiamare = 1 e cdCloud = 1 allora uso la url interna ad ecaas(ds_endpoint)
            //Se cdCloud del servizio da richiamare = 2 e cdCloud = 1 allora uso la url del service mesh su rancher(2)
            //Se cdCloud del servizio da richiamare = 1 e cdCloud = 2 allora uso la url del service mesh su ecaas(1)
            //Se cdCloud del servizio da richiamare = 2 e cdCloud = 2 allora uso la url interna a rancher(ds_endpoint)

            if("1".equalsIgnoreCase(cdCloudServizio) &&
                    "2".equalsIgnoreCase(cdCloud)){
                //Se cdCloud del servizio da richiamare = 1 e cdCloud = 2 allora uso la url del service mesh su ecaas(1)
                endpoint = serviceMesh1EndpointUrl + request.getRequestURI().replaceFirst("/internal", "");
                serviceMeshEndpoint = URI.create(serviceMesh1EndpointUrl).getHost();
            }else if("2".equalsIgnoreCase(cdCloudServizio) &&
                    "1".equalsIgnoreCase(cdCloud)){
                //Se cdCloud del servizio da richiamare = 2 e cdCloud = 1 allora uso la url del service mesh su rancher(2)
                endpoint = serviceMesh2EndpointUrl + request.getRequestURI().replaceFirst("/internal", "");
                serviceMeshEndpoint = URI.create(serviceMesh2EndpointUrl).getHost();
            }else{
                //Se cdCloud del servizio da richiamare = cdCloud
                endpoint = request.getRequestURI().replace("/" + serviceContextRoot, responseEntity.getBody().getPayload().getDsEndpoint());
                internalCall = true;
            }

        }

        //Reverse proxy
        long startTime = System.currentTimeMillis();

        if (serviceMeshEndpoint != null) {
            httpHeaders.set(HttpHeaders.HOST, serviceMeshEndpoint);
            httpHeaders.set("X-Forwarded-Host", serviceMeshEndpoint);
        }

        String forwardUrl = endpoint + (request.getQueryString() != null ? "?"+request.getQueryString() : "");

        log.info("forwardUrl = "+ forwardUrl);

        final String EKAAS = "ekaas";
        final String ECAAS = "ecaas";

        RestTemplate restTemplate = internalCall && !forwardUrl.contains(EKAAS) && !forwardUrl.contains(ECAAS) ? internalRestTemplate : externalRestTemplate;

        String contentType = request.getContentType();

        try {
            restTemplate.execute(forwardUrl, HttpMethod.valueOf(request.getMethod()), (clientRequest) -> {
                for (String headerName : httpHeaders.keySet()) {
                    if (HttpHeaders.COOKIE.equalsIgnoreCase(headerName) ||
                        HttpHeaders.HOST.equalsIgnoreCase(headerName) ||
                        HttpHeaders.ORIGIN.equalsIgnoreCase(headerName) ||
                        "Referer".equalsIgnoreCase(headerName)) {
                        continue;
                    }
                    for (String headerValue : httpHeaders.get(headerName)) {
                            clientRequest.getHeaders().add(headerName, headerValue);
                    }
                }
                if (contentType != null) {
                    clientRequest.getHeaders().set(HttpHeaders.CONTENT_TYPE, contentType);
                }

                httpHeaders.remove(HttpHeaders.CONTENT_LENGTH);

                try (InputStream is = request.getInputStream();
                     OutputStream os = clientRequest.getBody()) {
                    is.transferTo(os);
                    os.flush();
                }
            }, (clientResponse) -> {
                response.setStatus(clientResponse.getStatusCode().value());
                clientResponse.getHeaders().forEach((headerName, headerValues) -> {
                    if (!"Connection".equals(headerName) && !"Transfer-Encoding".equals(headerName)) {
                        boolean first = true;
                        for (String value : headerValues) {
                            if (first) {
                                response.setHeader(headerName, value);
                                first = false;
                            } else {
                                response.addHeader(headerName, value);
                            }
                        }
                    }
                });

                try (InputStream is = clientResponse.getBody();
                     OutputStream os = response.getOutputStream()) {
                    byte[] buffer = new byte[8192];
                    int read;
                    while ((read = is.read(buffer)) != -1) {
                        os.write(buffer, 0, read);
                        os.flush();
                    }
                    os.flush();
                } catch (IOException e) {
                    log.error("Errore durante il proxy dello stream: ", e);
                    throw e;
                }
                return null;
            });
        } catch (HttpStatusCodeException e) {
            log.error("--- ERRORE CHIAMATA HTTP ---");
            log.error("URL: {} {}", request.getMethod(), forwardUrl);
            log.error("Status Code: {}", e.getStatusCode());
            log.error("Status Text: {}", e.getStatusText());
            log.error("Response Body: {}", e.getResponseBodyAsString());
            log.error("Headers Ricevuti: {}", e.getResponseHeaders());
            throw e;
        } catch (Exception e) {
            log.error("Errore generico durante il forward verso {}: {}", forwardUrl, e.getMessage(), e);
            throw e;
        }
        long duration = System.currentTimeMillis() - startTime;
        log.info("The request took " + duration + " ms");
        log.info("Response Status = " + response.getStatus());
        log.info("Headers Ricevuti: {}", response.getHeaderNames().stream().map(h -> h + "=" + response.getHeaders(h)).collect(Collectors.joining(", ")));

    }

    private byte[] getEntityBody(HttpServletRequest request) {
        try (InputStream in = request.getInputStream()) {
            return in.readAllBytes();
        } catch (IOException e) {
            log.error("Error reading request body", e);
            return new byte[0];
        }
    }

    private String changeFlagTokenReduced(String token) {
        try {
            CurrentUser currentUser = jwtManager.consumeToken(token);
            currentUser.setFlagTokenReduced("N");
            return jwtManager.createToken(currentUser);
        } catch (Exception e) {
            log.error("Errore change flagTokenReduced", e);
            return token;
        }
    }

    private String getToken(HttpHeaders httpHeaders) throws TokenExpiredException, AuthenticationException {
        String[] targetHeaders = {HttpHeaders.AUTHORIZATION, AUTHORIZATION_2};

        for (String headerName : targetHeaders) {
            String rawValue = httpHeaders.getFirst(headerName);

            if (rawValue != null && rawValue.startsWith("Bearer ")) {
                String jwt = rawValue.substring(7);
                try {
                    CurrentUser user = jwtManager.consumeToken(jwt);

                    String finalToken = jwt;
                    if ("S".equalsIgnoreCase(user.getFlagTokenReduced())) {
                        finalToken = changeFlagTokenReduced(jwt);

                        httpHeaders.set(headerName, "Bearer " + finalToken);
                    }
                    return finalToken;
                } catch (TokenExpiredException ignored) {
                }
            }
        }

        throw new AuthenticationException("Nessun token valido trovato");
    }

    private String getServiceMeshToken() {
        try {
            MDC.put("cdAmbito", cdAmbito);
            MDC.put("cdApplicazione", cdApplicazione);

            InputLoginUtenteTecnicoVO input = new InputLoginUtenteTecnicoVO("SERVICE-MESH");
            return loginUtenteTecnicoClient.loginUtenteTecnico(makeRequestDTO(input))
                    .getPayload()
                    .getToken();
        } finally {
            MDC.remove("cdAmbito");
            MDC.remove("cdApplicazione");
        }
    }

    private void handleUnauthorized(HttpServletResponse response, Exception ex) {
        response.setStatus(HttpServletResponse.SC_UNAUTHORIZED);
        response.setContentType("text/plain;charset=UTF-8");
        try {
            response.getWriter().write(ex.getMessage());
            response.getWriter().flush();
        } catch (IOException e) {
            log.error("Errore durante la scrittura dell'unauthorized", e);
        }
    }
}
