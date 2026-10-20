package it.sistinf.romacapitale.management.config;

import it.sistinf.romacapitale.core.config.DiagnosticProperties;
import it.sistinf.romacapitale.core.domain.diagnostico.DiagnosticoService;
import it.sistinf.romacapitale.core.exceptions.GlobalExceptionHandler;
import lombok.AllArgsConstructor;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
@EnableConfigurationProperties(DiagnosticProperties.class)
@AllArgsConstructor
public class ExceptionHandlerConfig {

    private final DiagnosticoService diagnosticoService;
    private final DiagnosticProperties diagnosticProperties;

    @Bean
    public GlobalExceptionHandler globalExceptionHandler() {
        return new GlobalExceptionHandler(diagnosticoService, diagnosticProperties);
        //
    }
}