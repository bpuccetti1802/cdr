package it.sistinf.romacapitale.management.repository;

import it.sistinf.romacapitale.core.persistence.sql.AbstractRepository;
import it.sistinf.romacapitale.management.entity.ApplicazioneEntity;
import it.sistinf.romacapitale.management.entity.ApplicazioneEntityPK;
import org.springframework.stereotype.Repository;

@Repository
public class ApplicazioneRepository extends AbstractRepository<ApplicazioneEntityPK, ApplicazioneEntity> {

    public ApplicazioneRepository() {
        super(ApplicazioneEntity.class);
    }
}
