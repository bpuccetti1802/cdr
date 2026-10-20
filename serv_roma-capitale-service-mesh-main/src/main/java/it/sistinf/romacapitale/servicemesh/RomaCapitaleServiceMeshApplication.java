package it.sistinf.romacapitale.servicemesh;

import io.micrometer.core.aop.CountedAspect;
import io.micrometer.core.aop.TimedAspect;
import io.micrometer.core.instrument.MeterRegistry;
import io.swagger.v3.oas.annotations.OpenAPIDefinition;
import io.swagger.v3.oas.annotations.info.Info;
import it.sistinf.romacapitale.integration.auth.api.LoginUtenteTecnicoClient;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.EnableAutoConfiguration;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.domain.EntityScan;
import org.springframework.boot.autoconfigure.jdbc.DataSourceAutoConfiguration;
import org.springframework.boot.autoconfigure.jdbc.DataSourceTransactionManagerAutoConfiguration;
import org.springframework.boot.autoconfigure.mongo.MongoAutoConfiguration;
import org.springframework.boot.autoconfigure.orm.jpa.HibernateJpaAutoConfiguration;
import org.springframework.boot.autoconfigure.security.servlet.SecurityAutoConfiguration;
import org.springframework.cloud.openfeign.EnableFeignClients;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.data.mongodb.repository.config.EnableMongoRepositories;
import org.springframework.security.config.annotation.web.configuration.WebSecurityCustomizer;
import org.springframework.security.web.firewall.StrictHttpFirewall;

@SpringBootApplication(exclude = {SecurityAutoConfiguration.class })
//@EnableJpaRepositories(basePackages = { "it.sistinf.romacapitale.servicemesh.repository.sql" })
//Mongo è attivo (commentare se non si vuole usare mongodb)
//@EnableMongoRepositories(basePackages = { "it.sistinf.romacapitale.servicemesh.repository.nosql" })
//Annotation per disabilitare Mongo
@EnableAutoConfiguration(exclude = {MongoAutoConfiguration.class, DataSourceAutoConfiguration.class, HibernateJpaAutoConfiguration.class
		,DataSourceTransactionManagerAutoConfiguration.class
})
//@EntityScan(basePackages = { "it.sistinf.romacapitale.servicemesh.model" })
@ComponentScan(basePackages = { "it.sistinf.romacapitale.servicemesh", "it.sistinf.romacapitale.core", "it.sistinf.romacapitale.integration" })
@OpenAPIDefinition(info = @Info(title = "roma-capitale-servicemesh", version = "0.0.1", description = "Documentazione API " + "servicemesh 0.0.1"))
@EnableFeignClients(clients = {LoginUtenteTecnicoClient.class})
public class RomaCapitaleServiceMeshApplication {

	public static void main(String[] args) {
		SpringApplication.run(RomaCapitaleServiceMeshApplication.class, args);
	}

	@Bean
	public TimedAspect timedAspect(MeterRegistry registry) {
		return new TimedAspect(registry);
	}

	@Bean
	public CountedAspect countedAspect(MeterRegistry registry) {
		return new CountedAspect(registry);
	}
	@Bean
	public WebSecurityCustomizer webSecurityCustomizer() {
		StrictHttpFirewall firewall = new StrictHttpFirewall();
		firewall.setAllowBackSlash(true);
		firewall.setAllowUrlEncodedDoubleSlash(true);
		return (web) -> web.httpFirewall(firewall);
	}
}
