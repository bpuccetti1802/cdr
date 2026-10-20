package it.sistinf.romacapitale.management.repository;

import it.sistinf.romacapitale.core.persistence.sql.AbstractRepository;
import it.sistinf.romacapitale.management.entity.ProfiloEntity;
import org.springframework.stereotype.Repository;

@Repository
public class ProfiloRepository extends AbstractRepository<Long, ProfiloEntity> {

    public ProfiloRepository() {
        super(ProfiloEntity.class);
    }
}
