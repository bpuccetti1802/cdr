package it.sistinf.romacapitale.servicemesh.filters;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.DeserializationFeature;
import com.fasterxml.jackson.databind.ObjectMapper;
import io.micrometer.core.instrument.Counter;
import io.micrometer.core.instrument.Metrics;
import it.sistinf.romacapitale.core.dto.RequestDTO;
import it.sistinf.romacapitale.core.dto.RequestHeader;
import it.sistinf.romacapitale.core.filters.CachedBodyHttpServletRequest;
import it.sistinf.romacapitale.core.filters.ResponseCaptureWrapper;
import it.sistinf.romacapitale.core.security.CurrentUser;
import it.sistinf.romacapitale.core.utils.DateUtils;
import it.sistinf.romacapitale.core.utils.ObjectMapperFactory;
import jakarta.servlet.*;
import jakarta.servlet.http.Cookie;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import lombok.extern.slf4j.Slf4j;
import org.jose4j.json.internal.json_simple.JSONObject;
import org.slf4j.MDC;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.MediaType;
import org.springframework.jmx.export.annotation.ManagedMetric;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;

import java.io.IOException;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import java.sql.Timestamp;
import java.text.SimpleDateFormat;
import java.time.ZoneId;
import java.time.ZonedDateTime;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.CompletableFuture;

@Slf4j
@Component("GeneralFilterServiceMesh")
public class GeneralFilterServiceMesh implements Filter {

    @Value("${accountability.internal.url}")
    private String locationAPI;

    private Counter numeroChiamateErrore;

    private static final String API_ENDPOINT = "/audit/";

    @Override
    @ManagedMetric
    public void init(FilterConfig filterConfig) throws ServletException {
        this.numeroChiamateErrore = Counter.builder("audit.write.errors")
                .description("Contatore delle chiamate in errore")
                .register(Metrics.globalRegistry);
    }

    @Override
    public void doFilter(ServletRequest servletRequest, ServletResponse servletResponse, FilterChain filterChain) throws IOException, ServletException {
        //timer request
        //accountability request
        //gestire idRequest in MDC

        String idRequest = UUID.randomUUID().toString();
        String cdAmbito = "";
        String cdApplicazione = "";

        HttpServletRequest request = (HttpServletRequest) servletRequest;
        String authorization = request.getHeader(HttpHeaders.AUTHORIZATION);
//        log.info("GeneralFilter: authorization = "+authorization);

        if (request.getContentType() == null || !request.getContentType().startsWith("multipart/form-data")) {
            request = new CachedBodyHttpServletRequest(request);

            String JSON = getEntityBody(request);

            ObjectMapper objectMapper = ObjectMapperFactory.getInstance().getSimpleObjectMapper();
            objectMapper.configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false);

            RequestDTO requestBody;

            try {
                requestBody = objectMapper.readValue(JSON, RequestDTO.class);
                RequestHeader header = (RequestHeader) requestBody.getHeader();
                if(header.getIdRequest() != null) {
                    idRequest = header.getIdRequest().toString();
                }
                if(header.getCdAmbito() != null) {
                    cdAmbito = header.getCdAmbito();
                }
                if(header.getCdApplicazione() != null) {
                    cdApplicazione = header.getCdApplicazione();
                }
            } catch(Exception ignored) {
            }
        }

        //Per risalire all'endpoint del servizio
        request.getContextPath();

        //Ce li ho nell'header
        MDC.put("idRequest", idRequest);
        MDC.put("cdAmbito", cdAmbito);
        MDC.put("cdApplicazione", cdApplicazione);


        String path = request.getRequestURI();
        /*if (path.contains("/swagger")) {
            //Se viene chiamato l'endpoint di swagger non vengono chiamati ResponseCaptureWrapper e il filtro di audit (la riscrittura della response causa errori)
            filterChain.doFilter(request, servletResponse);
        }else{*/
            HttpServletResponse response = (HttpServletResponse) servletResponse;
            ResponseCaptureWrapper responseCaptureWrapper = new ResponseCaptureWrapper(response);

            filterChain.doFilter(request, response);

            //filterChain.doFilter(request, responseCaptureWrapper);

            //filter(request, servletResponse, responseCaptureWrapper);

        //}

