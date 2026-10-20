package it.sistinf.romacapitale.servicemesh.api;

import io.swagger.v3.oas.annotations.Operation;
import it.sistinf.romacapitale.core.dto.ResponseDTO;
import it.sistinf.romacapitale.core.security.CurrentUser;
import it.sistinf.romacapitale.core.security.JwtManager;
import it.sistinf.romacapitale.integration.management.vo.ApplicazioneVO;
import it.sistinf.romacapitale.servicemesh.domain.ForwardDomain;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import lombok.AllArgsConstructor;
import lombok.NoArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.*;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.HttpStatusCodeException;
import org.springframework.web.client.RestTemplate;

import java.io.IOException;
import java.io.InputStream;
import java.net.URI;
import java.nio.charset.StandardCharsets;
import java.util.Collections;
import java.util.function.Function;
import java.util.stream.Collectors;

@Slf4j
@RestController
@AllArgsConstructor
@RequestMapping("/")
public class ForwardV1 {

    private final ForwardDomain forwardDomain;

    @Operation(summary = "Chiama un servizio internal", description = "Chiama il servizio internal e ritorna la risposta")
    @RequestMapping(value = "{serviceContextRoot}/**",produces = "application/json")
    public void serviceMesh(
            @PathVariable String serviceContextRoot,
            HttpServletRequest request, HttpServletResponse response
    ) {

        forwardDomain.forwardServiceMesh(serviceContextRoot, request, response, true);
    }

    @Operation(summary = "Chiama un servizio external", description = "Chiama il servizio external e ritorna la risposta")
    @RequestMapping(value = "internal/{serviceContextRoot}/**",produces = "application/json")
    public void serviceMeshInternal(
            @PathVariable String serviceContextRoot,
            HttpServletRequest request, HttpServletResponse response
    ) {

        forwardDomain.forwardServiceMesh(serviceContextRoot, request, response, false);
    }
}
