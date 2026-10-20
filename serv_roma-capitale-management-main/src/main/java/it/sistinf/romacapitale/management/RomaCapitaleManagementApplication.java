package it.sistinf.romacapitale.management;

import io.micrometer.core.aop.CountedAspect;
import io.micrometer.core.aop.TimedAspect;
import io.micrometer.core.instrument.MeterRegistry;
import io.swagger.v3.oas.annotations.OpenAPIDefinition;
import io.swagger.v3.oas.annotations.info.Info;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.EnableAutoConfiguration;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.domain.EntityScan;
import org.springframework.boot.autoconfigure.mongo.MongoAutoConfiguration;
import org.springframework.boot.autoconfigure.security.servlet.SecurityAutoConfiguration;
import org.springframework.cloud.openfeign.EnableFeignClients;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;

@SpringBootApplication(exclude = {SecurityAutoConfiguration.class})
@EnableJpaRepositories(basePackages = { "it.sistinf.romacapitale.management.repository" })
@EntityScan(basePackages = { "it.sistinf.romacapitale.management.entity" })
@ComponentScan(basePackages = { "it.sistinf.romacapitale.management", "it.sistinf.romacapitale.core" })
@EnableAutoConfiguration(exclude={MongoAutoConfiguration.class})
@EnableFeignClients(basePackages = {
        "it.sistinf.romacapitale.integration.archiviazione.api"
})
@OpenAPIDefinition(info = @Info(title = "roma-capitale-management", version = "0.0.1", description = "Documentazione API " + "auth 0.0.1"))
public class RomaCapitaleManagementApplication {

	public static void main(String[] args) {
		SpringApplication.run(RomaCapitaleManagementApplication.class, args);
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
