package it.sistinf.romacapitale.auth.config;

import it.sistinf.romacapitale.core.security.AuthenticationFilter;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.method.configuration.EnableGlobalMethodSecurity;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.core.GrantedAuthorityDefaults;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;
import org.springframework.web.cors.CorsConfiguration;
import org.springframework.web.cors.CorsConfigurationSource;
import org.springframework.web.cors.UrlBasedCorsConfigurationSource;

import java.util.ArrayList;
import java.util.List;

@Configuration
@EnableWebSecurity
@EnableGlobalMethodSecurity(securedEnabled = true)
@RequiredArgsConstructor
public class SecurityConfiguration {

    private final AuthenticationFilter authenticationFilter;

    @Value("${cors.configuration}")
    private String corsPolicies;

    @Value("${cors.pattern.configuration}")
    private String corsPoliciesPatterns;

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity httpSecurity) throws Exception {

        List<String> publicUrls = List.of("/api/v1/autenticazione");

        authenticationFilter.setPublicUrls(publicUrls);

        return httpSecurity
                .cors(cors -> cors.configurationSource(authCorsConfigurationSource())) //abilitazione config CORS compatibile con callbacks OIDC
                .csrf(csrf -> csrf.disable())
                .authorizeHttpRequests(auth -> auth
                        .requestMatchers("/api/v1/autenticazione/**",
                        "/api/internal/**",
                        "/api/util/**").permitAll()
                        .anyRequest().authenticated()
                )
                .sessionManagement(sess -> sess.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
                .addFilterBefore(authenticationFilter, UsernamePasswordAuthenticationFilter.class)
                .build();
    }

    @Bean
    GrantedAuthorityDefaults grantedAuthorityDefaults() {
        return new GrantedAuthorityDefaults(""); // Remove the ROLE_ prefix
    }


    @Bean
    public CorsConfigurationSource authCorsConfigurationSource() {
        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        CorsConfiguration config = new CorsConfiguration();
        List<String> allowedPatterns = new ArrayList<>();

        config.setAllowCredentials(true);
        config.setAllowedMethods(List.of("GET", "POST", "PUT", "DELETE", "OPTIONS"));
        config.setAllowedHeaders(List.of("*"));
        //Patterns di base presenti in CorsConfiguration
        allowedPatterns.add("http://*-svc");  // Internal calls (e.g., "http://someservice-svc")
        allowedPatterns.add("https://www.comune.roma.it*"); // Frontend calls from portal
        //Patterns da Properties
        allowedPatterns.add((corsPoliciesPatterns != null && !corsPoliciesPatterns.trim().isEmpty())
                ? corsPoliciesPatterns
                : "http://*.datacenter.comune.roma*");
        allowedPatterns.add((corsPolicies != null && !corsPolicies.trim().isEmpty())
                ? corsPolicies
                : "http://localhost:8080/*");
        //Allow origin "null" per OIDC
        allowedPatterns.add("null");
        config.setAllowedOriginPatterns(allowedPatterns);

        source.registerCorsConfiguration("/**", config);

        return source;
    }

}