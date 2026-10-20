package it.sistinf.romacapitale.management.repository;

import it.sistinf.romacapitale.core.persistence.sql.AbstractRepository;
import it.sistinf.romacapitale.management.entity.EnteEntity;
import org.springframework.stereotype.Repository;

@Repository
public class EnteRepository extends AbstractRepository<Long, EnteEntity> {

    public EnteRepository() {
        super(EnteEntity.class);
    }
}
