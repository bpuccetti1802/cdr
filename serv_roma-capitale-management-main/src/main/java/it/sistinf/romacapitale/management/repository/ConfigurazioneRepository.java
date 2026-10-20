package it.sistinf.romacapitale.management.repository;

import it.sistinf.romacapitale.core.persistence.sql.AbstractRepository;
import it.sistinf.romacapitale.management.entity.ConfigurazioneEntity;
import it.sistinf.romacapitale.management.entity.ConfigurazioneEntityPK;
import org.springframework.stereotype.Repository;

@Repository
public class ConfigurazioneRepository extends AbstractRepository<ConfigurazioneEntityPK, ConfigurazioneEntity> {

    public ConfigurazioneRepository() {
        super(ConfigurazioneEntity.class);
    }
}
