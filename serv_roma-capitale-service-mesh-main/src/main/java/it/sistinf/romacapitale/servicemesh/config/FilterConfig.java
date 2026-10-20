package it.sistinf.romacapitale.servicemesh.config;

import it.sistinf.romacapitale.core.filters.GeneralFilter;
import it.sistinf.romacapitale.servicemesh.filters.AuthenticationFilter;
import org.springframework.boot.web.servlet.FilterRegistrationBean;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class FilterConfig {

    @Bean
    public FilterRegistrationBean<GeneralFilter> generalFilterRegistration(GeneralFilter filter) {
        FilterRegistrationBean<GeneralFilter> registration = new FilterRegistrationBean<>(filter);
        // Disabilita l'attivazione del filtro
        registration.setEnabled(false);
        return registration;
    }
}