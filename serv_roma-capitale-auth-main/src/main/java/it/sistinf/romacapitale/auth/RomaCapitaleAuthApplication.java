package it.sistinf.romacapitale.auth;

import io.micrometer.core.aop.CountedAspect;
import io.micrometer.core.aop.TimedAspect;
import io.micrometer.core.instrument.MeterRegistry;
import io.swagger.v3.oas.annotations.OpenAPIDefinition;
import io.swagger.v3.oas.annotations.info.Info;
import it.sistinf.romacapitale.integration.management.api.ApplicazioneClient;
import it.sistinf.romacapitale.integration.management.api.UtenteClient;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.EnableAutoConfiguration;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.jdbc.DataSourceAutoConfiguration;
import org.springframework.boot.autoconfigure.mongo.MongoAutoConfiguration;
import org.springframework.boot.autoconfigure.orm.jpa.HibernateJpaAutoConfiguration;
import org.springframework.boot.autoconfigure.security.servlet.SecurityAutoConfiguration;
import org.springframework.cloud.openfeign.EnableFeignClients;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.ComponentScan;

@SpringBootApplication(exclude = {SecurityAutoConfiguration.class })
@EnableAutoConfiguration(exclude={DataSourceAutoConfiguration.class, HibernateJpaAutoConfiguration.class, MongoAutoConfiguration.class})
@ComponentScan(basePackages = { "it.sistinf.romacapitale.auth", "it.sistinf.romacapitale.core", "it.sistinf.romacapitale.integration" })
@EnableFeignClients(clients = {UtenteClient.class, ApplicazioneClient.class})
@OpenAPIDefinition(info = @Info(title = "roma-capitale-auth", version = "0.0.1", description = "Documentazione API " + "auth 0.0.1"))
public class RomaCapitaleAuthApplication {

	public static void main(String[] args) {
		SpringApplication.run(RomaCapitaleAuthApplication.class, args);
	}

	@Bean
	public TimedAspect timedAspect(MeterRegistry registry) {
		return new TimedAspect(registry);
	}

	@Bean
	public CountedAspect countedAspect(MeterRegistry registry) {
		return new CountedAspect(registry);
	}

}
