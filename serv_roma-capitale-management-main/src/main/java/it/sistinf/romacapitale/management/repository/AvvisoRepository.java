package it.sistinf.romacapitale.management.repository;

import it.sistinf.romacapitale.core.persistence.sql.AbstractRepository;
import it.sistinf.romacapitale.management.entity.AvvisoEntity;
import org.springframework.stereotype.Repository;

@Repository
public class AvvisoRepository extends AbstractRepository<Long, AvvisoEntity> {

    public AvvisoRepository() {
        super(AvvisoEntity.class);
    }
}