        //response 403
        //aggiungere headers per la sicurezza
        //accountability response
        //timer response
    }

    public void filter(ServletRequest servletRequest, ServletResponse servletResponse, ResponseCaptureWrapper responseCaptureWrapper) throws IOException {
        HttpServletRequest request = (HttpServletRequest) servletRequest;

        String contentType = responseCaptureWrapper.getContentType();
        if (contentType != null && !contentType.startsWith("application/json")) {
            servletResponse.getOutputStream().write(responseCaptureWrapper.getCaptureAsBytes());

        } else {

            String responseBody = new String(responseCaptureWrapper.getCaptureAsBytes(), StandardCharsets.UTF_8);

            servletResponse.getWriter().write(responseBody);

            if (responseBody.isBlank()) {
                return;
            }

            try {
                ObjectMapper objectMapper = ObjectMapperFactory.getInstance().getSimpleObjectMapper();

                Map<Object, Object> payloadMap = objectMapper.readValue(responseBody, new TypeReference<>() {
                });
                Map<Object, Object> responseMap = new HashMap<>();
                responseMap.put("payload", payloadMap);
                request.setAttribute("responseMap", responseMap);
            } catch (Exception e) {
                log.error("Error parsing response body", e);
                return;
            }
        }

        String requestContent = getEntityBody(request);
        request.setAttribute("reqBody", requestContent);

        Cookie[] cookies = request.getCookies();
        Cookie cookieBearer = getCookie(cookies, "Bearer");

        if (cookieBearer != null) {
            String path = request.getRequestURI();
            if (path.contains("/internal/") || path.contains("/login")) {
                return;
            }

//            Map<Object, Object> responseMap = (HashMap<Object, Object>) request.getAttribute("responseMap");
//            if(responseMap != null) {
//                Map<Object, Object> payloadFatherMap = (Map<Object, Object>) responseMap.get("payload");
//                Map<Object, Object> summaryMap = (Map<Object, Object>) payloadFatherMap.get("summary");

//                boolean isError = summaryMap != null && (boolean) summaryMap.get("error");
				//Messo il blocco per la chiamata a Audit
//				isError=true;
				//
//                if (!isError) {
//                    CurrentUser cu = getCurrentUser();
//                    JSONObject jsonReqNew = buildAuditRequest(request, path, cu);
//
//                    try {
//                        ObjectMapper objectMapper = ObjectMapperFactory.getInstance().getSimpleObjectMapper();
//                        objectMapper.setDateFormat(new SimpleDateFormat(DateUtils.DATE_TIME_FORMAT));
//
//                        String queryParamsString = objectMapper.writeValueAsString(request.getParameterMap());
//                        String reqBodyStr = (String) request.getAttribute("reqBody");
//
//                        jsonReqNew.put("request", reqBodyStr.isEmpty() ? queryParamsString : reqBodyStr);
//                        jsonReqNew.put("response", objectMapper.writeValueAsString(responseMap.get("payload")));
//
//                        HttpHeaders headers = new HttpHeaders();
//                        headers.setContentType(MediaType.APPLICATION_JSON);
//                        headers.add(HttpHeaders.AUTHORIZATION, cookieBearer.getName() + "=" + cookieBearer.getValue());
//
//                        HttpEntity<String> entity = new HttpEntity<>(jsonReqNew.toString(), headers);
//                        RestTemplate restTemplate = new RestTemplate();
//
////                        log.info("Request Headers: ", headers);
////                        log.info("Request Body: ", jsonReqNew.toString());
////                        log.info("Full URL: ", locationAPI + API_ENDPOINT);
//
//                        CompletableFuture<Void> future = CompletableFuture.runAsync(() -> {
//                            restTemplate.exchange(locationAPI + API_ENDPOINT, HttpMethod.POST, entity, String.class);
//                        });
//
//                        future.join();
//                    } catch (Exception e) {
//                        log.error("Errore filtro di audit", e);
//                        numeroChiamateErrore.increment();
//                    }
//                } else {
//                    // response in errore
//                }
//            }
        } else {
            // cookie non presente
        }
    }

//    private JSONObject buildAuditRequest(HttpServletRequest request, String path, CurrentUser cu) {
//        JSONObject jsonReqNew = new JSONObject();
//        jsonReqNew.put("uri", path);
//        jsonReqNew.put("httpMethod", request.getMethod());
//        jsonReqNew.put("username", cu.getUsername());
//        jsonReqNew.put("idProfilo", cu.getIdProfilo());
//        jsonReqNew.put("codiceFiscale", cu.getCodiceFiscale());
//        //jsonReqNew.put("idProgramma", cu.getIdProgramma());
////        jsonReqNew.put("idGruppo", cu.getIdGruppo());
//        //jsonReqNew.put("codiceRegione", cu.getCdRegione());
//
//        ZoneId zoneId = ZoneId.of("Etc/UTC");
//        ZonedDateTime dateTime = ZonedDateTime.ofInstant(
//                new Timestamp(System.currentTimeMillis()).toInstant(),
//                zoneId
//        );
//
//        jsonReqNew.put("timestampOperazione", dateTime.toLocalDateTime().toString());
//
//        return jsonReqNew;
//    }

    private Cookie getCookie(Cookie[] cookies, String name) {
        if (cookies != null) {
            for (Cookie cookie : cookies) {
                if (name.equals(cookie.getName())) {
                    return cookie;
                }
            }
        }
        return null;
    }

    private String getEntityBody(HttpServletRequest request) {
        try (InputStream in = request.getInputStream()) {
            byte[] requestEntity = in.readAllBytes();
            return (requestEntity.length == 0) ? "" : new String(requestEntity, StandardCharsets.UTF_8);
        } catch (IOException e) {
            log.error("Error reading request body", e);
            return null;
        }
    }

    protected CurrentUser getCurrentUser() {
        Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
        return (authentication != null) ? (CurrentUser) authentication.getDetails() : null;
    }
}
