package it.sistinf.romacapitale.servicemesh.config;

import org.apache.hc.client5.http.impl.classic.CloseableHttpClient;
import org.apache.hc.client5.http.impl.classic.HttpClients;
import org.apache.hc.client5.http.impl.io.PoolingHttpClientConnectionManager;
import org.apache.hc.client5.http.impl.io.PoolingHttpClientConnectionManagerBuilder;
import org.apache.hc.client5.http.ssl.NoopHostnameVerifier;
import org.apache.hc.client5.http.ssl.SSLConnectionSocketFactoryBuilder;
import org.apache.hc.core5.ssl.SSLContexts;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.io.ClassPathResource;
import org.springframework.http.client.HttpComponentsClientHttpRequestFactory;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.util.DefaultUriBuilderFactory;

import javax.net.ssl.SSLContext;
import java.io.InputStream;
import java.security.KeyStore;

@Configuration
public class RestTemplateConfig {

    @Value("${trust-store-path:}")
    private String trustStorePath;

    @Value("${trust-store-password:service-mesh}")
    private String trustStorePassword;

    @Value("${trust-store-type:JKS}")
    private String trustStoreType;

    @Value("${http.request.factory.timeout:10000}")
    private Integer CONNECT_TIMEOUT;

    @Bean
    public RestTemplate restTemplateExternal() throws Exception {
        KeyStore trustStore = KeyStore.getInstance(trustStoreType);
        try (InputStream is = new ClassPathResource(trustStorePath.replace("classpath:", "")).getInputStream()) {
            trustStore.load(is, trustStorePassword.toCharArray());
        }

        SSLContext sslContext = SSLContexts.custom()
                .loadTrustMaterial(trustStore, null)
                .build();

        PoolingHttpClientConnectionManager connectionManager =
                PoolingHttpClientConnectionManagerBuilder.create()
                        .setSSLSocketFactory(
                                SSLConnectionSocketFactoryBuilder.create()
                                        .setSslContext(sslContext)
                                        .setHostnameVerifier(NoopHostnameVerifier.INSTANCE)
                                        .build()
                        )
                        .setMaxConnTotal(100)
                        .setMaxConnPerRoute(20)
                        .build();

        CloseableHttpClient httpClient = HttpClients.custom()
                .setConnectionManager(connectionManager)
                .build();

        return createRestTemplate(httpClient);
    }

    @Bean
    public RestTemplate restTemplateInternal() {
        return createRestTemplate(HttpClients.createDefault());
    }

    private RestTemplate createRestTemplate(CloseableHttpClient httpClient) {
        HttpComponentsClientHttpRequestFactory factory = new HttpComponentsClientHttpRequestFactory(httpClient);
        factory.setConnectTimeout(CONNECT_TIMEOUT);
        factory.setConnectionRequestTimeout(CONNECT_TIMEOUT);
        // factory.setReadTimeout(READ_TIMEOUT);

        RestTemplate restTemplate = new RestTemplate(factory);
        DefaultUriBuilderFactory uriFactory = new DefaultUriBuilderFactory();
        uriFactory.setEncodingMode(DefaultUriBuilderFactory.EncodingMode.NONE);
        restTemplate.setUriTemplateHandler(uriFactory);

        return restTemplate;
    }
}