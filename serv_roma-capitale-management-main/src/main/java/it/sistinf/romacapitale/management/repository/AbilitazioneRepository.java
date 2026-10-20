package it.sistinf.romacapitale.management.repository;

import it.sistinf.romacapitale.core.persistence.sql.AbstractRepository;
import it.sistinf.romacapitale.management.entity.AbilitazioneEntity;
import org.springframework.stereotype.Repository;

@Repository
public class AbilitazioneRepository extends AbstractRepository<Long, AbilitazioneEntity> {

    public AbilitazioneRepository() {
        super(AbilitazioneEntity.class);
    }
}
